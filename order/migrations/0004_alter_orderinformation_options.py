# Generated by Django 4.0.1 on 2022-09-10 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderinformation_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderinformation',
            options={'ordering': ('-date',), 'verbose_name_plural': 'Order Information'},
        ),
    ]
