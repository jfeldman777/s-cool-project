# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 10:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snow', '0019_course_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examrecord',
            name='in_0',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='in_1',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='in_2',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='in_3',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='in_4',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='in_5',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_0',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_1',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_2',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_3',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_4',
        ),
        migrations.RemoveField(
            model_name='examrecord',
            name='out_5',
        ),
        migrations.AddField(
            model_name='examrecord',
            name='current',
            field=models.IntegerField(default=0),
        ),
    ]
