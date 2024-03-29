# Generated by Django 4.2.7 on 2023-12-26 06:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_delete_player'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='ball_pos_x',
        ),
        migrations.RemoveField(
            model_name='game',
            name='ball_pos_y',
        ),
        migrations.RemoveField(
            model_name='game',
            name='map',
        ),
        migrations.RemoveField(
            model_name='game',
            name='p1_pos',
        ),
        migrations.RemoveField(
            model_name='game',
            name='p2_pos',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player_1_name',
        ),
        migrations.RemoveField(
            model_name='game',
            name='player_2_name',
        ),
        migrations.RemoveField(
            model_name='game',
            name='status',
        ),
        migrations.AddField(
            model_name='game',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
