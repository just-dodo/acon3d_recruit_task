from .models import Merchandise, MerchContent
from rest_framework import viewsets

from .serializers import MerchandiseSerializer 


class MerchandiseViewSet(viewsets.ModelViewSet):
    serializer_class = MerchandiseSerializer
    queryset = Merchandise.objects.all()