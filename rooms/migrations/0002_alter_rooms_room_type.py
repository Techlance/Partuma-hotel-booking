# Generated by Django 3.2.4 on 2021-06-25 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='room_type',
            field=models.TextField(),
        ),
    ]
