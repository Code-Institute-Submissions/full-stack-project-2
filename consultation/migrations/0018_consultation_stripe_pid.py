# Generated by Django 3.0.8 on 2020-11-26 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0017_auto_20201125_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='stripe_pid',
            field=models.CharField(default='', max_length=254),
        ),
    ]