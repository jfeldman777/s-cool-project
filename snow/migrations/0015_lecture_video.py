# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-22 13:53
from __future__ import unicode_literals

from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('snow', '0014_course_examrecord_lecture_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='video',
            field=smartfields.fields.FileField(null=True, upload_to=''),
        ),
    ]
