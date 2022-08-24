from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from rest_framework import serializers

class AbstractUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.CharField(allow_null=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )

    def validate_password(self, value):
        return make_password(value)

class UserSerializer(AbstractUserSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "group",
        )

    def get_group(self, user):
        return GroupSerializer(user.groups,many=True).data

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "name",
            "permissions",
        )
