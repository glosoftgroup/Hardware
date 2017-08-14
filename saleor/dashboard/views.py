from django.conf import settings
from django.contrib.admin.views.decorators import \
    staff_member_required as _staff_member_required
from django.db.models import F, Q, Sum
from django.template.response import TemplateResponse
from payments import PaymentStatus

from ..order.models import Order, Payment
from ..order import OrderStatus
from ..product.models import Product

from ..core.utils import get_paginator_items
from ..userprofile.models import User
from ..sale.models import Sales, SoldItem, Terminal
from ..product.models import Product, ProductVariant, Category
from ..decorators import permission_decorator, user_trail
from ..utils import render_to_pdf, convert_html_to_pdf

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Min, Sum, Avg, Max
from django.core import serializers
from django.template.defaultfilters import date
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import datetime
from datetime import date, timedelta
from django.utils.dateformat import DateFormat
import logging
import random
import csv
from django.utils.encoding import smart_str
from decimal import Decimal
from calendar import monthrange
import calendar
from django_xhtml2pdf.utils import generate_pdf

import re
import base64

from .reports.hours_chart import get_item_results, get_terminal_results, get_user_results, get_hours_results, get_hours_results_range, get_date_results_range, get_date_results, get_category_results

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')



def staff_member_required(f):
    return _staff_member_required(f, login_url='home')


@staff_member_required
def index(request):
    orders_to_ship = Order.objects.filter(status=OrderStatus.FULLY_PAID)
    orders_to_ship = (orders_to_ship
                      .select_related('user')
                      .prefetch_related('groups', 'groups__items', 'payments'))
    payments = Payment.objects.filter(
        status=PaymentStatus.PREAUTH).order_by('-created')
    payments = payments.select_related('order', 'order__user')
    #top categories
    cat = top_categories()
    items = top_items()
    # low stock
    low_stock = get_low_stock_products()

    ctx = {'preauthorized_payments': payments,
           'orders_to_ship': orders_to_ship,
           'low_stock': low_stock,
           #top_cat
           "sales_by_category": cat['sales_by_category'],
           "categs": cat['categs'],
           "avg": cat['avg'],
           "labels": cat['labels'],
           "default": cat['default'],
           "hcateg": cat['hcateg'],
           "date_total_sales": cat['date_total_sales'],

           #items
           "sales_by_item": items['sales_by_item'],
           "items": items['items'],
           "items_avg": items['items_avg'],
           "items_labels": items['items_labels'],
           "items_default": items['items_default'],
           "items_hcateg": items['items_hcateg'],
           }
    return TemplateResponse(request, 'dashboard/index.html', ctx)

def top_categories():
    today = datetime.datetime.now()
    try:
        last_sale = Sales.objects.latest('id')
        date = DateFormat(last_sale.created).format('Y-m-d')
    except:
        date = DateFormat(datetime.datetime.today()).format('Y-m-d')


    if date:
        try:
            sales_by_category = SoldItem.objects.filter(sales__created__contains=date).values('product_category').annotate(
                c=Count('product_category', distinct=True)).annotate(Sum('total_cost')).order_by('-total_cost__sum')[:5]
            sales_by_category_totals = sales_by_category.aggregate(Sum('total_cost__sum'))['total_cost__sum__sum']
            new_sales = []
            for sales in sales_by_category:
                color = "#%03x" % random.randint(0, 0xFFF)
                sales['color'] = color
                percent = (Decimal(sales['total_cost__sum']) / Decimal(sales_by_category_totals)) * 100
                percentage = round(percent, 2)
                sales['percentage'] = percentage
                for s in range(0, sales_by_category.count(), 1):
                    sales['count'] = s
                new_sales.append(sales)
            categs = Category.objects.all()
            this_year = today.year
            avg_m = Sales.objects.filter(created__year=this_year).annotate(c=Count('total_net'))
            highest_category_sales = new_sales[0]['product_category']
            default = []
            labels = []
            for i in range(1, (today.month + 1), 1):
                if len(str(i)) == 1:
                    m =  str('0' + str(i))
                else:
                    m = str(i)
                amount = get_category_results(highest_category_sales, str(today.year), m)
                labels.append(calendar.month_name[int(m)][0:3])
                default.append(amount)

            date_total_sales = Sales.objects.filter(created__contains=date).aggregate(Sum('total_net'))[
                'total_net__sum']


            data = {
                "sales_by_category": new_sales,
                "categs": categs,
                "avg": avg_m,
                "labels": labels,
                "default": default,
                "hcateg": highest_category_sales,
                "date_total_sales": date_total_sales
            }
            return data
        except Exception,e:
            error_logger.error(e)
            return HttpResponse(e)

def top_items():
    today = datetime.datetime.now()
    try:
        last_sale = Sales.objects.latest('id')
        date = DateFormat(last_sale.created).format('Y-m-d')
    except:
        date = DateFormat(datetime.datetime.today()).format('Y-m-d')

    if date:
        try:
            sales_by_category = SoldItem.objects.filter(sales__created__contains=date).values('product_name').annotate(
                c=Count('product_name', distinct=True)).annotate(Sum('total_cost')).order_by('-total_cost__sum')[:5]
            sales_by_category_totals = sales_by_category.aggregate(Sum('total_cost__sum'))['total_cost__sum__sum']
            new_sales = []
            for sales in sales_by_category:
                color = "#%03x" % random.randint(0, 0xFFF)
                sales['color'] = color
                percent = (Decimal(sales['total_cost__sum']) / Decimal(sales_by_category_totals)) * 100
                percentage = round(percent, 2)
                sales['percentage'] = percentage
                for s in range(0, sales_by_category.count(), 1):
                    sales['count'] = s
                new_sales.append(sales)
            categs = SoldItem.objects.values('product_name').annotate(Count('product_name', distinct=True)).order_by()
            this_year = today.year
            avg_m = Sales.objects.filter(created__year=this_year).annotate(c=Count('total_net'))
            highest_category_sales = new_sales[0]['product_name']
            default = []
            labels = []
            for i in range(1, (today.month + 1), 1):
                if len(str(i)) == 1:
                    m = str('0' + str(i))
                else:
                    m = str(i)
                amount = get_item_results(highest_category_sales, str(today.year), m)
                labels.append(calendar.month_name[int(m)][0:3])
                default.append(amount)

            data = {
                "sales_by_item": new_sales,
                "items": categs,
                "items_avg": avg_m,
                "items_labels": labels,
                "items_default": default,
                "items_hcateg": highest_category_sales
            }
            return data
        except IndexError as e:
            error_logger.error(e)
            return HttpResponse(e)


@staff_member_required
def styleguide(request):
    return TemplateResponse(request, 'dashboard/styleguide/index.html', {})

def get_low_stock_products():
    #threshold = getattr(settings, 'LOW_STOCK_THRESHOLD', 10)
    products = Product.objects.annotate(
        total_stock=Sum('variants__stock__quantity'))
    products = products.filter(total_stock__lte=F('low_stock_threshold')).distinct()
    return products
