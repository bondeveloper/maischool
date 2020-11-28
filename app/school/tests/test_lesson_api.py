from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from core.models import School, Level, Lesson, Category, Subject
from school.serializers import SubjectSerializer, LessonSerializer, \
                               LevelSerializer, UserSerializer


# if anyones knows how to reverse this path, feel free to make edits
reg_url = '/api/v1/accounts/auth/registration/'
login_url = '/api/v1/accounts/auth/login/'


class TestPublicLessonApi(TestCase):
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

    def test_lesson_authentication_required(self):
        self.client = APIClient()
        res = self.client.get(reverse("school:lesson-list"))
        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_lesson_create_api_successful(self):
        cat = Category.objects.create(
            basename="test-cat",
            name="Test Category"
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

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        learner = get_user_model().objects.create(
            username="learner01",
            email="learner@bondeveloper.coom",
            password="Qwerty!@#",
        )
        learner2 = get_user_model().objects.create(
            username="learner02",
            email="learner2@bondeveloper.coom",
            password="Qwerty!@#",
        )

        payload = {
            "subject": SubjectSerializer(sub).data.get('id'),
            "level": LevelSerializer(level).data.get('id'),
            "instructor": UserSerializer(instructor).data.get('id'),
            "learners": [
                            UserSerializer(learner).data.get('id'),
                            UserSerializer(learner2).data.get('id')
                        ],
            "name": "Django for beginners"
        }

        res = self.client.post(reverse("school:lesson-create"), payload,
                               format='json'
                               )
        self.assertEquals(res.status_code, status.HTTP_201_CREATED)

    def test_lesson_update_api_successful(self):

        cat = Category.objects.create(
            basename="test-cat",
            name="Test Category"
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

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )

        ser = LessonSerializer(les)

        res = self.client.patch(reverse(
                                       "school:lesson-update",
                                       args=[ser.data.get('id')]
                                      ),
                                ser.data,
                                format='json'
                                )
        les.refresh_from_db()
        ser = LessonSerializer(les)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data, ser.data)

    def test_lesson_list_api(self):
        cat = Category.objects.create(
            basename="test-cat",
            name="Test Category"
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

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )

        Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )

        Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python 101"
        )

        Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python Advanced"
        )

        res = self.client.get(reverse("school:lesson-list"))
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 4)

    def test_lesson_delete_api(self):
        cat = Category.objects.create(
            basename="test-cat",
            name="Test Category"
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

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )
        all = Lesson.objects.all()
        ser = LessonSerializer(all, many=True)
        self.assertEquals(len(ser.data), 2)

        res = self.client.delete(reverse("school:lesson-delete",
                                         args=[les.id]
                                         )
                                 )
        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)
        all = Lesson.objects.all()
        ser = LessonSerializer(all, many=True)
        self.assertEquals(len(ser.data), 1)

    def test_lesson_retrieve_api(self):
        cat = Category.objects.create(
            basename="test-cat",
            name="Test Category"
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

        instructor = get_user_model().objects.create(
            username="instructor",
            email="instructor@bondeveloper.coom",
            password="Qwerty!@#",
        )

        les = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Django for beginners"
        )

        res = self.client.get(reverse("school:lesson-view",
                                      args=[les.id]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        ser = LessonSerializer(les)
        self.assertEquals(res.data, ser.data)
