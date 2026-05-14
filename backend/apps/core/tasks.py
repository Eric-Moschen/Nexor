from celery import shared_task

from apps.core.events.base import InternalEvent
from apps.core.events.dispatcher import EventDispatcher


@shared_task
def process_internal_event(event_payload):
    event = InternalEvent(**event_payload)
    return EventDispatcher().publish(event).id


@shared_task
def dispatch_notification_digest():
    from apps.core.models import Notification

    return Notification.objects.filter(is_read=False).count()
