from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category
from school.serializers import CategorySerializer


category_create_url = reverse('school:category-create')
category_list_url = reverse('school:category-list')
category_payload = {"basename": "primary-school",
                    "displayname": "Primary School"}

# if anyones knows how to reverse this path, feel free to make edits
reg_url = '/api/accounts/auth/registration/'
login_url = '/api/accounts/auth/login/'

def sample_category(basename="primary-school", displayname="Primary School"):
    return Category.objects.create(
        basename=basename,
        displayname=displayname
    )

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
        self.assertIn('displayname', res.data.keys())
        self.assertEquals(str(res.data.get('displayname')[0]),
                          'This field may not be blank.')

    def test_update_category_basename_not_allowed(self):
        saved = sample_category()
        saved.basename = "test-update"
        sanitizer = CategorySerializer(saved)

        res = self.client.put(reverse('school:category-update',
                                      args=[sanitizer.data.get('id')]),
                              sanitizer.data, format='json')


        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertNotEquals(res.data, sanitizer.data)
        self.assertEquals(res.data.get('basename'), "primary-school")

    def test_update_displayname_successful(self):
        saved = sample_category()
        saved.displayname = "test-update display"
        sanitizer = CategorySerializer(saved)

        res = self.client.put(reverse('school:category-update',
                                      args=[sanitizer.data.get('id')]),
                              sanitizer.data, format='json')


        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, sanitizer.data)
        self.assertEquals(res.data.get('displayname'), "test-update display")

    def test_list_categories(self):
        sample_category()
        Category.objects.create(
            basename="college",
            displayname="College"
        )
        Category.objects.create(
            basename="university",
            displayname="University"
        )

        res = self.client.get(category_list_url)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data), 3)

    def test_remove_category(self):
        saved = sample_category()
        sanitizer = CategorySerializer(saved)

        Category.objects.create(
            basename="college",
            displayname="College"
        )

        res = self.client.delete(reverse('school:category-delete',
                                      args=[sanitizer.data.get('id')]),
                                 sanitizer.data, format='json')

        list = Category.objects.all()
        sanitizer = CategorySerializer(list, many=True)

        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(len(sanitizer.data), 1)

    def test_view_category(self):
        saved = sample_category()
        sanitizer = CategorySerializer(saved)

        res = self.client.get(reverse('school:category-view',
                                      args=[sanitizer.data.get('id')]),
                                 sanitizer.data, format='json')

        self.assertEquals(res.status_code, status.HTTP_200_OK)
