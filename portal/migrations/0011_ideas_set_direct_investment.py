# Generated by Django 2.2.5 on 2019-11-24 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0010_auto_20191124_0955'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideas',
            name='set_direct_investment',
            field=models.BooleanField(default=False),
        ),
    ]
