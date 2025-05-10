
from django import template
from ..models import Notification

register = template.Library()

@register.filter
def unread_notifications_count(user):
    if user.is_authenticated:
        return Notification.objects.filter(recipient=user, read=False).count()
    return 0