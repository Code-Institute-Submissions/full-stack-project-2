# Generated by Django 3.0.8 on 2020-11-22 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0011_consultation_stripe_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='original_idea',
            field=models.TextField(default=''),
        ),
    ]
