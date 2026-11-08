from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("password/change/", views.ChangePasswordView.as_view(), name="password_change"),
    path("links/", views.LinkListView.as_view(), name="links"),
    path("links/<int:pk>/delete/", views.LinkDeleteView.as_view(), name="link_delete"),
]
