# Generated by Django 4.0.4 on 2022-07-04 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercontactform',
            name='name',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usercontactform',
            name='subject',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]