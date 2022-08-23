from django.urls import include, path
from merchandises.views import *
from rest_framework.routers import SimpleRouter

app_name = "merchandises"

router = SimpleRouter()

urlpatterns = [
    path("", include((router.urls))),
]
