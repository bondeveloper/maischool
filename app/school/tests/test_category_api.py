from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category
from school.serializers import CategorySerializer


CATEGORY_CREATE_URL = reverse('school:category-create')
CATEGORY_PAYLOAD = {"basename": "primary-school",
                    "displayname": "Primary School"}


class PrivateCategoryTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_category(self):
        res = self.client.post(CATEGORY_CREATE_URL, CATEGORY_PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        category = Category.objects.get(pk=1)
        category = CategorySerializer(category)

        self.assertEqual(res.data, category.data)

    def test_category_basename_required(self):
        payload = {"basename": '',
                   "displayname": "Primary School"}

        res = self.client.post(CATEGORY_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_displayname_required(self):
        payload = {"basename": 'primary-school',
                   "displayname": ""}

        res = self.client.post(CATEGORY_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_categories_create_requires_authentication(self):

        res = self.client.post(CATEGORY_CREATE_URL, CATEGORY_PAYLOAD)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_update_category(self):
    #     category = sample_category()
    #
    #     to_update = Category.objects.get(pk=1)
    #
    #     # updated = CategorySerializer(to_update)
    #
    #     self.assertEqual(toUpdate.basename, category.basename)
    #     self.assertEqual(toUpdate.displayname, category.displayname)
    #
    #     toUpdate.basename = "primary-sch"
    #     toUpdate.save()
    #
    #     updated = Category.objects.get(pk=1)
    #
    #     self.assertEqual(updated.basename, category.basename)
