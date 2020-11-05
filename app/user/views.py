from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from user.serializers import UserSerializer
from core.models import User


class RetrieveUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_class = (IsAuthenticated,)


class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
