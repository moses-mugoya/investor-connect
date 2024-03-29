# Generated by Django 2.2.5 on 2019-11-23 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_partnerspaymentnotes_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ideas',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='startupbusiness',
            name='financing_you_are_looking_for',
        ),
        migrations.RemoveField(
            model_name='startupbusiness',
            name='interest',
        ),
        migrations.RemoveField(
            model_name='startupbusiness',
            name='minimum_financing',
        ),
        migrations.RemoveField(
            model_name='startupbusiness',
            name='stake_you_are_giving_up',
        ),
        migrations.AddField(
            model_name='startupbusiness',
            name='set_direct_investment',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='BusinessDirectInvestment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stake_you_are_giving_up', models.PositiveIntegerField(null=True)),
                ('minimum_financing', models.DecimalField(decimal_places=2, max_digits=15)),
                ('financing_you_are_looking_for', models.DecimalField(decimal_places=2, max_digits=15)),
                ('number_of_investors', models.PositiveIntegerField()),
                ('approved', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.StartupBusiness')),
            ],
        ),
    ]
