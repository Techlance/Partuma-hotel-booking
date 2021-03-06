# Generated by Django 3.2.4 on 2021-06-26 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0005_rooms_room_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rooms',
            old_name='room_photo',
            new_name='room_photo_1',
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_photo_2',
            field=models.ImageField(default='media/about3.jpg', upload_to='rooms_image/'),
        ),
        migrations.AddField(
            model_name='rooms',
            name='room_photo_3',
            field=models.ImageField(default='media/about3.jpg', upload_to='rooms_image/'),
        ),
    ]
