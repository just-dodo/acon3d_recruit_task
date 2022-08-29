from functools import partial
from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent
from rest_framework import serializers


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

    def save(self, **kwargs):

        contents_data = self.validated_data.pop("contents")
        merchandise = super().save(**kwargs)

        for content_data in contents_data:
            # content_data = dict(content_data)
            # print(content_data)
            language = content_data.get("language")
            content, created = MerchContent.objects.get_or_create(
                merchandise=merchandise, language=language
                )
                content_serializer = MerchContentSerializer(content, data=content_data, partial=True)
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
