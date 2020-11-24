from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer as \
                                                  js_RegisterSerializer

from core.models import School


class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField()


class RegisterSerializer(js_RegisterSerializer):

    def save(self, request):

        if request.method == 'POST':
            request_copy = request.data.copy()
            schools_ids = []
            if 'schools' in request_copy.keys():
                schools_ids = request_copy.pop('schools')

            user = super().save(request)

            for id in schools_ids:
                School.objects.get(pk=id).users.add(user)

        return user
