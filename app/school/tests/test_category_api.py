from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category
from school.serializers import CategorySerializer


category_create_url = reverse('school:category-create')
category_payload = {"basename": "primary-school",
                    "displayname": "Primary School"}

# if anyones knows how to reverse this path, feel free to make edits
reg_url = '/api/accounts/auth/registration/'
login_url = '/api/accounts/auth/login/'


class PrivateCategoryTestApi(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwerty!@#",
            "password1": "Qwerty!@#",
            "password2": "Qwerty!@#",
            "username": "testuser01"
        }

        self.client.post(reg_url, payload, format='json')

        auth_user = self.client.post(login_url, payload, format='json')
        access_token = auth_user.data.get('access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_categories_create_requires_authentication(self):
        self.client = APIClient()
        res = self.client.post(category_create_url, category_payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', res.data.keys())
        self.assertEquals(res.data.get('detail'),
                          'Authentication credentials were not provided.')

    def test_create_category_successful(self):
        res = self.client.post(category_create_url, category_payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        category = Category.objects.all()[0]
        category = CategorySerializer(category)

        self.assertEqual(res.data, category.data)

    def test_category_basename_required(self):
        payload = {"basename": '',
                   "displayname": "Primary School"}

        res = self.client.post(category_create_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('basename', res.data.keys())
        self.assertEquals(str(res.data.get('basename')[0]),
                          'This field may not be blank.')

    def test_category_basename_unique(self):
        Category.objects.create(
            basename=category_payload.get('basename'),
            displayname=category_payload.get('displayname'),
        )

        res = self.client.post(category_create_url, category_payload,
                               format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('basename', res.data.keys())
        self.assertEquals(str(res.data.get('basename')[0]),
                          'category with this basename already exists.')

    def test_category_displayname_required(self):
        payload = {"basename": 'primary-school',
                   "displayname": ""}

        res = self.client.post(category_create_url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_update_category_basename_not_allowed(self):
    #     saved = sample_category()
    #
    #     saved.basename = "primary-sch"
    #     saved.save()
    #     saved = CategorySerializer(saved).data
    #
    #     updated = Category.objects.all()[0]
    #     updated = CategorySerializer(saved).data
    #     print(updated)
    #     print(saved)
    #
    #     self.assertNotEquals(updated.get('basename'), saved.get('basename'))
