# Generated by Django 4.0.1 on 2022-09-29 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendorinformation',
            name='phone_number',
            field=models.CharField(max_length=20),
        ),
    ]
