from .models import Merchandise, MerchContent
from rest_framework import viewsets

from .serializers import (
    MerchContentSerializer,
    MerchandiseSerializer,
    PurchaseSerializer,
    MerchFilterSerializer,
    MerchContentFilterSerializer
)
from django.http import (
    response,
    HttpResponseNotFound,
    HttpResponseForbidden,
    HttpResponseBadRequest,
)
from django.db.models import query, Prefetch, Q

from django.db import transaction

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    DjangoModelPermissionsOrAnonReadOnly,
)
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class MerchandiseViewSet(viewsets.GenericViewSet):
    serializer_class = MerchandiseSerializer
    queryset = Merchandise.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']

    def get_permissions(self):
        permission_list = ()
        if self.action in ("create", "update", "delete"):
            return (IsAuthenticated(), DjangoModelPermissionsOrAnonReadOnly())
        return (AllowAny(),)

    def get_queryset(self):

        query_params = self.request.query_params.dict()

        # Query params to Merchandise filter kwargs
        merch_filter_serializer = MerchFilterSerializer(
            data=query_params, partial=True, constext={"request": self.request}
        )
        merch_filter_serializer.is_valid(raise_exception=True)
        merch_filter_kwargs = merch_filter_serializer.data
        merch_filter_kwargs = {}

        # Query params to MerchContent filter kwargs
        merch_content_filter_serializer = MerchContentFilterSerializer(
            data=query_params, partial=True, constext={"request": self.request}
        )
        merch_content_filter_serializer.is_valid(raise_exception=True)
        merch_content_filter_kwargs = merch_content_filter_serializer.data
        merch_content_filter_kwargs = {}

        queryset = Merchandise.objects.filter(
            deleted_at__isnull=True, **merch_filter_kwargs
        ).prefetch_related(
            Prefetch(
                "contents",
                queryset=MerchContent.objects.filter(
                    deleted_at__isnull=True, **merch_content_filter_kwargs
                ),
                to_attr="merchandise_contents",
            )
        )
        return queryset

    @transaction.atomic
    def create(self, request):
        user = request.user
        data = request.data

        serializer = self.get_serializer_class()(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        merchandise = serializer.save(author=user)

        image = request.FILES.get("image", None)
        if image:
            merchandise.image = image
            merchandise.save()

        file = request.FILES.get("file", None)
        if file:
            merchandise.file = file
            merchandise.save()

        data = self.get_serializer_class()(merchandise).data

        return Response(data)

    @transaction.atomic
    def update(self, request, pk):
        user = request.user
        data = request.data
        try:
            merchandise = Merchandise.objects.get(pk=pk)
        except Merchandise.DoesNotExist:
            return HttpResponseNotFound("The merchandise does not exist")

        if (
            merchandise.author != user
            and not user.groups.filter(name="Editors").exists()
        ):
            return HttpResponseForbidden(
                "You are neither the author of this merchandise nor a editor"
            )

        serializer = self.get_serializer_class()(
            merchandise, data=data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        merchandise = serializer.save()

        image = request.FILES.get("image", None)
        if image:
            merchandise.image = image
            merchandise.save()

        data = self.get_serializer_class()(merchandise).data
        return Response(data)

    def retrieve(self, requset, pk):
        try:
            merchandise = Merchandise.objects.get(pk=pk)
        except Merchandise.DoesNotExist:
            raise HttpResponseNotFound("Merchandise does not exist")

        serializer = self.get_serializer_class()(merchandise)
        data = serializer.data
        return Response(data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        data = serializer.data
        return Response(data)

    @action(detail=True, methods=["POST"])
    def purchase(self, request, pk):
        user = request.user
        queryset = self.get_queryset()

        try:
            print(pk)
            merchandise = queryset.get(pk=pk)
        except Merchandise.DoesNotExist:
            return HttpResponseNotFound("The merchandise does not exist")

        if merchandise.author == user:
            return HttpResponseBadRequest(
                "You cannot buy your merchandise for yourself."
            )

        serialize_data = {
            "merchandise": merchandise.id,
            "user": user.id,
        }

        serializer = PurchaseSerializer(
            data=serialize_data,
            partial=True,
            context={"request": request, "merchandise": merchandise},
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
