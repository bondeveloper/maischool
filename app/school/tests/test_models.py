from django.test import TestCase

from core.models import Category


def sample_category(basename="primary-school", displayname="Primary School"):
    return Category.objects.create(
        basename=basename,
        displayname=displayname
    )


class TestCategoryModel(TestCase):

    def test_create_category(self):
        category = sample_category()

        self.assertEqual(category.basename, "primary-school")
        self.assertEqual(category.displayname, "Primary School")

    def test_update_category(self):
        category = sample_category()

        to_update = Category.objects.all()[0]

        self.assertEqual(to_update.basename, category.basename)
        self.assertEqual(to_update.displayname, category.displayname)

        to_update.basename = "primary-sch"
        to_update.save()

        updated = Category.objects.all()[0]

        self.assertNotEqual(updated.basename, category.basename)

    def test_list_categories(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            displayname="Pre School"
        )

        categories = Category.objects.all()

        self.assertEqual(len(categories), 2)

    def test_remove_category(self):
        sample_category()
        Category.objects.create(
            basename="pre-school",
            displayname="Pre School"
        )

        categories = Category.objects.all()

        self.assertEqual(len(categories), 2)

        Category.objects.all()[0].delete()
        categories = Category.objects.all()

        self.assertNotEqual(len(categories), 2)
        self.assertEqual(len(categories), 1)
