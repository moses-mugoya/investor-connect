# Generated by Django 2.2.5 on 2019-11-24 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_ideas_set_direct_investment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessinvestments',
            name='investor_amount',
        ),
    ]
