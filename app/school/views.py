from rest_framework import generics
from rest_framework.permissions import AllowAny

from school.serializers import CategorySerializer, SchoolSerializer, \
                                SubjectSerializer, LevelSerializer, \
                                LessonSerializer
from core.models import Category, School, Subject, Level, Lesson


class CategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = CategorySerializer


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SchoolCreateAPIView(generics.CreateAPIView):
    serializer_class = SchoolSerializer
    permission_classes = (AllowAny,)


class SchoolListAPIView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolUpdateAPIView(generics.UpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolDeleteAPIView(generics.DestroyAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SchoolRetrieveAPIView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class SubjectCreateAPIView(generics.CreateAPIView):
    serializer_class = SubjectSerializer


class SubjectListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectUpdateAPIView(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class SubjectDestroyAPIView(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class LevelCreateAPIView(generics.CreateAPIView):
    serializer_class = LevelSerializer


class LevelUpdateAPIView(generics.UpdateAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelListAPIView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelDestroyAPIView(generics.DestroyAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LevelRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
