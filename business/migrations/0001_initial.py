# Generated by Django 4.0.1 on 2022-08-31 21:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorInformation',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=225)),
                ('phone_number', models.CharField(max_length=11)),
                ('password', models.CharField(blank=True, max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('file', models.FileField(blank=True, upload_to='vendor_profile')),
                ('address', models.CharField(blank=True, max_length=250)),
                ('category', models.CharField(blank=True, choices=[('food', 'Foods'), ('cake_pastries', 'Cakes and Pastries'), ('shar_pizza_grillz', 'Sharwarma, Pizza and Grillz'), ('snacks', 'Snacks and Small Chops'), ('others', 'Others')], max_length=100)),
                ('profile_updated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'VendorInformation',
            },
        ),
        migrations.CreateModel(
            name='MenuItems',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('category', models.CharField(blank=True, choices=[('rice', 'RICE'), ('cake_pastries', 'Cakes and Pastries'), ('swallow', 'Swallow'), ('proteins', 'Proteins'), ('soft_drinks', 'Soft Drinks'), ('juice', 'Juice'), ('yogourt', 'Yogourt')], max_length=100)),
                ('price', models.IntegerField()),
                ('vendor', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='business.vendorinformation')),
            ],
            options={
                'verbose_name_plural': 'MenuItems',
            },
        ),
    ]
