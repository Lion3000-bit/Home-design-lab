from django.urls import path

from . import views

app_name = "files"

urlpatterns = [
    path("", views.FileListView.as_view(), name="list"),
    path("public/", views.PublicFilesView.as_view(), name="public"),
    path("<int:pk>/delete/", views.FileDeleteView.as_view(), name="delete"),
    path("<int:pk>/download/", views.FileDownloadView.as_view(), name="download"),
]
