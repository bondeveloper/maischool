from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category, School, Session, Subject, Level, Lesson, \
                        Moderation
from school.serializers import SessionSerializer, ModerationSerializer, \
                               UserSerializer


reg_url = '/api/v1/accounts/auth/registration/'


class TestPrivateModerationApi(TestCase):
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
        res = self.client.get(reverse('school:moderation-list'))

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_moderation_create_successful(self):
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

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="TCN",
            end_time=timezone.now(),
            lesson=les
        )

        payload = {
            "session": SessionSerializer(ses).data.get('id'),
            "learner": UserSerializer(learner).data.get('id'),
            "learner_score": 45,
            "max_score": 100,
            "score_type": "unit",
        }

        res = self.client.post(reverse("school:moderation-create"),
                               payload, format='json'
                               )

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        self.assertEquals(res.data.get('learner_score'), 45)

    def test_moderation_update_api(self):
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

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="TCN",
            end_time=timezone.now(),
            lesson=les
        )

        mod = Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=20,
            max_score=100,
            score_type="unit"
        )

        res = self.client.patch(reverse(
                                        "school:moderation-update",
                                        args=[mod.id]
                                        ),
                                ModerationSerializer(mod).data,
                                format='json'
                                )

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('score_type'), 'unit')

    def test_moderation_list_successful(self):
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

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="TCN",
            end_time=timezone.now(),
            lesson=les
        )

        Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=20,
            max_score=100,
            score_type="unit"
        )
        Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=40,
            max_score=100,
            score_type="percentage"
        )

        res = self.client.get(reverse('school:moderation-list'))

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

    def test_moderation_delete_successful(self):
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

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="TCN",
            end_time=timezone.now(),
            lesson=les
        )

        mod1 = Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=20,
            max_score=100,
            score_type="unit"
        )
        Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=40,
            max_score=100,
            score_type="percentage"
        )

        mod = Moderation.objects.all()

        ser = ModerationSerializer(mod, many=True)
        self.assertEquals(len(ser.data), 2)

        res = self.client.delete(reverse(
                                         'school:moderation-delete',
                                         args=[mod1.id]
                                         ),
                                 ser.data, format='json'
                                 )

        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

        mod = Moderation.objects.all()
        ser = ModerationSerializer(mod, many=True)
        self.assertEquals(len(ser.data), 1)

    def test_moderation_retrieve_successful(self):
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

        ses = Session.objects.create(
            start_time=timezone.now(),
            type="TCN",
            end_time=timezone.now(),
            lesson=les
        )

        mod1 = Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=20,
            max_score=100,
            score_type="unit"
        )
        Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=40,
            max_score=100,
            score_type="percentage"
        )

        res = self.client.get(reverse("school:moderation-view",
                                      args=[mod1.id]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('score_type'), 'unit')
