# Generated by Django 3.0.8 on 2020-11-11 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0008_auto_20201111_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='phone_number',
            field=models.CharField(max_length=30),
        ),
    ]
