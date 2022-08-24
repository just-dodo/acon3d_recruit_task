from django.urls import include, path
from .views import UserViewSet
from rest_framework.routers import SimpleRouter

app_name = "users"

router = SimpleRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = [
    path("", include((router.urls))),
]
