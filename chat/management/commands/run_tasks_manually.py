from django.core.management.base import BaseCommand

from chat.tasks import update_conversation_titles


class Command(BaseCommand):
    help = "Run the tasks from register_tasks.py"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        update_conversation_titles()
