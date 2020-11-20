from rest_framework import generics
from rest_framework.permissions import AllowAny

from school.serializers import CategorySerializer, SchoolSerializer
from core.models import Category, School


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer


class UpdateCategoryView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ListCategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DestroyCategoryView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ViewCategoryView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CreateSchoolView(generics.CreateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (AllowAny,)


class ListSchoolView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer

class UpdateSchoolView(generics.UpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
#
# class RetrieveSchoolView(generics.RetrieveAPIView):
#     # queryset = School.objects.all()
#     serializer_class = SchoolSerializer
#     permission_classes = (AllowAny,)
#


# class CreateSchoolUserView(generics.CreateAPIView):
#     queryset = School.objects.all()
#     serializer_class = SchoolSerializer
#     permission_classes = (AllowAny,)
