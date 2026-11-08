import shutil

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from pages.models import SiteSettings

from .models import Folder, StoredFile

TEXT_EXTENSIONS = {
    ".txt", ".md", ".log", ".csv", ".json", ".xml", ".html", ".htm",
    ".css", ".js", ".py", ".ini", ".yaml", ".yml", ".toml",
}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mov", ".avi", ".mkv"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac", ".wma"}


def _extension(name):
    name = (name or "").lower()
    return name[name.rfind("."):] if "." in name else ""


def _human_size(size):
    size = int(size or 0)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if abs(size) < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} ТБ"


def _get_disk_usage():
    try:
        _, _, free = shutil.disk_usage(settings.MEDIA_ROOT)
        return free
    except OSError:
        return 0


class FileListView(LoginRequiredMixin, View):
    """Главная страница файлов — общая файловая система (корень или папка).
    Поддерживает загрузку файлов (POST) и создание папок.
    """

    def get(self, request, folder_id=None):
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id)
            breadcrumbs = folder.get_breadcrumbs()
            files = (
                StoredFile.objects.select_related("user")
                .filter(folder=folder)
                .order_by("-uploaded_at")
            )
            subfolders = (
                Folder.objects.select_related("user")
                .filter(parent=folder)
                .order_by("name")
            )
        else:
            folder = None
            breadcrumbs = []
            files = (
                StoredFile.objects.select_related("user", "folder")
                .filter(folder__isnull=True)
                .order_by("-uploaded_at")
            )
            subfolders = (
                Folder.objects.select_related("user")
                .filter(parent__isnull=True)
                .order_by("user__email", "name")
            )

        all_folders = Folder.objects.select_related("user").order_by("name")

        usage = (
            StoredFile.objects.all()
            .aggregate(total_size=Sum("size"))["total_size"]
            or 0
        )
        storage_limit = _get_disk_usage()

        return render(request, "files/list.html", {
            "folder": folder,
            "breadcrumbs": breadcrumbs,
            "files": files,
            "subfolders": subfolders,
            "all_folders": all_folders,
            "site_settings": SiteSettings.load(),
            "current_folder": folder,
            "storage_used": usage,
            "storage_used_human": _human_size(usage),
            "storage_limit": storage_limit,
            "storage_limit_human": _human_size(storage_limit),
            "storage_percent": (
                min(100, int(usage * 100 / storage_limit)) if storage_limit else 0
            ),
        })

    def post(self, request, folder_id=None):
        """Загрузка файлов в корень или в указанную папку."""
        folder = None
        if folder_id:
            folder = get_object_or_404(Folder, id=folder_id)

        uploaded = request.FILES.getlist("files")
        if not uploaded:
            if folder:
                return redirect("files:folder", folder_id=folder.id)
            return redirect("files:list")

        for f in uploaded:
            StoredFile.objects.create(
                user=request.user,
                folder=folder,
                file=f,
                name=f.name,
                size=f.size,
                content_type=f.content_type or "application/octet-stream",
            )

        if folder:
            return redirect("files:folder", folder_id=folder.id)
        return redirect("files:list")


class CreateFolderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        name = (request.POST.get("name") or "").strip()
        parent_id = request.POST.get("parent_id") or None
        parent = None
        if parent_id:
            parent = get_object_or_404(Folder, id=parent_id)
        if not name:
            if parent:
                return redirect("files:folder", folder_id=parent.id)
            return redirect("files:list")
        Folder.objects.create(user=request.user, name=name, parent=parent)
        if parent:
            return redirect("files:folder", folder_id=parent.id)
        return redirect("files:list")


class FolderDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        folder = get_object_or_404(Folder, id=pk)
        # Только владелец или админ может удалять папку
        if folder.user != request.user and not request.user.is_staff:
            raise Http404
        parent_id = folder.parent_id
        folder.delete()  # дети удалятся каскадом, файлы получат folder=None
        next_url = request.POST.get("next") or ""
        if next_url:
            return redirect(next_url)
        if parent_id:
            return redirect("files:folder", folder_id=parent_id)
        return redirect("files:list")


class FileView(LoginRequiredMixin, View):
    """Прямой просмотр файла (изображение, видео, аудио, текст) или скачивание."""

    def get(self, request, pk):
        obj = get_object_or_404(StoredFile, id=pk)

        content_type = (obj.content_type or "").lower()
        ext = _extension(obj.name)

        mode = "download"
        if content_type.startswith("image/") or ext in IMAGE_EXTENSIONS:
            mode = "image"
        elif content_type.startswith("video/") or ext in VIDEO_EXTENSIONS:
            mode = "video"
        elif content_type.startswith("audio/") or ext in AUDIO_EXTENSIONS:
            mode = "audio"
        elif content_type.startswith("text/") or ext in TEXT_EXTENSIONS:
            mode = "text"

        if mode == "download":
            response = FileResponse(obj.file.open("rb"), as_attachment=True, filename=obj.name)
            response["Content-Type"] = content_type or "application/octet-stream"
            return response

        text_content = None
        if mode == "text":
            try:
                with obj.file.open("rb") as fh:
                    text_content = fh.read().decode("utf-8", errors="replace")
            except Exception:
                text_content = "[Не удалось прочитать файл как текст]"

        all_folders = Folder.objects.all().order_by("name")

        return render(request, "files/view.html", {
            "file": obj,
            "mode": mode,
            "text_content": text_content,
            "site_settings": SiteSettings.load(),
            "breadcrumbs": obj.folder.get_breadcrumbs() if obj.folder else [],
            "all_folders": all_folders,
        })


class FileDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        obj = get_object_or_404(StoredFile, id=pk)
        # Только владелец или админ может удалять файл
        if obj.user != request.user and not request.user.is_staff:
            raise Http404
        folder_id = obj.folder_id
        obj.delete()
        next_url = request.POST.get("next") or ""
        if next_url:
            return redirect(next_url)
        if folder_id:
            return redirect("files:folder", folder_id=folder_id)
        return redirect("files:list")


class FileDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        obj = get_object_or_404(StoredFile, id=pk)
        response = FileResponse(obj.file.open("rb"), as_attachment=True, filename=obj.name)
        return response


class MoveFileView(LoginRequiredMixin, View):
    """Переместить файл в папку или в корень."""

    def post(self, request, pk):
        obj = get_object_or_404(StoredFile, id=pk)
        if obj.user != request.user and not request.user.is_staff:
            raise Http404
        folder_id = request.POST.get("folder_id") or None
        if folder_id:
            obj.folder = get_object_or_404(Folder, id=folder_id)
        else:
            obj.folder = None
        obj.save(update_fields=["folder"])
        return redirect("files:list")
