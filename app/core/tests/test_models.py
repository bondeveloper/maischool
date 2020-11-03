from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelsTest(TestCase):
    TEST_DATA = {
        "email": "test@bondeveloper.com",
        "password": "123123",
        "normalize_email": "test@BONDEVELOPER.COM"
    }

    def test_create_user_with_email(self):

        user = get_user_model().objects.create_user(
            email=self.TEST_DATA.get("email"),
            password=self.TEST_DATA.get("password")
        )

        self.assertEqual(user.email, self.TEST_DATA.get("email"))
        self.assertTrue(user.check_password(self.TEST_DATA.get("password")))

    def test_create_user_email_normalized(self):

        user = get_user_model().objects.create_user(
            email=self.TEST_DATA.get("normalize_email"),
            password=self.TEST_DATA.get("password")
        )

        self.assertEqual(user.email, self.TEST_DATA.get("email"))

    def test_create_user_email_not_empty(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                password=self.TEST_DATA.get("password")
            )

    def test_create_user_password_not_empty(self):

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=self.TEST_DATA.get("email")
            )

    def test_create_super_user(self):
        superuser = get_user_model().objects.create_superuser(
            email=self.TEST_DATA.get("email"),
            password=self.TEST_DATA.get("password")
        )

        self.assertEquals(superuser.email, self.TEST_DATA.get("email"))
        self.assertTrue(superuser.is_superuser, True)
