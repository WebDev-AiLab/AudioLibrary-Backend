# Generated by Django 4.0.4 on 2022-09-16 09:09

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadArtists',
            fields=[
            ],
            options={
                'verbose_name': 'Upload Artists',
                'verbose_name_plural': 'Upload Artists',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tracks.artist',),
        ),
        migrations.CreateModel(
            name='UploadTrack',
            fields=[
            ],
            options={
                'verbose_name': 'Upload Tracks',
                'verbose_name_plural': 'Upload Tracks',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('tracks.track',),
        ),
    ]
