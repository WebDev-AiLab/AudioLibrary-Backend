# Generated by Django 4.0.4 on 2022-06-07 13:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tracks', '0001_initial'),
        ('accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated date')),
                ('ip', models.CharField(max_length=46, verbose_name='IP Address')),
                ('guest', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.guest')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plays', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
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
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tracks.track')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
