# Generated by Django 4.2.7 on 2023-12-12 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0017_player_is_connected'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.AutoField(primary_key=True, serialize=False)),
                ('ball_pos_x', models.FloatField()),
                ('ball_pos_y', models.FloatField()),
                ('p1_pos', models.FloatField()),
                ('p2_pos', models.FloatField()),
                ('score', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('ongoing', 'Ongoing'), ('finished', 'Finished'), ('pause', 'Pause')], max_length=20)),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_player2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]