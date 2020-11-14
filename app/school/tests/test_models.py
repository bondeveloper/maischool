from django.test import TestCase

from core.models import Category
from school.serializers import CategorySerializer


def sample_category(basename="primary-school", displayname="Primary School"):
    return Category.objects.create(
        basename=basename,
        displayname=displayname
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
