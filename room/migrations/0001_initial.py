# Generated by Django 3.1.7 on 2021-05-01 02:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import room.snippets


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rooms',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('host', models.OneToOneField(help_text='who created the room', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='user.users')),
                ('code', models.CharField(default=room.snippets.generate_unique_code, help_text='public room identifier', max_length=16, unique=True)),
                ('guests_can_pause', models.BooleanField(default=False, help_text='allow guests to pause a room')),
                ('votes_to_skip', models.PositiveSmallIntegerField(default=1, help_text='votes to reach so the song will be skipped', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)])),
                ('current_votes', models.PositiveSmallIntegerField(default=0, help_text='total of votes for the current song', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(999)])),
                ('track_id', models.CharField(default=None, help_text='spotify song_id', max_length=64, null=True)),
                ('current_playing_track', models.JSONField(default=dict, help_text='spotify current playback cleaned for frontend')),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_id', models.CharField(default='', help_text='spotify track_id', max_length=64)),
                ('action', models.CharField(choices=[('SK', 'Skip'), ('LI', 'Like')], help_text='User vote kind for the track', max_length=2)),
                ('room', models.ForeignKey(help_text='Room', on_delete=django.db.models.deletion.CASCADE, to='room.rooms')),
                ('user', models.OneToOneField(help_text='who made the vote the track', on_delete=django.db.models.deletion.CASCADE, to='user.users')),
            ],
        ),
        migrations.CreateModel(
            name='TracksState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('track_id', models.CharField(default='', help_text='spotify track_id', max_length=64)),
                ('uri', models.CharField(help_text="track's uri in Spotify. can be construct with id", max_length=64)),
                ('name', models.TextField(help_text="track's display name in spotify", null=True)),
                ('external_url', models.TextField(help_text="track's first external url in spotify api", null=True)),
                ('album_name', models.TextField(help_text="track's display name in spotify", null=True)),
                ('album_image_url', models.TextField(help_text="album's image url in spotify, intended to be a mid-size image but not ensured", null=True)),
                ('artists_str', models.TextField(help_text="artist's names, coma separated", null=True)),
                ('state', models.CharField(choices=[('SU', 'Success Tracks'), ('SK', 'Skipped Tracks'), ('RE', 'Recommended Tracks'), ('QU', 'Queue Tracks')], help_text='State of the song in the room', max_length=2)),
                ('room', models.ForeignKey(help_text='Room', on_delete=django.db.models.deletion.CASCADE, to='room.rooms')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
