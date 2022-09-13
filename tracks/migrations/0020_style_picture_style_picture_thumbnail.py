# Generated by Django 4.0.4 on 2022-06-15 17:53

from django.db import migrations, models
import tools.upload


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0019_remove_genre_style_style_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=tools.upload.ModifyUpload('style')),
        ),
        migrations.AddField(
            model_name='style',
            name='picture_thumbnail',
            field=models.FileField(blank=True, null=True, upload_to=tools.upload.ModifyUpload('thumbnail')),
        ),
    ]
