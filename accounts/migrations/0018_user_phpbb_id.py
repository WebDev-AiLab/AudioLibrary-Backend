# Generated by Django 4.0.4 on 2022-08-08 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_usercontactform_name_usercontactform_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phpbb_id',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
    ]