
from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent
from rest_framework import serializers


class MerchandiseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(allow_null=True)
    contents = serializers.SerializerMethodField(allow_null=True)

    class Meta:
        model = Merchandise
        fields = (
            "name", "author", "released_at",
            "is_reviewed", "commission_rate", "contents")

    def get_author(self, merchendise):
        return AbstractUserSerializer(merchendise.author).data

    def get_contents(self, merchendise):
        if hasattr(merchendise, 'merchandise_contents'):
            return MerchContentSerializer(merchendise.merchandise_contents, many=True).data
        else:
            return []

    def create(self, validated_data):

        merchandise = super().create(validated_data=validated_data)
        author = validated_data.get("author", "")

        if author:
            merchandise.author = author
            merchandise.save()
        return merchandise


class MerchContentSerializer(serializers.ModelSerializer):
    merchandise = serializers.CharField(write_only=True)

    class Meta:
        model = MerchContent
        fields = (
            "language",
            "title",
            "body",
            "price",
        )
