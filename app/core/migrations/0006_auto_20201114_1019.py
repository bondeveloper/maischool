# Generated by Django 3.1.3 on 2020-11-14 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
