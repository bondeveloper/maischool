from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


class TestAuthApi(TestCase):

    # if anyones knows how to reverse this path, feel free to make edits
    reg_url = '/api/accounts/auth/registration/'
    login_url = '/api/accounts/auth/login/'
    token_url = '/api/accounts/auth/token/'

    def setUp(self):
        self.client = APIClient()

    def test_user_registration_successful(self):
        payload = {
            "email": "testuser@bondeveloper.com",
            "password1": "Qwerty!@#",
            "password2": "Qwerty!@#",
            "username": "testuser01",
            "first_name": "Test Fistname",
            "last_name": "Test Lastname"
        }
        res = self.client.post(self.reg_url, payload,  format='json')

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', res.data.keys())
        self.assertIn('refresh_token', res.data.keys())
        self.assertIn('user', res.data.keys())
        self.assertEquals(res.data.get('user')['email'], payload.get('email'))

    def test_user_registration_email_required(self):

        payload = {
            "email": "",
            "password1": "Qwerty!@#",
            "password2": "Qwerty!@#",
            "username": "testuser01",
            "first_name": "Test Fistname",
            "last_name": "Test Lastname"
        }
        res = self.client.post(self.reg_url, payload,  format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', res.data.keys())
        self.assertEquals(str(res.data.get('email')[0]),
                          'This field may not be blank.')

    def test_user_registration_username_required(self):
        payload = {
            "email": "testuser@bondeveloper.com",
            "password1": "Qwerty!@#",
            "password2": "Qwerty!@#",
            "username": "",
        }
        res = self.client.post(self.reg_url, payload,  format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', res.data.keys())
        self.assertEquals(str(res.data.get('username')[0]),
                          'This field may not be blank.')

    def test_user_registration_password1_required(self):

        payload = {
            "email": "testuser@bondeveloper.com",
            "password1": "",
            "password2": "Qwerty!@#",
            "username": "testuser01",
        }
        res = self.client.post(self.reg_url, payload,  format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', res.data.keys())
        self.assertEquals(str(res.data.get('password1')[0]),
                          'This field may not be blank.')

    def test_user_registration_password2_required(self):
        payload = {
            "email": "testuser@bondeveloper.com",
            "password1": "Qwerty!@#",
            "password2": "",
            "username": "testuser01",
        }
        res = self.client.post(self.reg_url, payload, format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', res.data.keys())
        self.assertEquals(str(res.data.get('password2')[0]),
                          'This field may not be blank.')

    def test_user_registration_passwords_match(self):
        payload = {
            "email": "testuser@bondeveloper.com",
            "password1": "Qwerty!@#",
            "password2": "Qwerty#@!",
            "username": "testuser01",
        }
        res = self.client.post(self.reg_url, payload,  format='json')

        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data.keys())
        self.assertEquals(str(res.data.get('non_field_errors')[0]),
                          'The two password fields didn\'t match.')

    def test_login_user_required(self):
        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwerty!@#",
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', res.data.keys())
        self.assertEquals(str(res.data.get('non_field_errors')[0]),
                          'Unable to log in with provided credentials.')

    def test_login_successfull(self):
        get_user_model().objects.create_user(
            email="testuser@bondeveloper.com",
            password="Qwert!@#"
        )

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwert!@#"
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code,  status.HTTP_200_OK)
        self.assertIn('access_token', res.data.keys())
        self.assertIn('refresh_token', res.data.keys())
        self.assertIn('user', res.data.keys())
        self.assertEquals(res.data.get('user')['email'], payload.get('email'))

    def test_verify_valid_access_token(self):
        get_user_model().objects.create_user(
            email="testuser@bondeveloper.com",
            password="Qwert!@#"
        )

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwert!@#"
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', res.data.keys())

        payload = {
            "token": str(res.data.get('access_token'))
        }
        res = self.client.post(self.token_url+'verify/', payload,
                               format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)

    def test_verify_invalid_access_token(self):
        get_user_model().objects.create_user(
            email="testuser@bondeveloper.com",
            password="Qwert!@#"
        )

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwert!@#"
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', res.data.keys())

        payload = {
            "token": str(res.data.get('access_token')+"made_invalid_by_str")
        }
        res = self.client.post(self.token_url+'verify/', payload,
                               format='json')
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', res.data.keys())
        self.assertIn('code', res.data.keys())
        self.assertEquals(res.data.get('detail'),
                          'Token is invalid or expired')
        self.assertEquals(res.data.get('code'), 'token_not_valid')

    def test_refresh_using_refresh_token(self):
        get_user_model().objects.create_user(
            email="testuser@bondeveloper.com",
            password="Qwert!@#"
        )

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwert!@#"
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('refresh_token', res.data.keys())

        payload = {
            "refresh": str(res.data.get('refresh_token'))
        }
        res = self.client.post(self.token_url+'refresh/', payload,
                               format='json')

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data.keys())

    def test_refresh_using_access_token(self):
        get_user_model().objects.create_user(
            email="testuser@bondeveloper.com",
            password="Qwert!@#"
        )

        payload = {
            "email": "testuser@bondeveloper.com",
            "password": "Qwert!@#"
        }

        res = self.client.post(self.login_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', res.data.keys())

        payload = {
            "refresh": str(res.data.get('access_token'))
        }
        res = self.client.post(self.token_url+'refresh/', payload,
                               format='json')

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', res.data.keys())
        self.assertIn('code', res.data.keys())
        self.assertEquals(res.data.get('detail'), 'Token has wrong type')
        self.assertEquals(res.data.get('code'), 'token_not_valid')
