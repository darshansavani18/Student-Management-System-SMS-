from .models import Notification

def notification_count(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(
            user = request.user,
            is_read = False
        ).count()
    else:
        count = 0
    return {'notification_count': count}


def user_roles(request):
    # Get the currently logged-in user from the request object
    user = request.user

    return {
        # True if the user is authenticated and either:
        # - a Django superuser, or
        # - belongs to the 'Admin' group
        'is_admin': user.is_authenticated and (
            user.is_superuser or user.groups.filter(name='Admin').exists()
        ),
        # True if the user is authenticated and belongs to the 'Teacher' group
        'is_teacher': user.is_authenticated and user.groups.filter(name='Teacher').exists(),
         # True if the user is authenticated and belongs to the 'Student' group
        'is_student': user.is_authenticated and user.groups.filter(name='Student').exists(),
    }

"""
    Context processor that determines the role of the currently logged-in user.

    This function checks whether the authenticated user belongs to
    specific Django groups (Admin, Teacher, Student) or has superuser privileges.

    The returned dictionary is automatically available in all templates,
    allowing role-based UI rendering (menus, buttons, permissions).
"""