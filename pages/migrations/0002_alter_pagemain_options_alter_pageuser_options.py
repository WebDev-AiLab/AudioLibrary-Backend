# Generated by Django 4.0.4 on 2022-07-04 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pagemain',
            options={'verbose_name': 'Menu Item/Main', 'verbose_name_plural': 'Menu Items/Main'},
        ),
        migrations.AlterModelOptions(
            name='pageuser',
            options={'verbose_name': 'Menu Item/User', 'verbose_name_plural': 'Menu Items/User'},
        ),
    ]
