import logging
import time

from chat.bot import generate_message_general, generate_message_mention
from chat.helpers import detect_mention

logger = logging.getLogger(__name__)


def mention(conversation):
    bots = [participant.bot for participant in conversation.participants.filter(participant_type="bot")]

    for bot in bots:
        messages = conversation.messages.exclude(triggered_bots__id=bot.id).exclude(participant__bot__id=bot.id)

        for message in messages:
            if detect_mention(bot.name, message.message):
                logger.info(f'Mention detected: {bot.name} in "{message.message}"')
                message.triggered_bots.add(bot)
                generate_message_mention(conversation, message, bot)


def general(conversation):
    bots = [participant.bot for participant in conversation.participants.filter(participant_type="bot")]

    for bot in bots:
        generate_message_general(conversation, bot)
        time.sleep(5)
