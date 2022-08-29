
from users.serializers import AbstractUserSerializer
from .models import Merchandise, MerchContent
from rest_framework import serializers


class ContentsField(serializers.Field):
    def get_attribute(self, merchendise):
        contents_queryset = []
        print(merchendise)
        if hasattr(merchendise, 'merchandise_contents'):
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
        fields = '__all__'

    def get_author(self, merchendise):
        return AbstractUserSerializer(merchendise.author).data

    def save(self, **kwargs):

        contents = self.validated_data.pop('contents')

        merchandise = super().save(**kwargs)

        content_serializer = MerchContentSerializer(data=contents, many=True)
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
