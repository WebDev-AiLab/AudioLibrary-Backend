# Generated by Django 4.0.4 on 2022-06-13 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0003_alter_vote_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='at',
            field=models.IntegerField(default=0, verbose_name='Created At'),
        ),
    ]
