from django.contrib import admin

from chat.models import Bot, Conversation, CoreMemory, LLMRequest, Message, Participant, Trigger


class CoreMemoryInline(admin.TabularInline):
    model = CoreMemory
    extra = 0


class BotAdmin(admin.ModelAdmin):
    inlines = [CoreMemoryInline]


class LLMRequestAdmin(admin.ModelAdmin):
    readonly_fields = ("total_tokens", "completion_tokens")


admin.site.register(Conversation)
admin.site.register(Participant)
admin.site.register(Bot, BotAdmin)
admin.site.register(Message)
admin.site.register(Trigger)
admin.site.register(LLMRequest, LLMRequestAdmin)
admin.site.register(CoreMemory)
