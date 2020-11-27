from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Category, School, Level
from school.serializers import LevelSerializer

# if anyones knows how to reverse this path, feel free to make edits
reg_url = '/api/v1/accounts/auth/registration/'
login_url = '/api/v1/accounts/auth/login/'


def sample_level():
    cat = Category.objects.create(
        basename="test-cat",
        name="Test Cat"
    )

    sch = School.objects.create(
        basename="try-school",
        name="Try School 02",
        category=cat
    )

    return Level.objects.create(
        basename="grade-12",
        name="Grade 12",
        school=sch,
    )


class TestPrivateLevelApi(TestCase):
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

    def test_level_authentication_required(self):
        self.client = APIClient()
        res = self.client.get(reverse("school:level-list"))

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_level_api(self):
        cat = Category.objects.create(
            basename="test-cat",
            name="Test Cat"
        )

        sch = School.objects.create(
            basename="test-school02",
            name="Test School 02",
            category=cat
        )

        payload = {
            "basename": "grade-12",
            "name": "Grade 12",
            "school": LevelSerializer(sch).data.get('id'),
        }

        res = self.client.post(reverse("school:level-create"), payload,
                               format='json'
                               )

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_update_level_api(self):
        level = sample_level()

        update_basename = "updated-basename"
        update_name = "Updated Name"
        level.basename = update_basename
        level.name = update_name
        ser = LevelSerializer(level)

        res = self.client.patch(reverse('school:level-update',
                                        args=[ser.data.get('id')]
                                        ),
                                ser.data, format='json'
                                )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get("basename"), update_basename)
        self.assertEqual(res.data.get("name"), update_name)

    def test_list_levels_api(self):
        sample_level()

        cat2 = Category.objects.create(
            basename="test-cat02",
            name="Test Cat02"
        )

        sch2 = School.objects.create(
            basename="A-school02",
            name="A School 02",
            category=cat2
        )

        Level.objects.create(
            basename="grade-1",
            name="Grade 1",
            school=sch2,
        )

        res = self.client.get(reverse('school:level-list'))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

    def test_delete_level_api(self):
        level = sample_level()
        ser = LevelSerializer(level)

        cat2 = Category.objects.create(
            basename="test-cat03",
            name="Test Cat03"
        )

        sch2 = School.objects.create(
            basename="B-school",
            name="B School",
            category=cat2
        )

        Level.objects.create(
            basename="grade-1",
            name="Grade 1",
            school=sch2,
        )

        all = Level.objects.all()
        self.assertEquals(len(all), 2)

        res = self.client.delete(reverse("school:level-delete",
                                         args=[ser.data.get("id")]
                                         )
                                 )
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

        all = Level.objects.all()
        self.assertEquals(len(all), 1)

    def test_retrieve_level_successful(self):
        sub = sample_level()
        ser = LevelSerializer(sub)

        res = self.client.get(reverse('school:level-view',
                                      args=[ser.data.get('id')]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get("basename"), "grade-12")
