from django.shortcuts import render
from django.db import transaction
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group

from users.models import *
from users.serializers import UserSerializer


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated(),)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in (
            "create",
            "login",
        ):
            return (AllowAny(),)
        return self.permission_classes

    @transaction.atomic
    @action(detail=False, methods=["POST"], permission_classes=(AllowAny(),))
    def login(self, request):
        if request.method == "POST":
            username = request.data.get("username", "")
            password = request.data.get("password", "")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                return Response({"Token": token.key})
            else:
                return Response(
                    {"error": "Invalid Account or Wrong Password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        elif request.method == "PUT":
            data = request.data
            user = request.user
            if user.is_authenticated:
                serializer = self.get_serializer(
                    user, data=data, partial=True, context={"row_data": data}
                )
                serializer.is_valid(raise_exception=True)
                user = serializer.save()

                data = self.get_serializer(user).data
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Not Authorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        data = self.get_serializer(user).data
        token = Token.objects.create(user=user)
        data["token"] = token.key
        return Response(data)

    @transaction.atomic
    def update(self, request, pk=None):
        user = request.user
        print(user)
        data = request.data

        if pk != "me":
            return Response(
                {"error": "You are not allowed to change information"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = self.get_serializer(user).data
        return Response(data)

    @transaction.atomic
    def retrieve(self, request, pk=None):
        if pk == "me":
            user = request.user
        elif User.objects.filter(pk=pk).exists():
            user = User.objects.get(pk=pk)
        else:
            return Response(
                {"error": "There is no user with the id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(self.get_serializer(user).data)

    @transaction.atomic
    def list(self, request):
        username = request.query_params.get("username", "")
        if username:
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
            else:
                return Response(
                    {"error": "There is no user with the username"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"error": "Username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(self.get_serializer(user).data)
