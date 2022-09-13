# Generated by Django 4.0.4 on 2022-07-05 18:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0028_label_contact_info_alter_labelsite_label'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artist',
            name='birth_location',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='birthday',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='excerpt',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='profile_aliases',
        ),
        migrations.RemoveField(
            model_name='artist',
            name='type',
        ),
        migrations.RemoveField(
            model_name='artistsite',
            name='source',
        ),
        migrations.AddField(
            model_name='artist',
            name='contact_info',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='singer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='artist',
            name='status',
            field=models.CharField(blank=True, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=16, null=True),
        ),
        migrations.AddField(
            model_name='artist',
            name='wikipedia',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='artist',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='Profile'),
        ),
        migrations.AlterField(
            model_name='artist',
            name='voice_type',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Type of Voice'),
        ),
        migrations.AlterField(
            model_name='label',
            name='contact_info',
            field=models.TextField(blank=True, null=True, verbose_name='contact'),
        ),
        migrations.CreateModel(
            name='ArtistYoutube',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('url', models.URLField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_youtubes', to='tracks.artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtistSocial',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('source', models.CharField(choices=[('Facebook', 'Facebook'), ('Instagram', 'Instagram'), ('Twitter', 'Twitter'), ('VK', 'VK')], db_index=True, max_length=64, verbose_name='Social Network')),
                ('url', models.URLField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_social', to='tracks.artist')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArtistMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('source', models.CharField(choices=[('Spotify', 'Spotify'), ('Apple Music', 'Apple Music')], db_index=True, max_length=64, verbose_name='Service')),
                ('url', models.URLField()),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artist_medias', to='tracks.artist')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
