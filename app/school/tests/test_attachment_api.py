from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.files import File
from django.contrib.staticfiles import finders

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Category, School, Session, Subject, Level, Lesson, \
                        Attachment
from school.serializers import SessionSerializer, AttachmentSerializer


reg_url = '/api/v1/accounts/auth/registration/'


class TestPrivateAttachmentApi(TestCase):
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
        res = self.client.get(reverse('school:attachment-list'))

        self.assertEquals(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_attachment_create_api(self):
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

        path = finders.find('tests/sample.pdf')
        with open(path, 'r', encoding="ISO-8859-1") as fp:

            payload = {
                "session": SessionSerializer(ses).data.get('id'),
                "notes": "TCN",
                "file": File(fp)
            }

            res = self.client.post(reverse("school:attachment-create"),
                                   payload
                                   )

            self.assertEquals(res.status_code, status.HTTP_201_CREATED)
            self.assertEquals(res.data.get('notes'), 'TCN')

    def test_attachment_update_api(self):
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

        path = finders.find('tests/sample.docx')
        with open(path, 'r', encoding="ISO-8859-1") as fp:

            att = Attachment.objects.create(
                session=ses,
                notes="Test note"
            )

            payload = {
                "file": File(fp),
                "notes": "Updated Notes"
            }

            res = self.client.patch(reverse(
                                           "school:attachment-update",
                                           args=[att.id]
                                           ),
                                    payload
                                    )
            self.assertEquals(res.status_code, status.HTTP_200_OK)
            self.assertIn('file', res.data.keys())
            self.assertIsNotNone(res.data.get('file'))
            self.assertIn('notes', res.data.keys())
            self.assertEquals(res.data.get('notes'), 'Updated Notes')

    def test_attachment_list_api(self):
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

        Attachment.objects.create(
            session=ses,
            notes="Test note"
        )
        Attachment.objects.create(
            session=ses,
            notes="Test note 2"
        )

        res = self.client.get(reverse('school:attachment-list'))

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 2)

    def test_attachment_delete_api(self):
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

        att1 = Attachment.objects.create(
            session=ses,
            notes="Test note"
        )
        Attachment.objects.create(
            session=ses,
            notes="Test note 2"
        )

        att = Attachment.objects.all()

        ser = AttachmentSerializer(att, many=True)
        self.assertEquals(len(ser.data), 2)

        res = self.client.delete(reverse(
                                         'school:attachment-delete',
                                         args=[att1.id]
                                         ),
                                 ser.data, format='json'
                                 )

        self.assertEquals(res.status_code, status.HTTP_204_NO_CONTENT)

        att = Attachment.objects.all()
        ser = AttachmentSerializer(att, many=True)
        self.assertEquals(len(ser.data), 1)

    def test_attachment_retrieve_api(self):
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

        att = Attachment.objects.create(
            session=ses,
            notes="Test note"
        )
        Attachment.objects.create(
            session=ses,
            notes="Test note 2"
        )

        res = self.client.get(reverse("school:attachment-view",
                                      args=[att.id]
                                      )
                              )
        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(res.data.get('notes'), 'Test note')
