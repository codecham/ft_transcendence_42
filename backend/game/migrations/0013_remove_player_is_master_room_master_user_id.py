# Generated by Django 4.2.7 on 2023-12-10 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_player_is_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='is_master',
        ),
        migrations.AddField(
            model_name='room',
            name='master_user_id',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
