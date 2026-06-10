from .models import Notification

def create_notification(user, title, message, link=None):
    """
    Helper function to create a notification for a user.
    """
    notification = Notification.objects.create(
        user=user,
        title=title,
        message=message,
        link=link
    )
    return notification
