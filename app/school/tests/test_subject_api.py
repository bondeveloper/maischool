from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import School, Category, Subject
from school.serializers import SchoolSerializer, SubjectSerializer

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


def sample_subject():
    return Subject.objects.create(
        basename="english-fal",
        name="English FAL",
        school=sample_school()
    )


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

        category01 = Category.objects.create(
            basename="high-school",
            displayname="High School"
        )

        school = School.objects.create(
            basename="bbg",
            name="Beitbridge Gvt",
            category=category01,
        )

        payload = {
            "basename": "physics",
            "name": "Physics",
            "school": SchoolSerializer(school).data.get("id")
        }

        res = self.client.post(subject_create_url, payload, format='json')
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertEquals(res.data.get("basename"), "physics")

    def test_list_subjects_api(self):
        category01 = Category.objects.create(
            basename="high-school1",
            displayname="High School1"
        )
        category02 = Category.objects.create(
            basename="college1",
            displayname="College1"
        )

        s1 = School.objects.create(
            basename="bbg01",
            name="Beitbridge Gvt1",
            category=category01,
        )

        Subject.objects.create(
            basename="xhosa-hl1",
            name="Xhosa HL",
            school=s1
        )

        s2 = School.objects.create(
            basename="mckeurtan1",
            name="Mckeurtan",
            category=category02,
        )

        Subject.objects.create(
            basename="afrikaans-hl1",
            name="Afrikaans HL",
            school=s2
        )

        res = self.client.get(subject_list_url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

    def test_subject_update_successful(self):
        subject = sample_subject()
        update_basename = "updated-basename"
        update_name = "Updated Name"
        subject.basename = update_basename
        subject.name = update_name
        ser = SubjectSerializer(subject)

        # res = self.client.patch(reverse('school:subject-update',
        #                               args=[ser.data.get('id')]
        #                               )
        #                        ), ser.data, format='json')
        res = self.client.patch(
                               reverse('school:subject-update',
                                       args=[ser.data.get('id')]
                                       ),
                               ser.data, format='json'
                             )

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("basename"), update_basename)
        self.assertEqual(res.data.get("name"), update_name)

    def test_delete_subject(self):
        subject = Subject.objects.create(
            basename="math-literacy",
            name="Mathematic Literacy",
            school=sample_school()
        )
        ser = SubjectSerializer(subject)
        res = self.client.delete(reverse('school:subject-delete',
                                         args=[ser.data.get('id')]
                                         )
                                 )
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_subject_successful(self):
        sub = sample_subject()
        ser = SubjectSerializer(sub)

        res = self.client.get(reverse('school:subject-view',
                                      args=[ser.data.get('id')]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get("basename"), "english-fal")
