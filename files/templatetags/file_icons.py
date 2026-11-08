from django import template

register = template.Library()


@register.filter
def file_icon(content_type):
    """Возвращает эмодзи-иконку для типа файла."""
    ct = (content_type or "").lower()
    if ct.startswith("image/"):
        return "🖼️"
    if ct.startswith("video/"):
        return "🎬"
    if ct.startswith("audio/"):
        return "🎵"
    if ct.startswith("text/") or ct in (
        "application/json",
        "application/xml",
        "application/javascript",
    ):
        return "📄"
    if "pdf" in ct:
        return "📕"
    if "zip" in ct or "compressed" in ct:
        return "🗜️"
    return "📎"
