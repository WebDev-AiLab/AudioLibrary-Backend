# Generated by Django 4.0.4 on 2022-06-15 17:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0015_submission'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submission',
            old_name='submitted_file',
            new_name='file',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='submitted_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='submission',
            old_name='submitted_title',
            new_name='title',
        ),
    ]