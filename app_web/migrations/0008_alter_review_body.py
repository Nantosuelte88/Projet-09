# Generated by Django 5.0 on 2024-01-11 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_web', '0007_remove_userfollows_is_blocked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='body',
            field=models.TextField(blank=True, max_length=8192),
        ),
    ]