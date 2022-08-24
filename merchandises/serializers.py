from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent
from rest_framework import serializers


class MerchandiseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(allow_null=True)
    contents = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Merchandise
        fields = ("name", "author","released_at", "is_reviewed", "commission_rate", "contents")

    def get_author(self, merchendise):
        return AbstractUserSerializer(merchendise.author).data

    def get_contents(self, merchendise):
        return MerchContentSerializer(merchendise.contents, many=True).data


class MerchContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchContent
        fields = (
            "language",
            "title",
            "body",
            "price",
        )
