# Generated by Django 4.0.4 on 2022-07-06 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0032_artist_beatport_artist_discogs_label_beatport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='is_wikipedia',
            field=models.BooleanField(default=False, verbose_name='Has Wikipedia page'),
        ),
        migrations.AddField(
            model_name='artist',
            name='visible',
            field=models.BooleanField(db_index=True, default=True, verbose_name='Visible'),
        ),
    ]