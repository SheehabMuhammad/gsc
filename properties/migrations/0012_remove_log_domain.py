# Generated by Django 3.2.6 on 2021-08-27 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_log_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log',
            name='domain',
        ),
    ]
