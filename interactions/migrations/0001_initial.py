# Generated by Django 4.0.4 on 2022-09-16 09:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('ip', models.CharField(max_length=46, null=True, verbose_name='IP Address')),
                ('ipv', models.CharField(max_length=16, null=True, verbose_name='IP Version')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plays', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TrackPlays',
            fields=[
            ],
            options={
                'verbose_name': 'Play',
                'verbose_name_plural': 'Plays',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tracks.track',),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Like',
                'verbose_name_plural': 'Likes',
            },
        ),
        migrations.CreateModel(
            name='Stat',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('type', models.CharField(choices=[('vote', 'Like'), ('play', 'Play')], db_index=True, max_length=16)),
                ('play', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactions.play')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracks.track')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vote', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='interactions.vote')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('text', models.TextField(max_length=2048)),
                ('at', models.IntegerField(default=0, verbose_name='Created At')),
                ('type', models.CharField(choices=[('track', 'Track'), ('artist', 'Artist')], db_index=True, max_length=16)),
                ('artist', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tracks.artist')),
                ('track', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommentArtists',
            fields=[
            ],
            options={
                'verbose_name': 'Comment/Artist',
                'verbose_name_plural': 'Comments/Artist',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('interactions.comment',),
        ),
        migrations.CreateModel(
            name='CommentTracks',
            fields=[
            ],
            options={
                'verbose_name': 'Comment/Track',
                'verbose_name_plural': 'Comments/Track',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('interactions.comment',),
        ),
    ]
