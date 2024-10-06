import logging

import openai
from django.conf import settings
from django.core.management.base import BaseCommand

from chat import bot
from chat.models import Bot, Conversation, Message

logger = logging.getLogger(__name__)

# Make sure you set the OpenAI API key
openai.api_key = settings.OPENAI_API_KEY


class Command(BaseCommand):
    help = "Create a chat completion for a conversation using the specified bot"

    def add_arguments(self, parser):
        parser.add_argument("trigger", type=str, help="Trigger for the chat message")
        parser.add_argument("conversation_id", type=int, help="ID of the conversation")
        parser.add_argument("message_id", type=int, help="ID of the message", default=None)
        parser.add_argument("bot_id", type=int, help="ID of the bot")

    def handle(self, *args, **kwargs):
        trigger = kwargs["trigger"]
        conversation_id = kwargs["conversation_id"]
        message_id = kwargs["message_id"]
        bot_id = kwargs["bot_id"]

        if trigger == "general":
            conversation = Conversation.objects.get(id=conversation_id)
            chatbot = Bot.objects.get(id=bot_id)
            logger.info(bot.generate_message_general(conversation, chatbot))

        if trigger == "mention":
            conversation = Conversation.objects.get(id=conversation_id)
            message = Message.objects.get(id=message_id)
            chatbot = Bot.objects.get(id=bot_id)
            logger.info(bot.generate_message_mention(conversation, message, chatbot))
