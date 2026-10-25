/**
 * Quizify Core Quiz Engine
 * - Anti-Drift Asynchronous Countdown Timer using absolute timestamp deltas
 * - Event Delegation & DOM UI State Synchronizer
 * - SessionStorage Resilience (Timer & Answer Persistence across refreshes)
 * - WCAG 2.1 AA Dynamic Announcements & Keyboard Focus Management
 */
(() => {
    'use strict';

    class QuizEngine {
        constructor() {
            // DOM Elements
            this.timerDisplay = document.getElementById('quiz-timer');
            this.timerBadge = document.getElementById('timer-badge');
            this.quizForm = document.getElementById('quiz-form');
            this.timeTakenInput = document.getElementById('time-taken-seconds');
            this.submitBtn = document.getElementById('btn-submit-quiz');
            this.questionsContainer = document.getElementById('questions-container');
            this.srAnnouncer = document.getElementById('sr-announcer');
            
            // Progress Bar Elements
            this.progressText = document.getElementById('progress-text');
            this.progressBarFill = document.getElementById('progress-bar-fill');
            this.progressBar = document.getElementById('quiz-progress-bar');

            // Modal Elements
            this.unansweredModalEl = document.getElementById('unansweredModal');
            this.unansweredModal = (this.unansweredModalEl && window.bootstrap) ? new bootstrap.Modal(this.unansweredModalEl) : null;
            this.unansweredCountText = document.getElementById('unanswered-count-text');
            this.btnConfirmSubmit = document.getElementById('btn-confirm-incomplete-submit');
            this.btnJumpUnanswered = document.getElementById('btn-jump-first-unanswered');

            if (!this.timerDisplay || !this.quizForm) return;

            // Quiz Config & State
            this.quizId = this.timerDisplay.getAttribute('data-quiz-id') || 'default';
            this.totalDurationSeconds = parseInt(this.timerDisplay.getAttribute('data-duration') || '600', 10);
            
            this.storageKeyPrefix = `quizify_${this.quizId}`;
            this.storageTimerKey = `${this.storageKeyPrefix}_deadline`;
            this.storageAnswersKey = `${this.storageKeyPrefix}_answers`;

            this.totalQuestions = document.querySelectorAll('.question-card').length;
            this.answersState = new Map();
            this.timerInterval = null;
            this.isSubmitting = false;

            this.init();
        }

        /**
         * Initialize State, Storage & Event Listeners
         */
        init() {
            this.initTimer();
            this.restoreSavedAnswers();
            this.updateProgress();
            this.bindEvents();
        }

        /**
         * 1. Anti-Drift Timer Architecture
         * Uses target timestamp delta rather than simple decrements to prevent 
         * background tab execution throttling and event loop drift.
         */
        initTimer() {
            const now = Date.now();
            let targetDeadline = sessionStorage.getItem(this.storageTimerKey);

            if (!targetDeadline) {
                targetDeadline = now + (this.totalDurationSeconds * 1000);
                sessionStorage.setItem(this.storageTimerKey, targetDeadline.toString());
            } else {
                targetDeadline = parseInt(targetDeadline, 10);
            }

            this.deadline = targetDeadline;
            this.tick(); // Immediate initial render

            this.timerInterval = setInterval(() => this.tick(), 1000);
        }

        tick() {
            const now = Date.now();
            const remainingMs = Math.max(0, this.deadline - now);
            const remainingSeconds = Math.ceil(remainingMs / 1000);
            const elapsedSeconds = Math.max(0, this.totalDurationSeconds - remainingSeconds);

            // Update hidden input for backend consumption
            if (this.timeTakenInput) {
                this.timeTakenInput.value = elapsedSeconds;
            }

            // Update display
            this.timerDisplay.textContent = this.formatTime(remainingSeconds);

            // Warnings at milestones
            if (remainingSeconds <= 60 && remainingSeconds > 0) {
                if (this.timerBadge && !this.timerBadge.classList.contains('warning')) {
                    this.timerBadge.classList.add('warning');
                    this.announceToScreenReader('Warning: Less than one minute remaining on your quiz.');
                }
            }

            // Auto-submit on expiration
            if (remainingSeconds <= 0) {
                this.handleTimeExpired();
            }
        }

        formatTime(seconds) {
            const mins = Math.floor(seconds / 60);
            const secs = seconds % 60;
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }

        handleTimeExpired() {
            if (this.isSubmitting) return;
            clearInterval(this.timerInterval);
            this.isSubmitting = true;

            this.announceToScreenReader('Time has expired. Submitting your quiz now.');
            this.timerDisplay.textContent = '00:00';
            
            // Clean up session storage before submission
            this.clearSessionState();

            // Submit form automatically without confirmation modal
            this.quizForm.submit();
        }

        /**
         * 2. Event Delegation for Option Selection & UI State Sync
         * Single event listener on parent form minimizes memory allocation and garbage collection churn.
         */
        bindEvents() {
            // Listen for input changes via event bubbling
            this.quizForm.addEventListener('change', (e) => {
                if (e.target && e.target.matches('.option-input')) {
                    this.handleOptionSelected(e.target);
                }
            });

            // Intercept form submission for validation
            this.quizForm.addEventListener('submit', (e) => this.handleFormSubmit(e));

            // Modal actions
            if (this.btnConfirmSubmit) {
                this.btnConfirmSubmit.addEventListener('click', () => {
                    this.isSubmitting = true;
                    this.clearSessionState();
                    if (this.unansweredModal) this.unansweredModal.hide();
                    this.quizForm.submit();
                });
            }

            if (this.btnJumpUnanswered) {
                this.btnJumpUnanswered.addEventListener('click', () => {
                    if (this.unansweredModal) this.unansweredModal.hide();
                    this.scrollToFirstUnanswered();
                });
            }

            // Prevent accidental browser closure
            window.addEventListener('beforeunload', (e) => {
                if (!this.isSubmitting) {
                    e.preventDefault();
                    e.returnValue = 'Your quiz is still in progress. Changes are saved, but the timer keeps running.';
                    return e.returnValue;
                }
            });
        }

        handleOptionSelected(input) {
            const questionId = input.getAttribute('data-question-id');
            const selectedVal = input.value;

            // 1. Update State Map
            this.answersState.set(questionId, selectedVal);

            // 2. Persist to SessionStorage
            this.persistAnswers();

            // 3. Update Visual Status of Question Card
            this.updateQuestionCardUI(questionId);

            // 4. Update Completion Progress
            this.updateProgress();
        }

        updateQuestionCardUI(questionId) {
            const statusBadge = document.getElementById(`status-badge-${questionId}`);
            if (statusBadge) {
                statusBadge.textContent = 'Answered';
                statusBadge.className = 'status-indicator badge bg-success-subtle text-success border border-success-subtle';
            }
        }

        /**
         * 3. Client-Side Session Storage Resilience
         */
        persistAnswers() {
            const answersObj = Object.fromEntries(this.answersState);
            sessionStorage.setItem(this.storageAnswersKey, JSON.stringify(answersObj));
        }

        restoreSavedAnswers() {
            try {
                const saved = sessionStorage.getItem(this.storageAnswersKey);
                if (!saved) return;

                const parsed = JSON.parse(saved);
                Object.entries(parsed).forEach(([qId, val]) => {
                    this.answersState.set(qId, val);

                    // Re-check input in the DOM
                    const radio = this.quizForm.querySelector(`input[name="question_${qId}"][value="${val}"]`);
                    if (radio) {
                        radio.checked = true;
                        this.updateQuestionCardUI(qId);
                    }
                });
            } catch (err) {
                console.error('Failed to parse saved quiz state:', err);
            }
        }

        clearSessionState() {
            sessionStorage.removeItem(this.storageTimerKey);
            sessionStorage.removeItem(this.storageAnswersKey);
        }

        /**
         * 4. Progress Tracking & DOM Batch Updates
         */
        updateProgress() {
            const answeredCount = this.answersState.size;
            const percentage = this.totalQuestions > 0 
                ? Math.round((answeredCount / this.totalQuestions) * 100) 
                : 0;

            if (this.progressBarFill) {
                this.progressBarFill.style.width = `${percentage}%`;
            }

            if (this.progressBar) {
                this.progressBar.setAttribute('aria-valuenow', percentage.toString());
            }

            if (this.progressText) {
                this.progressText.textContent = `${answeredCount} of ${this.totalQuestions} answered (${percentage}%)`;
            }
        }

        /**
         * 5. Accidental Submission Prevention & Modal Workflow
         */
        handleFormSubmit(e) {
            if (this.isSubmitting) return;

            const answeredCount = this.answersState.size;
            const unansweredCount = this.totalQuestions - answeredCount;

            // If some questions are unanswered, prevent immediate submission and prompt user
            if (unansweredCount > 0) {
                e.preventDefault();
                if (this.unansweredCountText) {
                    this.unansweredCountText.textContent = unansweredCount.toString();
                }
                if (this.unansweredModal) {
                    this.unansweredModal.show();
                } else if (confirm(`You have ${unansweredCount} unanswered question(s). Are you sure you want to submit?`)) {
                    this.isSubmitting = true;
                    this.clearSessionState();
                    this.quizForm.submit();
                }
                return;
            }

            // Normal complete submission confirmation
            if (!confirm('Are you ready to submit your quiz?')) {
                e.preventDefault();
                return;
            }

            this.isSubmitting = true;
            if (this.submitBtn) {
                this.submitBtn.disabled = true;
                this.submitBtn.innerHTML = `<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Submitting...`;
            }
            this.clearSessionState();
        }

        scrollToFirstUnanswered() {
            const allQuestionCards = document.querySelectorAll('.question-card');
            for (const card of allQuestionCards) {
                const qId = card.getAttribute('data-question-id');
                if (!this.answersState.has(qId)) {
                    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    // Set focus to the first radio in that card for accessibility
                    const firstRadio = card.querySelector('.option-input');
                    if (firstRadio) firstRadio.focus();
                    break;
                }
            }
        }

        announceToScreenReader(message) {
            if (this.srAnnouncer) {
                this.srAnnouncer.textContent = message;
            }
        }
    }

    // Initialize when DOM content is fully loaded
    document.addEventListener('DOMContentLoaded', () => {
        new QuizEngine();
    });
})();
