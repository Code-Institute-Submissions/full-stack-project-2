# Generated by Django 3.0.8 on 2020-11-25 17:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultation', '0015_consultation_profile'),
        ('profiles', '0003_auto_20201125_1708'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='UserProfile',
        ),
    ]
