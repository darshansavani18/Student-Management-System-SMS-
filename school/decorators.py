from django.http import HttpResponseForbidden
# Used to return a 403 Forbidden response when access is denied

from .utils import is_admin, is_teacher, is_student
# Utility functions to check user roles based on groups


def admin_only(view_func):
    """
    Decorator to allow access only to Admin users.
    """

    def wrapper(request, *args, **kwargs):
        # Check if the logged-in user is an admin
        if is_admin(request.user):
            return view_func(request, *args, **kwargs)

        # Block access if user is not admin
        return HttpResponseForbidden("Access Denied")

    return wrapper


def teacher_only(view_func):
    """
    Decorator to allow access only to Teacher users.
    """

    def wrapper(request, *args, **kwargs):
        # Check if the logged-in user is a teacher
        if is_teacher(request.user):
            return view_func(request, *args, **kwargs)

        # Block access if user is not teacher
        return HttpResponseForbidden("Access Denied")

    return wrapper


def student_only(view_func):
    """
    Decorator to allow access only to Student users.
    """

    def wrapper(request, *args, **kwargs):
        # Check if the logged-in user is a student
        if is_student(request.user):
            return view_func(request, *args, **kwargs)

        # Block access if user is not student
        return HttpResponseForbidden("Access Denied")

    return wrapper


def admin_or_teacher_only(view_func):
    """
    Decorator to allow access to both Admin and Teacher users.
    """

    def wrapper(request, *args, **kwargs):
        # Check if user belongs to Admin or Teacher group
        if request.user.groups.filter(name__in=['Admin', 'Teacher']).exists():
            return view_func(request, *args, **kwargs)

        # Block access for all other users
        return HttpResponseForbidden('Access Denied')

    return wrapper
