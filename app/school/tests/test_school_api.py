from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category, School
from school.serializers import CategorySerializer


create_school_url = reverse('school:create')
list_school_url = reverse('school:list')

reg_url = '/api/v1/accounts/auth/registration/'


def sample_category(basename="pre-school", name="Pre School"):
    return Category.objects.create(
        basename=basename,
        name=name
    )


def sample_user():
    return get_user_model().objects.create(
        username="testuser01",
        email="testuser@bondeveloper.coom",
        password="Qwerty!@#",
    )


def sample_school():
    cat = Category.objects.create(
                basename="pre-school",
                name="Pre School"
            )

    user1 = get_user_model().objects.create_user(
        username="testuser0bc",
        email="testuser02cb@bondeveloper.coom",
        password="Qwerty!@#",
        first_name="Test F",
        last_name="Test L"
    )

    School.objects.create(
        basename="bbg",
        name="Beitbridge Gvt",
        category=cat,
    ).users.add(user1)


class TestPublicSchoolApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_school_create_successful(self):
        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        payload = {
            "basename": "test-school",
            "name": "Test School",
            "category": CategorySerializer(cat).data.get('id'),
            "users": [{
                "username": "testuser01",
                "email": "testuser@bondeveloper.coom",
                "password": "Qwerty!@#",
                "first_name": "Test User Firstname",
                "last_name": "Test User Lastname"
            }]
        }
        res = self.client.post(create_school_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("users", res.data.keys())
        self.assertTrue(len(res.data.get("users")) == 1)
        self.assertIn("id", res.data.get("users")[0].keys())

    def test_add_admin_user_to_school(self):
        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        payload = {
            "basename": "test-school",
            "name": "Test School",
            "category": CategorySerializer(cat).data.get('id'),
            "users": []
        }

        with self.assertRaises(ValueError):
            self.client.post(create_school_url, payload, format='json')

    def test_create_school_basename_required(self):

        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        payload = {
            "basename": "test-school",
            "name": "",
            "category": CategorySerializer(cat).data.get('id'),
            "users": [{
                "username": "testuser01",
                "email": "testuser@bondeveloper.coom",
                "password": "Qwerty!@#",
                "first_name": "Test User Firstname",
                "last_name": "Test User Lastname"
            }]
        }

        res = self.client.post(create_school_url, payload, format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_school_name_required(self):

        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        payload = {
            "basename": "test-school",
            "category": CategorySerializer(cat).data.get('id'),
            "users": [{
                "username": "testuser01",
                "email": "testuser@bondeveloper.coom",
                "password": "Qwerty!@#",
                "first_name": "Test User Firstname",
                "last_name": "Test User Lastname"
            }]
        }

        res = self.client.post(create_school_url, payload, format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)


class TestPrivateSchoolApi(TestCase):
    def setUp(self):
        self.client = APIClient()

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwerty!@#",
            "password1": "Qwerty!@#",
            "password2": "Qwerty!@#",
            "username": "testuser01"
        }

        auth_user = self.client.post(reg_url, payload, format='json')

        access_token = auth_user.data.get('access_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    def test_authentication_required(self):
        self.client = APIClient()
        res = self.client.get(list_school_url)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_schools(self):
        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        user1 = get_user_model().objects.create(
            username="testuser02",
            email="testuser02@bondeveloper.coom",
            password="Qwerty!@#",
        )

        School.objects.create(
            basename="bbg",
            name="Beitbridge Gvt",
            category=cat,
        ).users.add(user1)

        user2 = get_user_model().objects.create(
            username="testuser03",
            email="testuser03@bondeveloper.coom",
            password="Qwerty!@#",
        )
        School.objects.create(
            basename="mckeurtan",
            name="Mckeurtan",
            category=cat,
        ).users.add(user2)

        res = self.client.get(list_school_url)
        self.assertEquals(res.status_code, status.HTTP_200_OK)

        self.assertEquals(len(res.data), 2)

    def test_update_school(self):
        cat = Category.objects.create(
                    basename="pre-school",
                    name="Pre School"
                )

        user1 = get_user_model().objects.create_user(
            username="testuser0bc",
            email="testuser02cb@bondeveloper.coom",
            password="Qwerty!@#",
            first_name="Test F",
            last_name="Test L"
        )

        school = School.objects.create(
            basename="bbg",
            name="Beitbridge Gvt",
            category=cat,
        ).users.add(user1)

        school = self.client.get(list_school_url).data[0]
        school.name = "BB Gov"
        school.get('users')[0].pop("email")

        res = self.client.patch(
                                reverse('school:update',
                                        args=[school.get('id')]
                                        ),
                                school, format='json'
                              )

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(str(res.data.get("name")), "Beitbridge Gvt")

    def test_school_delete_successful(self):
        sample_school()

        school_res = self.client.get(list_school_url)
        self.assertEquals(school_res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(school_res.data), 1)

        res = self.client.delete(reverse('school:delete',
                                         args=[school_res.data[0].get('id')]
                                         )
                                 )
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

        school_res = self.client.get(list_school_url)
        self.assertEquals(school_res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(school_res.data), 0)

    def test_retrieve_school_successful(self):
        sample_school()

        school_res = self.client.get(list_school_url)
        self.assertEquals(school_res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(school_res.data), 1)

        res = self.client.get(reverse('school:view',
                                      args=[school_res.data[0].get('id')]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get("basename"), "bbg")
