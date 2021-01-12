from rest_framework import serializers

from django.contrib.auth import get_user_model

from core.models import Category, School, Subject, Level, Lesson, Session, \
                        Attachment, Moderation
from user.serializers import UserSerializer

# from core.helpers import removeKey


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'basename', 'name')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        validated_data.pop('basename', None)
        return super().update(instance, validated_data)


class CategoryPublicSerializer(CategorySerializer):
     class Meta:
        model = Category
        fields = ('id', 'basename', 'name')
        read_only_fields = ('id',)


class SchoolSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = School
        fields = ('id', 'basename', 'name', 'category', 'users')
        read_only_fields = ('id',)
        ordering = ('basename',)
        extra_kwargs = {'users': {'write_only': True}}


    def create(self, validated_data):
  
        """on create, there can only ever be one user"""
        users_data = validated_data.pop("users")
        if users_data is None or len(users_data) < 1:
            raise ValueError("School user is required")

        school = School.objects.create(**validated_data)
        users = []

        for user_data in users_data:

            # user_data = users_data[0]
            email = user_data.pop("email")
            password = user_data.pop("password")
            user = get_user_model().objects.create_user(
                email=email,
                password=password,
                **user_data
            )

            users.append(user)
        
        school.users.add(*users)

        return school


    def update(self, instance, validated_data):

        validated_data.pop('users')
        return super().update(instance, validated_data)


class SchoolPublicSerializer(SchoolSerializer):
     class Meta:
        model = School
        fields = ('id', 'basename', 'name', 'category')
        read_only_fields = ('id',)
        ordering = ('basename',)


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ('id', 'basename', 'name', 'school')
        read_only_fields = ('id',)


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ('id', 'basename', 'name', 'school')
        read_only_fields = ('id',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'subject', 'level', 'learners', 'name')
        read_only_fields = ('id',)
        extra_kwargs = {'instructor': {'write_only': True}}

    def create(self, validated_data):
        user_id = None
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user and hasattr(request.user, 'id'):
            validated_data['instructor'] = request.user

        return super().create(validated_data)


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'start_time', 'end_time', 'type', 'attendance',
                  'lesson'
                  )
        read_only_fields = ('id',)


class AttachmentSerializer(serializers.ModelSerializer):
    file = serializers.FileField(max_length=None, allow_empty_file=False)

    class Meta:
        model = Attachment
        fields = ('id', 'session', 'notes', 'file')
        read_only_fields = ('id',)


class ModerationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Moderation
        fields = ('id', 'session', 'learner', 'learner_score', 'max_score',
                  'score_type'
                  )
        read_only_fields = ('id',)
