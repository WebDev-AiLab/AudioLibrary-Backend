# Generated by Django 4.0.4 on 2022-06-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0017_remove_style_genre_genre_style_style_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='style',
            field=models.ManyToManyField(related_name='genres', to='tracks.style'),
        ),
    ]
