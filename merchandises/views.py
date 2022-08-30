from .models import Merchandise, MerchContent
from rest_framework import viewsets

from .serializers import (
    MerchContentSerializer,
    MerchandiseSerializer,
    PurchaseSerializer,
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


class MerchandiseViewSet(viewsets.GenericViewSet):
    serializer_class = MerchandiseSerializer
    queryset = Merchandise.objects.all()

    def get_permissions(self):
        permission_list = ()
        if self.action in ("create", "update", "delete"):
            return (IsAuthenticated(), DjangoModelPermissionsOrAnonReadOnly())
        return (AllowAny(),)

    def get_queryset(self):

        merch_kwargs = {}
        if (
            self.request.user.is_anonymous
            or not self.request.user.groups.filter(name="Editors").exists()
        ):
            merch_kwargs["is_reviewed"] = True

        query_params = self.request.query_params.dict()
        contents_kwargs = {}
        language = query_params.pop("language", "")

        if language:
            contents_kwargs["language"] = language
        merch_kwargs.update(query_params)

        queryset = Merchandise.objects.filter(
            deleted_at__isnull=True, **merch_kwargs
        ).prefetch_related(
            Prefetch(
                "contents",
                queryset=MerchContent.objects.filter(
                    deleted_at__isnull=True, **contents_kwargs
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
