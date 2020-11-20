from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Category, School
from school.serializers import CategorySerializer, SchoolSerializer
from user.serializers import UserSerializer


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


class TestCategoryModel(TestCase):

    def test_create_category(self):
        saved = sample_category()
        saved = CategorySerializer(saved).data

        category = Category.objects.all()[0]
        category = CategorySerializer(category).data

        self.assertEquals(category, saved)
        self.assertEquals(category.get('basename'), "primary-school")
        self.assertEquals(category.get('displayname'), "Primary School")

    def test_update_category_displayname(self):
        saved = sample_category()

        saved.basename = "primary-sch"
        saved.save()
        saved = CategorySerializer(saved).data

        updated = Category.objects.all()[0]
        updated = CategorySerializer(updated).data

        self.assertEquals(updated, saved)
        self.assertEquals(updated.get('basename'), "primary-sch")

    def test_list_categories(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            displayname="Pre School"
        )

        categories = Category.objects.all()
        categories = CategorySerializer(categories, many=True).data

        self.assertEquals(len(categories), 2)

    def test_remove_category(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            displayname="Pre School"
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

    def test_create_school(self):
        saved = sample_school()
        saved.users.add(sample_user())
        saved.save()
        saved = SchoolSerializer(saved)

        school = School.objects.all()[0]
        serializer = SchoolSerializer(school)

        self.assertEquals(serializer.data,  saved.data)

    def test_update_school_name(self):
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
            displayname="High School"
        )
        category02 = Category.objects.create(
            basename="college",
            displayname="College"
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

    def test_school_delete_school(self):
        sample_school().users.add(sample_user())
        category01 = Category.objects.create(
            basename="high-school",
            displayname="High School"
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
