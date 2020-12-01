from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.utils import timezone

from core.models import Category, School, Subject, Level, Lesson, Session, \
                        Attachment, Moderation
from school.serializers import CategorySerializer, SchoolSerializer, \
                               SubjectSerializer, LevelSerializer, \
                               LessonSerializer, SessionSerializer, \
                               AttachmentSerializer, ModerationSerializer
from user.serializers import UserSerializer


def sample_school(basename="test-school", name="test school"):
    return School.objects.create(
        basename=basename,
        name=name,
        category=sample_category(),
    )


def sample_category(basename="primary-school", name="Primary School"):
    return Category.objects.create(
        basename=basename,
        name=name
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


def sample_level():
    return Level.objects.create(
        basename="grade-12",
        name="Grade 12",
        school=sample_school()
    )


class TestCategoryModel(TestCase):

    def test_category_create(self):
        saved = sample_category()
        saved = CategorySerializer(saved).data

        category = Category.objects.all()[0]
        category = CategorySerializer(category).data

        self.assertEquals(category, saved)
        self.assertEquals(category.get('basename'), "primary-school")
        self.assertEquals(category.get('name'), "Primary School")

    def test_category_update_displayname(self):
        saved = sample_category()

        saved.basename = "primary-sch"
        saved.save()
        saved = CategorySerializer(saved).data

        updated = Category.objects.all()[0]
        updated = CategorySerializer(updated).data

        self.assertEquals(updated, saved)
        self.assertEquals(updated.get('basename'), "primary-sch")

    def test_categories_list(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            name="Pre School"
        )

        categories = Category.objects.all()
        categories = CategorySerializer(categories, many=True).data

        self.assertEquals(len(categories), 2)

    def test_category_delete(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            name="Pre School"
        )

        categories = Category.objects.all()
        categories = CategorySerializer(categories, many=True).data
        self.assertEquals(len(categories), 2)

        Category.objects.all()[0].delete()
        categories = Category.objects.all()
        categories = CategorySerializer(categories, many=True).data

        self.assertNotEquals(len(categories), 2)
        self.assertEquals(len(categories), 1)


class TestSchoolModel(TestCase):

    def test_school_create_successful(self):
        saved = sample_school()
        saved.users.add(sample_user())
        saved.save()
        saved = SchoolSerializer(saved)

        school = School.objects.all()[0]
        serializer = SchoolSerializer(school)

        self.assertEquals(serializer.data,  saved.data)

    def test_school_update_name(self):
        saved = sample_school()
        saved.users.add(sample_user())
        saved.name = "Updated name"
        saved.save()
        saved = SchoolSerializer(saved)

        self.assertEquals(saved.data.get('name'),  "Updated name")

    def test_school_list(self):
        saved = sample_school()
        saved.users.add(sample_user())
        saved.save()
        category01 = Category.objects.create(
            basename="high-school",
            name="High School"
        )
        category02 = Category.objects.create(
            basename="college",
            name="College"
        )
        user1 = get_user_model().objects.create(
            username="testuser02",
            email="testuser02@bondeveloper.coom",
            password="Qwerty!@#",
        )
        user2 = get_user_model().objects.create(
            username="testuser03",
            email="testuser03@bondeveloper.coom",
            password="Qwerty!@#",
        )

        School.objects.create(
            basename="bbg",
            name="Beitbridge Gvt",
            category=category01,
        ).users.add(user1)
        School.objects.create(
            basename="mckeurtan",
            name="Mckeurtan",
            category=category02,
        ).users.add(user2)

        list = School.objects.all()
        serializer = SchoolSerializer(list, many=True)
        self.assertTrue(len(serializer.data), 3)

    def test_school_delete_successful(self):
        sample_school().users.add(sample_user())
        category01 = Category.objects.create(
            basename="high-school",
            name="High School"
        )

        user1 = get_user_model().objects.create(
            username="testuser02",
            email="testuser02@bondeveloper.coom",
            password="Qwerty!@#",
        )

        School.objects.create(
            basename="bbg",
            name="Beitbridge Gvt",
            category=category01,
        ).users.add(user1)

        list = School.objects.all()
        school = list[0]
        serializer = SchoolSerializer(list, many=True)
        self.assertEquals(len(serializer.data), 2)

        list = Category.objects.all()
        serializer = CategorySerializer(list, many=True)
        self.assertEquals(len(serializer.data), 2)

        list = get_user_model().objects.all()
        serializer = UserSerializer(list, many=True)
        self.assertEquals(len(serializer.data), 2)

        school.delete()

        list = School.objects.all()
        serializer = SchoolSerializer(list, many=True)
        self.assertNotEquals(len(serializer.data), 2)


class TestSubjectModel(TestCase):
    def test_create_subject_successful(self):

        serializer = SubjectSerializer(sample_subject())

        saved = Subject.objects.get(pk=serializer.data.get('id'))
        saved_serializer = SubjectSerializer(saved)

        self.assertEquals(serializer.data, saved_serializer.data)

    def test_subject_basename_unique(self):
        sample_subject()

        with self.assertRaises(IntegrityError):
            sample_subject()

    def test_subject_update_successful(self):
        subject = sample_subject()
        ser = SubjectSerializer(subject)

        update_basename = "updated-basename"
        update_name = "Updated Name"

        Subject .objects.filter(pk=ser.data.get("id")).update(
            basename=update_basename,
            name=update_name
        )

        subject.refresh_from_db()
        ser = SubjectSerializer(subject)

        self.assertEqual(ser.data.get("basename"), update_basename)
        self.assertEqual(ser.data.get("name"), update_name)

    def test_list_subjects(self):
        sample_subject()

        category01 = Category.objects.create(
            basename="high-school1",
            name="High School1"
        )
        category02 = Category.objects.create(
            basename="college1",
            name="College1"
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

        subjects = Subject.objects.all()
        ser = SubjectSerializer(subjects, many=True)

        self.assertEquals(len(ser.data), 3)

    def test_delete_subject(self):
        subject = Subject.objects.create(
            basename="math-literacy",
            name="Mathematic Literacy",
            school=sample_school()
        )
        ser = SubjectSerializer(subject)
        Subject.objects.filter(pk=ser.data.get("id")).delete()

        subjects = Subject.objects.all()
        self.assertEquals(len(subjects), 0)


class TestLevelModel(TestCase):
    def test_level_create_succesful(self):

        ser = LevelSerializer(sample_level())
        self.assertIn('id', ser.data.keys())
        self.assertIsNotNone(ser.data.get("id"))

    def test_basename_level_unique(self):
        sample_level()

        cat = Category.objects.create(
            basename="test-cat",
            name="Test Cat"
        )

        sch = School.objects.create(
            basename="test-school02",
            name="Test School 02",
            category=cat
        )

        with self.assertRaises(IntegrityError):

            Level.objects.create(
                basename="grade-12",
                name="Grade 12",
                school=sch,
            )

    def test_level_update(self):
        level = sample_level()
        Level.objects.filter(pk=level.id).update(
            basename="updated-basename",
            name="Updated Name"
        )

        level.refresh_from_db()
        ser = LevelSerializer(level)
        self.assertEquals(ser.data.get("basename"), 'updated-basename')
        self.assertEquals(ser.data.get("name"), 'Updated Name')

    def test_levels_list(self):
        sample_level()

        cat = Category.objects.create(
            basename="cat-basename",
            name="Cat name"
        )

        sch = School.objects.create(
            basename="sch-basename",
            name="Sch name",
            category=cat,
        )

        Level.objects.create(
            basename="grade-10",
            name="Grade 0",
            school=sch,
        )

        all = Level.objects.all()
        self.assertEquals(len(all), 2)

    def test_level_delete(self):

        cat = Category.objects.create(
            basename="cat-basename",
            name="Cat name"
        )

        sch = School.objects.create(
            basename="sch-basename",
            name="Sch name",
            category=cat,
        )

        level = Level.objects.create(
            basename="grade-12",
            name="Grade 12",
            school=sch,
        )

        cat = Category.objects.create(
            basename="cat-basename02",
            name="Cat displayname02"
        )

        sch = School.objects.create(
            basename="sch-basename02",
            name="Sch name02",
            category=cat,
        )

        Level.objects.create(
            basename="grade-11",
            name="Grade 11",
            school=sch,
        )

        all = Level.objects.all()
        self.assertEquals(len(all), 2)

        Level.objects.filter(pk=level.id).delete()
        all = Level.objects.all()
        self.assertEquals(len(all), 1)


class TestLessonModel(TestCase):
    def test_lesson_create_succesful(self):

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

        ser = LessonSerializer(les)
        self.assertIn('id', ser.data.keys())
        self.assertIsNotNone(ser.data.get("id"))

    def test_lesson_update_succesful(self):

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

        Lesson.objects.filter(pk=les.id).update(
            name="Python 3"
        )

        les.refresh_from_db()

        ser = LessonSerializer(les)
        self.assertEquals(ser.data.get("name"), "Python 3")

    def test_lessons_list(self):

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

        les2 = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python Advanced"
        )
        les2.learners.add(learner, learner2)

        res = Lesson.objects.all()
        ser = LessonSerializer(res, many=True)
        self.assertEquals(len(ser.data), 2)

    def test_lesson_delete(self):

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

        les2 = Lesson.objects.create(
            subject=sub,
            level=level,
            instructor=instructor,
            name="Python Advanced"
        )
        les2.learners.add(learner, learner2)

        res = Lesson.objects.all()
        ser = LessonSerializer(res, many=True)
        self.assertEquals(len(ser.data), 2)

        Lesson.objects.filter(pk=les.id).delete()
        res = Lesson.objects.all()
        ser = LessonSerializer(res, many=True)
        self.assertEquals(len(ser.data), 1)


class TestSessionModel(TestCase):
    def test_session_create_successful(self):
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
        ses.attendance.add(learner, learner2)
        ser = SessionSerializer(ses)
        self.assertIn('id', ser.data.keys())
        self.assertIsNotNone(ser.data.get('id'))

    def test_session_update_successful(self):
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
        ser = SessionSerializer(ses)

        start_time = timezone.now() + timezone.timedelta(days=3)

        Session.objects.filter(pk=ser.data.get('id')).update(
            start_time=start_time,
            end_time=timezone.now() + timezone.timedelta(days=3),
            type='PRT'
        )

        ses.refresh_from_db()

        ser = SessionSerializer(ses)
        self.assertEquals(ser.data.get('type'), 'PRT')

    def test_session_list_successful(self):
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
        ses = Session.objects.all()

        ser = SessionSerializer(ses, many=True)
        self.assertEquals(len(ser.data), 2)

    def test_session_delete_successful(self):
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
        ses = Session.objects.all()

        ser = SessionSerializer(ses, many=True)
        self.assertEquals(len(ser.data), 2)

        Session.objects.filter(pk=ses1.id).delete()
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
        ses = Session.objects.get(pk=ses1.id)

        ser = SessionSerializer(ses)
        self.assertEquals(ser.data.get('type'), 'XM')


class TestAttachmentModel(TestCase):
    def test_attachment_create_successful(self):
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
            notes="Test note",
            file="attachment.pdf"
        )

        ser = AttachmentSerializer(att)
        self.assertIn('id', ser.data.keys())
        self.assertIsNotNone(ser.data.get('id'))

    def test_attachment_update_successful(self):
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

        Attachment.objects.filter(pk=att.id).update(notes="Notes Update")
        att.refresh_from_db()

        ser = AttachmentSerializer(att)
        self.assertEquals(ser.data.get('notes'), 'Notes Update')

    def test_attachment_list_successful(self):
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

        att = Attachment.objects.all()

        ser = AttachmentSerializer(att, many=True)
        self.assertEquals(len(ser.data), 2)

    def test_attachment_delete_successful(self):
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

        Attachment.objects.filter(pk=att1.id).delete()
        att = Attachment.objects.all()

        ser = AttachmentSerializer(att, many=True)
        self.assertEquals(len(ser.data), 1)

    def test_attachment_retrieve_successful(self):
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

        att = Attachment.objects.get(pk=att1.id)

        ser = AttachmentSerializer(att)
        self.assertEquals(ser.data.get('notes'), 'Test note')


class TestModerationModel(TestCase):
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

        mod = Moderation.objects.create(
            session=ses,
            learner=learner,
            learner_score=20,
            max_score=100,
            score_type="unit"
        )

        ser = ModerationSerializer(mod)
        self.assertIn('id', ser.data.keys())
        self.assertIsNotNone(ser.data.get('id'))

    def test_moderation_update_successful(self):
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

        Moderation.objects.filter(pk=mod.id).update(score_type="percentage")
        mod.refresh_from_db()

        ser = ModerationSerializer(mod)
        self.assertEquals(ser.data.get('score_type'), 'percentage')

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

        mod = Moderation.objects.all()

        ser = ModerationSerializer(mod, many=True)
        self.assertEquals(len(ser.data), 2)

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

        Moderation.objects.filter(pk=mod1.id).delete()
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

        mod = Moderation.objects.get(pk=mod1.id)

        ser = ModerationSerializer(mod)
        self.assertEquals(ser.data.get('score_type'), 'unit')
