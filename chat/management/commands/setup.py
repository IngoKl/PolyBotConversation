from django.core.management.base import BaseCommand
from django_q.tasks import schedule

from chat.models import Trigger


class Command(BaseCommand):
    help = "Setup the application"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        # Populate database

        # Triggers
        trigger_names = ["general", "mention"]

        for name in trigger_names:
            Trigger.objects.get_or_create(name=name)

        # Schedule general tasks

        schedule(
            "chat.tasks.update_conversation_titles",
            schedule_type="I",
            minutes=1,
            name="update_conversation_titles",
        )
