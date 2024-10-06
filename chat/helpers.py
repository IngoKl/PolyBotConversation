import logging

from django.conf import settings

from chat.prompt_templates import prompts

logger = logging.getLogger(__name__)


def detect_mention(bot_name, message):
    if f"@{bot_name.lower()}" in message.lower():
        return True


def judge_bot_determination(bot_response):
    if bot_response.lower().strip() == "yes" or bot_response.lower().strip() == "yes.":
        return True
    else:
        return False


def get_system_prompt(conversation, bot):
    system_promopt = prompts["bots_in_conversation"].format(
        bot_name=bot.name,
        list_of_bots=conversation.list_of_bots(),
        list_of_humans=conversation.list_of_humans(),
        bot_prompt=bot.prompt,
        core_memories=bot.get_core_memories_for_prompt(n_last_memories=settings.MAX_CORE_MEMORIES_PER_PROMPT),
    )
    logger.debug(f"System Prompt: {system_promopt}")

    return system_promopt
