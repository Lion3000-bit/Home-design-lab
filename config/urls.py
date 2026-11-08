from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("files/", include("files.urls")),
    path("dashboard/", include("dashboard.urls")),
    path("chat/", include("chat.urls")),
    path("", include("pages.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "pages.views.error_404"
handler500 = "pages.views.error_500"
handler403 = "pages.views.error_403"
