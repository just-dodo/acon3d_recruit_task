from django.urls import include, path
from users.views import *
from rest_framework.routers import SimpleRouter

app_name = "users"

router = SimpleRouter()

urlpatterns = [
    path("", include((router.urls))),
]
