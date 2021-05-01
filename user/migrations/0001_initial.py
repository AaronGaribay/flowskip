# Generated by Django 3.1.7 on 2021-05-01 02:20

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commerces',
            fields=[
                ('id', models.CharField(help_text="user's id in spotify database", max_length=64, primary_key=True, serialize=False)),
                ('commerce_name', models.CharField(default=None, help_text='name of the commerce', max_length=64, validators=[django.core.validators.MinLengthValidator(3)])),
                ('exclusive_code', models.CharField(help_text='code for commerce room', max_length=16, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('commerce_lon', models.DecimalField(decimal_places=6, help_text="longitud of the comerce's physical location", max_digits=9, null=True)),
                ('commerce_lat', models.DecimalField(decimal_places=6, help_text="latitude of the comerce's physical location", max_digits=9, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaidUsers',
            fields=[
                ('id', models.CharField(help_text="user's id in spotify database", max_length=64, primary_key=True, serialize=False)),
                ('exclusive_code', models.CharField(default=None, help_text='code for personal room', max_length=16, null=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('session', models.OneToOneField(help_text='django session for the user', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='sessions.session')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
