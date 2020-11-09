from rest_framework import generics

from school.serializers import CategorySerializer


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer
