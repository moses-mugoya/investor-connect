# Generated by Django 2.2.5 on 2019-11-23 21:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0006_auto_20191123_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessdirectinvestment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='businessdirectinvestment',
            name='financing_you_are_looking_for',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
        migrations.AlterField(
            model_name='businessdirectinvestment',
            name='minimum_financing',
            field=models.DecimalField(decimal_places=2, max_digits=15, null=True),
        ),
    ]
