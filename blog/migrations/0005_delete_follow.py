# Generated by Django 3.1.4 on 2020-12-11 05:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
