# Generated by Django 3.2.4 on 2021-06-30 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0008_auto_20210629_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rooms',
            name='air_conditioning',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='breakfast',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='dinner',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='gym',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='lunch',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='swimming_pool',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='tv',
        ),
        migrations.RemoveField(
            model_name='rooms',
            name='wifi',
        ),
    ]
