from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status


LIST_USER_URL = reverse("user:list")
# REG_USER_URL = reverse("core:list")


class TestPrivateUserApi(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_authentication_required(self):

        res = self.client.get(LIST_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_user_registration_successful(self):

        # payload = {
        #     "email": "testb@gmail.com",
        #     "username": "test B",
        #     "password1": "123123",
        #     "password2": "123123"
        # }
        #
        # res = self.client.post(adsd, payload)
