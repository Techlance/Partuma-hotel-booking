# Generated by Django 3.2.4 on 2021-06-26 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0004_auto_20210625_2243'),
    ]

    operations = [
        migrations.AddField(
            model_name='rooms',
            name='room_photo',
            field=models.ImageField(default='media/about3.jpg', upload_to='rooms_image/'),
        ),
    ]
