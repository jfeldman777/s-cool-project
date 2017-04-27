# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-14 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('snow', '0025_auto_20170414_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('books', models.ManyToManyField(to='snow.Course')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='arc.Cat')),
                ('siblings', models.ManyToManyField(related_name='_cat_siblings_+', to='arc.Cat')),
            ],
        ),
    ]