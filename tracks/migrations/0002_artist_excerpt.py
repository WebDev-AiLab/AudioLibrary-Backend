# Generated by Django 4.0.4 on 2022-06-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='excerpt',
            field=models.CharField(blank=True, help_text="Very short line containing essential information about artist, for instance 'British Rock-Band'", max_length=128, null=True, verbose_name='Artist Specialization'),
        ),
    ]