# Generated by Django 4.2.7 on 2023-11-28 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='connected_users',
            field=models.ManyToManyField(related_name='connected_rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
