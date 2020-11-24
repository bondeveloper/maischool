from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name',
                  'email', 'password')
        read_only_fields = ('id',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("************")

    def update(self, instance, validated_data):
        validated_data.pop('email', None)
        return super().update(instance, validated_data)
