# Generated by Django 4.0.4 on 2022-07-04 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tracks', '0027_alter_artistsite_artist_alter_artistsite_source_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='contact_info',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='labelsite',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='label_sites', to='tracks.label'),
        ),
    ]