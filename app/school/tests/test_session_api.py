from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category, School, Session, Subject, Level, Lesson
from school.serializers import SessionSerializer, LessonSerializer


reg_url = '/api/v1/accounts/auth/registration/'


class TestPrivateSessionApi(TestCase):
    def setUp(self):
        self.client = APIClient()
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
        res = self.client.get(reverse('school:session-list'))

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_create_api(self):
        learner = get_user_model().objects.create(
            username="learner01",
            email="learner@bondeveloper.coom",
            password="Qwerty!@#",
        )
        learner2 = get_user_model().objects.create(
            username="learner02",
            email="learner02@bondeveloper.coom",
            password="Qwerty!@#",
        )

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        cat = Category.objects.create(
            basename="sample1",
            name="Sample Category"
        )

        sch = School.objects.create(
            basename="gruut-high",
            name="Gruut High",
            category=cat,
        )

        sub = Subject.objects.create(
            basename="spanish-fal",
            name="Spanish FAL",
            school=sch
        )

        level = Level.objects.create(
            basename="grade-9",
            name="Grade 9",
            school=sch
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )
        les.learners.add(learner, learner2)

        payload = {
            "start_time": timezone.now(),
            "type": "TCN",
            "end_time": timezone.now(),
            "lesson": LessonSerializer(les).data.get('id')
        }

        res = self.client.post(reverse("school:session-create"),
                               payload, format='json'
                               )

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertEquals(res.data.get('type'), 'TCN')

    def test_session_update_api(self):
        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        cat = Category.objects.create(
            basename="sample1",
            name="Sample Category"
        )

        sch = School.objects.create(
            basename="gruut-high",
            name="Gruut High",
            category=cat,
        )

        sub = Subject.objects.create(
            basename="spanish-fal",
            name="Spanish FAL",
            school=sch
        )

        level = Level.objects.create(
            basename="grade-9",
            name="Grade 9",
            school=sch
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="XM",
            end_time=timezone.now(),
            lesson=les
        )

        ses.type = "PRT"

        res = self.client.patch(reverse(
                                        "school:session-update",
                                        args=[ses.id]
                                        ),
                                SessionSerializer(ses).data,
                                format='json'
                                )

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('type'), 'PRT')

    def test_session_list_api(self):
        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        cat = Category.objects.create(
            basename="sample1",
            name="Sample Category"
        )

        sch = School.objects.create(
            basename="gruut-high",
            name="Gruut High",
            category=cat,
        )

        sub = Subject.objects.create(
            basename="spanish-fal",
            name="Spanish FAL",
            school=sch
        )

        level = Level.objects.create(
            basename="grade-9",
            name="Grade 9",
            school=sch
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )

        Session.objects.create(
            start_time=timezone.now(),
            type="XM",
            end_time=timezone.now(),
            lesson=les
        )

        Session.objects.create(
            start_time=timezone.now(),
            type="PRT",
            end_time=timezone.now(),
            lesson=les
        )

        res = self.client.get(reverse('school:session-list'))

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

    def test_session_delete_api(self):
        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        cat = Category.objects.create(
            basename="sample1",
            name="Sample Category"
        )

        sch = School.objects.create(
            basename="gruut-high",
            name="Gruut High",
            category=cat,
        )

        sub = Subject.objects.create(
            basename="spanish-fal",
            name="Spanish FAL",
            school=sch
        )

        level = Level.objects.create(
            basename="grade-9",
            name="Grade 9",
            school=sch
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )

        ses1 = Session.objects.create(
            start_time=timezone.now(),
            type="XM",
            end_time=timezone.now(),
            lesson=les
        )

        Session.objects.create(
            start_time=timezone.now(),
            type="PRT",
            end_time=timezone.now(),
            lesson=les
        )
        ser = SessionSerializer(ses1)
        res = self.client.delete(reverse(
                                         'school:session-delete',
                                         args=[ser.data.get('id')]
                                         ),
                                 ser.data, format='json'
                                 )

        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

        ses = Session.objects.all()

        ser = SessionSerializer(ses, many=True)
        self.assertEquals(len(ser.data), 1)

    def test_session_retrieve_successful(self):
        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        cat = Category.objects.create(
            basename="sample1",
            name="Sample Category"
        )

        sch = School.objects.create(
            basename="gruut-high",
            name="Gruut High",
            category=cat,
        )

        sub = Subject.objects.create(
            basename="spanish-fal",
            name="Spanish FAL",
            school=sch
        )

        level = Level.objects.create(
            basename="grade-9",
            name="Grade 9",
            school=sch
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )

        ses1 = Session.objects.create(
            start_time=timezone.now(),
            type="XM",
            end_time=timezone.now(),
            lesson=les
        )

        Session.objects.create(
            start_time=timezone.now(),
            type="PRT",
            end_time=timezone.now(),
            lesson=les
        )

        res = self.client.get(reverse("school:session-view",
                                      args=[ses1.id]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('type'), 'XM')
