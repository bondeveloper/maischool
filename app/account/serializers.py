from rest_framework import serializers

from core.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'created')
        read_only_fields = ('id',)
