from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    """
    Decorator for views that checks if the user is logged in and is staff or superuser.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in with admin privileges to access this area.")
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access denied. Administrator privileges required.")
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def anonymous_required(view_func):
    """
    Decorator for views that allows only unauthenticated users (e.g. login, register).
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff or request.user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('user_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
