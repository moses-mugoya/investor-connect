# Generated by Django 2.2.5 on 2019-11-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20191123_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ideas',
            name='copyright_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='ideas',
            name='patent_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='startupbusiness',
            name='company_registration_number',
            field=models.CharField(max_length=50),
        ),
    ]
