# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-21 06:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('product', '0002_auto_20170616_1000'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userprofile', '0001_initial'),
        ('discount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='orderhistoryentry',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='order.Order', verbose_name='order'),
        ),
        migrations.AddField(
            model_name='orderhistoryentry',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='delivery_group',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.DeliveryGroup', verbose_name='delivery group'),
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='product.Product', verbose_name='product'),
        ),
        migrations.AddField(
            model_name='ordereditem',
            name='stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.Stock', verbose_name='stock'),
        ),
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='userprofile.Address', verbose_name='billing address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_address',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='userprofile.Address', verbose_name='shipping address'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='order',
            name='voucher',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='discount.Voucher', verbose_name='voucher'),
        ),
        migrations.AddField(
            model_name='deliverygroup',
            name='order',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='order.Order'),
        ),
    ]
