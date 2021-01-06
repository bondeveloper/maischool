from rest_framework import generics
from rest_framework.permissions import AllowAny

import school.serializers as CustomSerializers
from core.models import Category, School, Subject, Level, Lesson, Session, \
                       Attachment,  Moderation


class CategoryCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.CategorySerializer


class CategoryUpdateAPIView(generics.UpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CustomSerializers.CategorySerializer


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CustomSerializers.CategorySerializer

class CategoryPublicListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CustomSerializers.CategoryPublicSerializer
    permission_classes = (AllowAny,)


class CategoryDestroyAPIView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CustomSerializers.CategorySerializer


class CategoryRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CustomSerializers.CategorySerializer


class SchoolCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.SchoolSerializer
    permission_classes = (AllowAny,)


class SchoolListAPIView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = CustomSerializers.SchoolSerializer


class SchoolPublicListAPIView(generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = CustomSerializers.SchoolPublicSerializer
    permission_classes = (AllowAny,)


class SchoolUpdateAPIView(generics.UpdateAPIView):
    queryset = School.objects.all()
    serializer_class = CustomSerializers.SchoolSerializer


class SchoolDeleteAPIView(generics.DestroyAPIView):
    queryset = School.objects.all()
    serializer_class = CustomSerializers.SchoolSerializer


class SchoolRetrieveAPIView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = CustomSerializers.SchoolSerializer


class SubjectCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.SubjectSerializer


class SubjectListAPIView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = CustomSerializers.SubjectSerializer


class SubjectRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = CustomSerializers.SubjectSerializer


class SubjectUpdateAPIView(generics.UpdateAPIView):
    queryset = Subject.objects.all()
    serializer_class = CustomSerializers.SubjectSerializer


class SubjectDestroyAPIView(generics.DestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = CustomSerializers.SubjectSerializer


class LevelCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.LevelSerializer


class LevelUpdateAPIView(generics.UpdateAPIView):
    queryset = Level.objects.all()
    serializer_class = CustomSerializers.LevelSerializer


class LevelListAPIView(generics.ListAPIView):
    queryset = Level.objects.all()
    serializer_class = CustomSerializers.LevelSerializer


class LevelDestroyAPIView(generics.DestroyAPIView):
    queryset = Level.objects.all()
    serializer_class = CustomSerializers.LevelSerializer


class LevelRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Level.objects.all()
    serializer_class = CustomSerializers.LevelSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.LessonSerializer


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CustomSerializers.LessonSerializer


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CustomSerializers.LessonSerializer


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CustomSerializers.LessonSerializer


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = CustomSerializers.LessonSerializer


class SessionListAPIView(generics.ListAPIView):
    queryset = Session.objects.all()
    serializer_class = CustomSerializers.SessionSerializer


class SessionCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.SessionSerializer


class SessionUpdateAPIView(generics.UpdateAPIView):
    queryset = Session.objects.all()
    serializer_class = CustomSerializers.SessionSerializer


class SessionDestroyAPIView(generics.DestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = CustomSerializers.SessionSerializer


class SessionRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Session.objects.all()
    serializer_class = CustomSerializers.SessionSerializer


class AttachmentListAPIView(generics.ListAPIView):
    queryset = Attachment.objects.all()
    serializer_class = CustomSerializers.AttachmentSerializer


class AttachmentCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.AttachmentSerializer


class AttachmentUpdateAPIView(generics.UpdateAPIView):
    queryset = Attachment.objects.all()
    serializer_class = CustomSerializers.AttachmentSerializer


class AttachmentDestroyAPIView(generics.DestroyAPIView):
    queryset = Attachment.objects.all()
    serializer_class = CustomSerializers.AttachmentSerializer


class AttachmentRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Attachment.objects.all()
    serializer_class = CustomSerializers.AttachmentSerializer


class ModerationListAPIView(generics.ListAPIView):
    queryset = Moderation.objects.all()
    serializer_class = CustomSerializers.ModerationSerializer


class ModerationCreateAPIView(generics.CreateAPIView):
    serializer_class = CustomSerializers.ModerationSerializer


class ModerationUpdateAPIView(generics.UpdateAPIView):
    queryset = Moderation.objects.all()
    serializer_class = CustomSerializers.ModerationSerializer


class ModerationDestroyAPIView(generics.DestroyAPIView):
    queryset = Moderation.objects.all()
    serializer_class = CustomSerializers.ModerationSerializer


class ModerationRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Moderation.objects.all()
    serializer_class = CustomSerializers.ModerationSerializer
