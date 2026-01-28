from .models import Notification

def is_admin(user):
    return user.is_superuser or user.groups.filter(name='Admin').exists()

def is_teacher(user):
    return user.groups.filter(name='Teacher').exists()

def is_student(user):
    return user.groups.filter(name='Student').exists()

def create_notification(user, title, message):
    Notification.objects.create(
        user = user,
        title = title,
        message = message
    )