from django_q.tasks import async_task

from chat.llm import llm_conversation_title, llm_form_core_memories
from chat.models import Conversation
from chat.triggers import general, mention


def update_conversation_titles():
    conversations = Conversation.objects.all()

    for conversation in conversations:
        try:
            if conversation.messages.last().timestamp > conversation.title_update_date or conversation.title is None:
                llm_conversation_title(conversation)
        except AttributeError:
            pass

    return True


def generate_messages(conversation_id):
    conversation = Conversation.objects.get(id=conversation_id)

    for trigger in conversation.triggers.all():
        if trigger.name == "mention":
            async_task(mention, conversation)

        if trigger.name == "general":
            async_task(general, conversation)


def generate_core_memories(conversation):
    bots = [participant.bot for participant in conversation.participants.filter(participant_type="bot")]
    for bot in bots:
        llm_form_core_memories(conversation, bot)
