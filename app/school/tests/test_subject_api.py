from django.test import TestCase
from django.urls import reverse
from django.contrib.auth  import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import School, Category
from school.serializers import SchoolSerializer

subject_create_url = reverse("school:subject-create")
subject_list_url = reverse("school:subject-list")

# if anyones knows how to reverse this path, feel free to make edits
reg_url = '/api/v1/accounts/auth/registration/'
login_url = '/api/v1/accounts/auth/login/'


def sample_school(basename="test-school", name="test school"):
    return School.objects.create(
        basename=basename,
        name=name,
        category=sample_category(),
    )


def sample_category(basename="primary-school", displayname="Primary School"):
    return Category.objects.create(
        basename=basename,
        displayname=displayname
    )


def sample_user():
    return get_user_model().objects.create(
        username="testuser01",
        email="testuser@bondeveloper.coom",
        password="Qwerty!@#",
    )
#
#
# def sample_subject():
#     return Subject.objects.create(
#         basename="english-fal",
#         name="English FAL",
#         school=sample_school()
#     )


class SubjectPrivateApi(TestCase):
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

    def test_subject_authentication_required(self):
        self.client = APIClient()
        res = self.client.get(subject_list_url)

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subject_create_api_successful(self):
        payload = {
            "basename": "physics",
            "name": "Physics",
            "school": SchoolSerializer(sample_school()).data.get("id")
        }

        res = self.client.post(subject_create_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertEquals(res.data.get("basename"), "mathematics")
