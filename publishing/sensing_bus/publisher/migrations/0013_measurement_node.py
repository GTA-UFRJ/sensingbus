# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 17:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0012_sensingnode'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='node',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='publisher.SensingNode', verbose_name='node that collected measurement'),
            preserve_default=False,
        ),
    ]
