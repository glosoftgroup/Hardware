# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-23 11:11
from __future__ import unicode_literals

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solditem',
            name='order',
            field=models.IntegerField(default=Decimal('1')),
        ),
    ]