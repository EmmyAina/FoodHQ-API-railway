# Generated by Django 4.0.1 on 2022-09-08 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_wallettrxinformation'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettrxinformation',
            name='transaction_reference',
            field=models.CharField(blank=True, max_length=16),
        ),
    ]
