from rest_framework import serializers

from django.contrib.auth import get_user_model

from core.models import Category, School, Subject
from user.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'basename', 'displayname')
        read_only_fields = ('id',)

    def update(self, instance, validated_data):
        validated_data.pop('basename', None)
        return super().update(instance, validated_data)


class SchoolSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = School
        fields = ('id', 'basename', 'name', 'category', 'users')
        read_only_fields = ('id',)
        ordering = ('basename',)
        extra_kwargs = {'users': {'write_only': True}}

    def create_or_update_users(self, users):
        user_ids = []
        for user in users:
            user_instance, created = get_user_model().objects.update_or_create(
                    pk=user.get('id'),
                    defaults=user
                    )
            user_ids.append(user_instance.pk)
        return user_ids

    def create(self, validated_data):

        """on create, there can only ever be one user"""
        users_data = validated_data.pop("users")
        if users_data is None or len(users_data) < 1:
            raise ValueError("School user is required")

        user_data = users_data[0]
        email = user_data.pop("email")
        password = user_data.pop("password")

        school = School.objects.create(**validated_data)
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
            **user_data
        )
        school.users.add(user)
        return school

    def update(self, instance, validated_data):

        validated_data.pop('users')
        return super().update(instance, validated_data)


class SubjectSerializer(serializers.ModelSerializer):
    school = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'basename', 'name', 'school')
        read_only_fields = ('id',)
