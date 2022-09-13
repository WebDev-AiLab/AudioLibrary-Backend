# Generated by Django 4.0.4 on 2022-06-15 17:41

from django.db import migrations, models
import tools.upload


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0016_rename_submitted_file_submission_file_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='style',
            name='genre',
        ),
        migrations.AddField(
            model_name='genre',
            name='style',
            field=models.ManyToManyField(to='tracks.style'),
        ),
        migrations.AddField(
            model_name='style',
            name='description',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='file',
            field=models.FileField(editable=False, help_text='.mp3 file location', upload_to=tools.upload.ModifyUpload('file'), verbose_name='.MP3 File'),
        ),
    ]