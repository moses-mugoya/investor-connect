# Generated by Django 2.2.5 on 2019-11-24 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_ideadirectinvestment'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessdirectinvestment',
            name='declined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ideadirectinvestment',
            name='declined',
            field=models.BooleanField(default=False),
        ),
    ]
