# Generated by Django 4.0.4 on 2022-07-02 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_usercontactform_ip_usercontactform_ipv_alter_user_ip'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usercontactform',
            options={'verbose_name': 'Appeal'},
        ),
    ]