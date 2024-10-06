from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from django_q.models import Schedule
from django_q.tasks import async_task, schedule

from chat.forms import ManageBotsForm, ManageTriggersForm
from chat.llm import llm_conversation_title
from chat.models import Conversation, Message, Participant, Trigger
from chat.triggers import mention


@login_required
def index(request):
    context = {
        "conversations": Conversation.objects.all(),
        "version": settings.VERSION,
    }

    return render(request, "chat/index.html", context)


@login_required
def chat_new(request):
    # Create a new conversation
    conversation = Conversation.objects.create()

    # Create a participant for the logged-in user
    participant = Participant.objects.get(participant_type="user", user=request.user)
    conversation.participants.add(participant)

    # Add default trigger
    conversation.triggers.add(Trigger.objects.get(name="mention"))

    # Add task
    schedule(
        "chat.tasks.generate_messages",
        conversation_id=conversation.id,
        schedule_type="I",
        minutes=1,
        name=f"generate_messages_{conversation.uuid}",
    )

    # Redirect to the chat view for the newly created conversation
    return redirect(f"/chat/{conversation.uuid}")


@login_required
def chat(request, conversation_uuid=False):
    # Fetch the conversation instance based on the UUID provided as a query parameter
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)

    # Retrieve all participants (both users and bots) from the conversation
    participants = conversation.participants.select_related("user", "bot").all()

    # Retrieve all messages for the conversation
    messages = Message.objects.filter(conversation=conversation).select_related("participant__user", "participant__bot").order_by("timestamp")

    # Create the context to pass to the template
    context = {
        "conversations": Conversation.objects.all(),
        "conversation": conversation,
        "messages": messages,
        "participants": participants,
        "version": settings.VERSION,
    }

    return render(request, "chat/chat.html", context)


@login_required
def user(request):
    context = {
        "conversations": Conversation.objects.all(),
        "version": settings.VERSION,
    }

    return render(request, "chat/user.html", context)


@login_required
def load_messages(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)
    messages = Message.objects.filter(conversation=conversation).select_related("participant__user", "participant__bot").order_by("timestamp")
    return render(request, "chat/partials/messages.html", {"messages": messages})


@login_required
def conversation_title(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)

    return HttpResponse(llm_conversation_title(conversation))


@login_required
@require_http_methods(["POST"])
def send_message(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)
    participant = conversation.participants.filter(user=request.user).first()  # Assuming the logged-in user is the sender

    if participant and "message" in request.POST:
        message_content = request.POST["message"]
        Message.objects.create(conversation=conversation, participant=participant, message=message_content)

        if conversation.triggers.filter(name="mention").exists():
            mention(conversation)

    # Return updated messages list
    messages = Message.objects.filter(conversation=conversation).select_related("participant__user", "participant__bot").order_by("timestamp")
    return render(request, "chat/partials/messages.html", {"messages": messages})


@login_required
@require_http_methods(["GET", "POST"])
def manage_bots_in_conversation(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)

    if request.method == "POST":
        form = ManageBotsForm(request.POST)
        if form.is_valid():
            current_bots = conversation.participants.filter(participant_type="bot")
            selected_bots = form.cleaned_data["bots"]

            removed_bots = current_bots.exclude(bot__in=selected_bots)

            for removed_bot in removed_bots:
                conversation.participants.remove(removed_bot)

            for bot in selected_bots:
                participant, created = Participant.objects.get_or_create(participant_type="bot", bot=bot)
                conversation.participants.add(participant)

            return redirect("chat:chat", conversation_uuid=conversation_uuid)
    else:
        form = ManageBotsForm(initial={"bots": conversation.participants.filter(participant_type="bot").values_list("bot", flat=True)})

    # Create the context to pass to the template
    context = {
        "conversations": Conversation.objects.all(),
        "form": form,
        "conversation": conversation,
        "version": settings.VERSION,
    }

    return render(request, "chat/manage_bots.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def manage_triggers_for_conversation(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)

    if request.method == "POST":
        form = ManageTriggersForm(request.POST)
        if form.is_valid():
            current_triggers = conversation.triggers.all()
            selected_triggers = form.cleaned_data["triggers"]

            removed_triggers = current_triggers.exclude(id__in=selected_triggers)

            for removed_trigger in removed_triggers:
                conversation.triggers.remove(removed_trigger)

            for trigger in selected_triggers:
                conversation.triggers.add(trigger)

            return redirect("chat:chat", conversation_uuid=conversation_uuid)
    else:
        form = ManageTriggersForm(initial={"triggers": conversation.triggers.all().values_list(flat=True)})

    # Create the context to pass to the template
    context = {
        "conversations": Conversation.objects.all(),
        "form": form,
        "conversation": conversation,
        "version": settings.VERSION,
    }

    return render(request, "chat/manage_triggers.html", context)


@login_required
def chat_clear(request):
    conversations = Conversation.objects.all()

    for conversation in conversations:
        Schedule.objects.filter(name=f"generate_messages_{conversation.uuid}").delete()

        if settings.BUILD_CORE_MEMORIES:
            async_task("chat.tasks.generate_core_memories", conversation)

        conversation.delete()

    return redirect("chat:index")


@login_required
def chat_delete(request, conversation_uuid):
    conversation = get_object_or_404(Conversation, uuid=conversation_uuid)
    Schedule.objects.filter(name=f"generate_messages_{conversation.uuid}").delete()

    if settings.BUILD_CORE_MEMORIES:
        async_task("chat.tasks.generate_core_memories", conversation)

    conversation.delete()

    return redirect("chat:index")
