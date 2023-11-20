from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout, authenticate

from users.models import User
from .serializers import (UserCreateSerializer, UserSerializer,
                          UserLoginSerializer)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


user_create = UserCreateAPIView.as_view()


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


user_list = UserListAPIView.as_view()


class UserLoginAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request: Request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                request,
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
            if user is not None:
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'User not found!'},
                                status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


user_login = UserLoginAPIView.as_view()


class UserLogoutAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return Response({'message': 'Logged out successfully!'})


user_logout = UserLogoutAPIView.as_view()
