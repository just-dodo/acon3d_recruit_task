from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent
from rest_framework import serializers


class ContentsField(serializers.Field):
    def get_attribute(self, merchendise):
        contents_queryset = []
        print(merchendise)
        if hasattr(merchendise, "merchandise_contents"):
            contents_queryset = merchendise.merchandise_contents
        elif merchendise.contents.exists():
            contents_queryset = merchendise.contents
        return contents_queryset

    def to_representation(self, value):
        return MerchContentSerializer(value, many=True).data

    def to_internal_value(self, data):
        content_serializer = MerchContentSerializer(data=data, many=True)
        content_serializer.is_valid(raise_exception=True)

        return content_serializer.data


class MerchandiseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(allow_null=True)
    contents = ContentsField()

    class Meta:
        model = Merchandise
        fields = "__all__"

    def get_author(self, merchendise):
        return AbstractUserSerializer(merchendise.author).data

    def save(self, **kwargs):

        contents_data = self.validated_data.pop("contents")
        print(contents_data)
        merchandise = super().save(**kwargs)

        for content_data in contents_data:
            # content_data = dict(content_data)
            # print(content_data)
            language = content_data.get("language")
            content, created = MerchContent.objects.get_or_create(
                merchendise=merchandise, language=language
            )

            content_serializer = MerchContentSerializer(content, data=content_data)
            content_serializer.is_valid(raise_exception=True)
            content_serializer.save(merchendise=merchandise)

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
