from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.DashboardHomeView.as_view(), name="home"),
    path("users/", views.DashboardUsersView.as_view(), name="users"),
    path("settings/", views.DashboardSettingsView.as_view(), name="settings"),
    path("users/<str:action>/<int:pk>/", views.DashboardUserActionView.as_view(), name="user_action"),
]
