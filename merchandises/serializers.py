from functools import partial
from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent, Purchase
from rest_framework import serializers
from django.db.utils import IntegrityError
from django.http import HttpResponseBadRequest
from rest_framework.fields import empty


class ContentsField(serializers.Field):
    def get_attribute(self, merchandise):
        contents_queryset = []
        if hasattr(merchandise, "merchandise_contents"):
            contents_queryset = merchandise.merchandise_contents
        elif merchandise.contents.exists():
            contents_queryset = merchandise.contents
        return contents_queryset

    def to_representation(self, value):

        return MerchContentSerializer(value, many=True).data

    def to_internal_value(self, data):
        return data


class MerchandiseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(allow_null=True)
    contents = ContentsField()

    class Meta:
        model = Merchandise
        fields = "__all__"

    def get_author(self, merchandise):
        return AbstractUserSerializer(merchandise.author).data

    def validate_is_submitted(self, value):
        user = self.context["request"].user
        if self.instance:
            if self.instance.author != user:
                raise serializers.ValidationError("Not allowed to change is_submitted")
        return value

    def validate_is_reviewed(self, value):
        return self.is_editor(value)

    def validate_commission_rate(self, value):
        return self.is_editor(value)

    def is_editor(self, value):
        user = self.context["request"].user
        if not user.groups.filter(name="Editors").exists():
            raise serializers.ValidationError(
                "Only editors are allowed to change this value."
            )

        return value

    def save(self, **kwargs):

        contents_data = self.validated_data.pop("contents")
        merchandise = super().save(**kwargs)

        for content_data in contents_data:
            # content_data = dict(content_data)
            # print(content_data)
            language = content_data.get("language")

            if MerchContent.objects.filter(
                merchandise=merchandise, language=language
            ).exists():
                content = MerchContent.objects.get(
                    merchandise=merchandise, language=language
                )
                content_serializer = MerchContentSerializer(
                    content, data=content_data, partial=True
                )
            else:
                content_serializer = MerchContentSerializer(data=content_data)
            content_serializer.is_valid(raise_exception=True)
            content_serializer.save(merchandise=merchandise)

        return merchandise


class MerchContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchContent
        fields = (
            "language",
            "title",
            "body",
            "price",
        )


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"

    def validate_user(self, user):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")
        return user

    def create(self, validated_data, **kwargs):
        try:
            return super().create(validated_data, **kwargs)
        except IntegrityError:
            raise serializers.ValidationError("You already have bought it.")

    def __init__(self, instance=None, data=empty, *args, **kwargs):

        merchandise = kwargs["context"]["merchandise"]
        merchandise_content = merchandise.merchandise_contents[0]
        merchandise_content_data = MerchContentSerializer(merchandise_content).data

        if data is not empty:
            data.update(merchandise_content_data)
        else:
            data = merchandise_content_data

        super().__init__(instance=instance, data=data, *args, **kwargs)


class MerchFilterSerializer(serializers.Serializer):
    class Meta:
        fields = ("author", "released_at", "is_submitted", "is_reviewed")

    def validate_is_reviewed(self, value):
        user = self.context["request"].user
        if user.is_anonymous or not user.groups.filter(name="Editors").exists():
            return True
        else:
            return False

    def validate_user(self, user):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")
        return user
class MerchContentFilterSerializer(serializers.Serializer):
    class Meta:
        fields = ("title", "language", "body", "price")

    def validate_is_reviewed(self, value):
        user = self.context["request"].user
        if user.is_anonymous or not user.groups.filter(name="Editors").exists():
            return True
        else:
            return False

    def validate_user(self, user):
        user = self.context["request"].user
        if not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")
        return user
