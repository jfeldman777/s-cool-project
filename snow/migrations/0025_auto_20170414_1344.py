# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 10:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('snow', '0024_examrecord_done'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArcStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Empty'), ('A', 'Asked'), ('G', 'Granted'), ('D', 'Delayed'), ('B', 'Blocked')], default='E', max_length=1)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WizStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('E', 'Empty'), ('A', 'Asked'), ('G', 'Granted'), ('D', 'Delayed'), ('B', 'Blocked')], default='E', max_length=1)),
                ('add_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_status',
            field=models.CharField(choices=[('S', 'Student'), ('E', 'Expert'), ('T', 'Tutor'), ('A', 'Architect'), ('W', 'Wizard')], default='S', max_length=1),
        ),
    ]
