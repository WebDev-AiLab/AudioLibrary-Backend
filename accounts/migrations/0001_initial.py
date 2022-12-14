# Generated by Django 4.0.4 on 2022-09-16 10:36

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('ip', models.CharField(max_length=46, null=True, verbose_name='IP Address')),
                ('ipv', models.CharField(max_length=16, null=True, verbose_name='IP Version')),
                ('phpbb_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='PHPBB ID')),
                ('is_guest', models.BooleanField(default=False, verbose_name='Guest')),
                ('is_active', models.BooleanField(default=True, verbose_name='Active')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Verified by Email')),
                ('password', models.CharField(blank=True, max_length=128, null=True, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Registration Date')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='login')),
                ('browser', models.CharField(blank=True, max_length=255, null=True)),
                ('operating_system', models.CharField(blank=True, max_length=255, null=True)),
                ('last_seen', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Last seen')),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('timezone', models.CharField(blank=True, max_length=255, null=True)),
                ('utc_offset', models.CharField(blank=True, max_length=255, null=True, verbose_name='UTC offset')),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('banned_by_ip', models.BooleanField(default=False)),
                ('_raw_password', models.CharField(blank=True, max_length=512, null=True, verbose_name='Raw Password')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserVerificationData',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('token', models.CharField(editable=False, max_length=255, unique=True)),
                ('target', models.CharField(db_index=True, max_length=50)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('sent', 'sent'), ('completed', 'completed')], db_index=True, default='pending', max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verification', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserContactForm',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Created date')),
                ('updated', models.DateTimeField(auto_now=True, db_index=True, verbose_name='Updated date')),
                ('ip', models.CharField(max_length=46, null=True, verbose_name='IP Address')),
                ('ipv', models.CharField(max_length=16, null=True, verbose_name='IP Version')),
                ('email', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('name', models.CharField(max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Appeal',
            },
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserOnline',
            fields=[
            ],
            options={
                'verbose_name': 'User Online',
                'verbose_name_plural': 'Users Online',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
