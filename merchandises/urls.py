from django.urls import include, path
from .views import MerchandiseViewSet
from rest_framework.routers import SimpleRouter

app_name = "merchandises"

router = SimpleRouter()
router.register("", MerchandiseViewSet, basename="merchandises")

urlpatterns = [
    path("", include((router.urls))),
]
