# Generated by Django 3.2.6 on 2021-08-16 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('property', models.URLField(unique=True)),
                ('description', models.TextField(blank=True)),
                ('options', models.TextField(blank=True)),
                ('crawl_priority', models.CharField(default='low', max_length=100)),
                ('last_crawled', models.DateTimeField(blank=True)),
                ('is_active', models.BooleanField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Properties',
            },
        ),
        migrations.CreateModel(
            name='Url',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('c_type', models.CharField(blank=True, max_length=255, null=True)),
                ('c_status', models.CharField(blank=True, max_length=255, null=True)),
                ('crawled_at', models.DateTimeField(default=None, null=True)),
                ('mu_type', models.CharField(blank=True, max_length=255, null=True)),
                ('mu_status', models.CharField(blank=True, default='Not listed as mobile friendly', max_length=255, null=True)),
                ('detected_at', models.DateTimeField(default=None, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='properties.property')),
            ],
            options={
                'verbose_name_plural': 'Options',
            },
        ),
        migrations.AddConstraint(
            model_name='url',
            constraint=models.UniqueConstraint(fields=('property', 'url'), name='unique property url constraint'),
        ),
    ]