from rest_framework import generics
from rest_framework.permissions import AllowAny

from school.serializers import CategorySerializer, SchoolSerializer, \
                                SubjectSerializer
from core.models import Category, School, Subject


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


class DeleteSchoolView(generics.DestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class RetrieveSchoolAPIView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class CreateSubjectAPIView(generics.CreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
