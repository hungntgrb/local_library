from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny

from users.models import User
from .serializers import UserCreateSerializer, UserSerializer


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
