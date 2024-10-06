from django.urls import include, path

from chat import views

app_name = "chat"

urlpatterns = [
    path("", views.index, name="index"),
    path("user/", views.user, name="user"),
    path("chat/new/", views.chat_new, name="chat_new"),
    path("chat/clear/", views.chat_clear, name="chat_clear"),
    path("chat/<uuid:conversation_uuid>/", views.chat, name="chat"),
    path("<uuid:conversation_uuid>/", views.chat, name="chat"),
    path(
        "<uuid:conversation_uuid>/load_messages/",
        views.load_messages,
        name="load_messages",
    ),
    path(
        "<uuid:conversation_uuid>/send_message/",
        views.send_message,
        name="send_message",
    ),
    path(
        "chat/<uuid:conversation_uuid>/title",
        views.conversation_title,
        name="conversation_title",
    ),
    path(
        "chat/<uuid:conversation_uuid>/manage_bots/",
        views.manage_bots_in_conversation,
        name="manage_bots_in_conversation",
    ),
    path(
        "chat/<uuid:conversation_uuid>/manage_triggers/",
        views.manage_triggers_for_conversation,
        name="manage_triggers_for_conversation",
    ),
    path("chat/<uuid:conversation_uuid>/delete/", views.chat_delete, name="chat_delete"),
    path("accounts/", include("django.contrib.auth.urls")),
]
