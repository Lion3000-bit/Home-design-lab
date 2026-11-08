import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.test import Client

c = Client()
r = c.get("/accounts/login/")
print("LOGIN_PAGE", r.status_code)
r = c.post("/accounts/login/", {"username": "admin@example.com", "password": "admin12345"}, follow=True)
print("LOGIN_POST", r.status_code, r.resolver_match.view_name if r.resolver_match else None)
r = c.get("/dashboard/")
print("DASHBOARD", r.status_code)
r = c.get("/files/")
print("FILES", r.status_code)
r = c.get("/")
print("HOME", r.status_code)
r = c.get("/admin/login/")
print("ADMIN_LOGIN", r.status_code)
r = c.get("/accounts/profile/")
print("PROFILE_ANON", r.status_code)
r = c.get("/accounts/register/")
print("REGISTER", r.status_code)
r = c.post(
    "/accounts/register/",
    {"username": "smokeuser", "email": "smoke@example.com", "password1": "SmokePass123", "password2": "SmokePass123"},
)
print("REGISTER_POST", r.status_code)
from django.contrib.auth import get_user_model

User = get_user_model()
u = User.objects.filter(email="smoke@example.com").first()
print("SMOKE_USER", u)
if u:
    u.delete()
