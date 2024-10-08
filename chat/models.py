import uuid

from django.contrib.auth.models import User
from django.db import models


class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=18, default="#cd5334ff")
    model = models.CharField(max_length=255)
    prompt = models.TextField()
    temperature = models.FloatField(default=0.8)

    def __str__(self):
        return f"Bot {self.id} {self.name} ({self.model})"

    def get_core_memories_for_prompt(self, n_last_memories=1000):
        core_memories = self.core_memories.all().order_by("-timestamp")[:n_last_memories]
        core_memories = [f"- {cm.memory}" for cm in core_memories]
        return "\n".join(core_memories)


class Trigger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"Trigger {self.id}: {self.name}"


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True, default="New Conversation")
    creation_date = models.DateTimeField(auto_now_add=True)
    title_update_date = models.DateTimeField(auto_now=True)
    participants = models.ManyToManyField("Participant", related_name="conversations")
    triggers = models.ManyToManyField(Trigger, related_name="conversations", blank=True)

    def __str__(self):
        return f"Conversation {self.uuid} created on {self.creation_date}"

    def list_of_bots(self):
        return ", ".join([participant.name() for participant in self.participants.filter(participant_type="bot")])

    def list_of_humans(self):
        return ", ".join([participant.name() for participant in self.participants.filter(participant_type="user")])


class Participant(models.Model):
    PARTICIPANT_TYPE_CHOICES = (
        ("user", "User"),
        ("bot", "Bot"),
    )

    id = models.AutoField(primary_key=True)
    participant_type = models.CharField(max_length=10, choices=PARTICIPANT_TYPE_CHOICES)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="participant_user",
    )
    bot = models.ForeignKey(
        Bot,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="participant_bot",
    )

    def __str__(self):
        return f"Participant ({self.participant_type}) - {'User: ' + self.user.username if self.user else 'Bot: ' + self.bot.name}"

    def name(self):
        return self.user.username if self.participant_type == "user" else self.bot.name


class Message(models.Model):
    id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name="sent_messages")
    timestamp = models.DateTimeField(auto_now_add=True)
    triggered_bots = models.ManyToManyField(Bot, related_name="responded_messages", blank=True)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.participant} at {self.timestamp} in conversation {self.conversation.uuid}"

    def participant_name(self):
        return self.participant.user.username if self.participant.participant_type == "user" else self.participant.bot.name


class LLMRequest(models.Model):
    id = models.AutoField(primary_key=True)
    request_type = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    prompt = models.TextField()
    response = models.TextField()
    total_tokens = models.IntegerField(editable=False, default=0)
    completion_tokens = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return f"LLMRequest {self.id} at {self.timestamp}"


class CoreMemory(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    memory = models.TextField()
    bot = models.ForeignKey(Bot, on_delete=models.CASCADE, related_name="core_memories")

    def __str__(self):
        return f"CoreMemory {self.id} for Bot {self.bot.name} at {self.timestamp}"
