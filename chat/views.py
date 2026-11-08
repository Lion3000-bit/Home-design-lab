from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from .models import ChatMessage


class ChatView(LoginRequiredMixin, View):
    template_name = "chat/chat.html"

    def get(self, request, *args, **kwargs):
        messages = ChatMessage.objects.select_related("user").order_by("-created_at")[:100]
        messages = list(reversed(messages))
        return render(
            request,
            self.template_name,
            {"messages": messages},
        )

    def post(self, request, *args, **kwargs):
        text = (request.POST.get("text") or "").strip()
        if not text:
            return redirect("chat:chat")
        ChatMessage.objects.create(user=request.user, text=text)
        return redirect("chat:chat")
