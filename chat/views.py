from itertools import groupby

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .models import ChatMessage


class ChatView(LoginRequiredMixin, View):
    template_name = "chat/chat.html"

    def get(self, request, *args, **kwargs):
        messages = (
            ChatMessage.objects.select_related("user")
            .all()
            .order_by("-created_at")[:200]
        )
        messages = list(reversed(messages))

        # Группировка сообщений по датам для разделителей (как в мессенджерах)
        grouped = []
        for day, msgs in groupby(messages, key=lambda m: m.created_at.date()):
            grouped.append((day, list(msgs)))

        return render(request, self.template_name, {"groups": grouped})

    def post(self, request, *args, **kwargs):
        text = (request.POST.get("text") or "").strip()
        if not text:
            return redirect("chat:chat")
        ChatMessage.objects.create(user=request.user, text=text)
        return redirect("chat:chat")
