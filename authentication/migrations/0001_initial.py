# Generated by Django 4.0.1 on 2022-08-31 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
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
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, null=True, unique=True, verbose_name='email address')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=300, null=True)),
                ('phone_number', models.CharField(max_length=11)),
                ('is_staff', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ('-date_joined',),
            },
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=225, null=True)),
                ('token_type', models.CharField(choices=[('ACCOUNT_VERIFICATION', 'ACCOUNT_VERIFICATION'), ('PASSWORD_RESET', 'PASSWORD_RESET'), ('AUTH_TOKEN', 'AUTH_TOKEN')], default='ACCOUNT_VERIFICATION', max_length=100)),
                ('access', models.CharField(blank=True, max_length=350, null=True)),
                ('refresh', models.CharField(blank=True, max_length=350, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OTPToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=6, null=True)),
                ('token_type', models.CharField(choices=[('ACCOUNT_VERIFICATION', 'ACCOUNT_VERIFICATION'), ('PASSWORD_RESET', 'PASSWORD_RESET'), ('AUTH_TOKEN', 'AUTH_TOKEN')], default='ACCOUNT_VERIFICATION', max_length=100)),
                ('access', models.CharField(blank=True, max_length=350, null=True)),
                ('refresh', models.CharField(blank=True, max_length=350, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
