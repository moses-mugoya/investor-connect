# Generated by Django 2.2.5 on 2019-11-23 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_services_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='partnerspaymentnotes',
            name='amount',
            field=models.PositiveIntegerField(null=True),
        ),
    ]