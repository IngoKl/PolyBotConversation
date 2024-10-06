import logging

from django.core.management.base import BaseCommand

from chat.models import Conversation
from chat.tasks import generate_core_memories
from chat.triggers import general

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create a chat completion for a conversation using the specified bot"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        conversation = Conversation.objects.last()
        logger.info(conversation.uuid)

        bot = conversation.participants.filter(participant_type="bot").first().bot
        general(conversation=conversation)
        # generate_core_memories(conversation=conversation)
