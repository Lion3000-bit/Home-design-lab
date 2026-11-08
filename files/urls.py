from django.urls import path

from . import views

app_name = "files"

urlpatterns = [
    path("", views.FileListView.as_view(), name="list"),
    path("folder/create/", views.CreateFolderView.as_view(), name="create_folder"),
    path("folder/<int:folder_id>/", views.FileListView.as_view(), name="folder"),
    path("folder/<int:pk>/delete/", views.FolderDeleteView.as_view(), name="delete_folder"),
    path("view/<int:pk>/", views.FileView.as_view(), name="view"),
    path("<int:pk>/move/", views.MoveFileView.as_view(), name="move"),
    path("<int:pk>/delete/", views.FileDeleteView.as_view(), name="delete"),
    path("<int:pk>/download/", views.FileDownloadView.as_view(), name="download"),
]
