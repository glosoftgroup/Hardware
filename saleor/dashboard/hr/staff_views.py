from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
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

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import User
from ...supplier.models import Supplier
from ...customer.models import Customer
from ...sale.models import Sales, SoldItem, Terminal
from ...product.models import Product, ProductVariant, Category
from ...decorators import permission_decorator, user_trail
from ...utils import render_to_pdf, convert_html_to_pdf


def list_staff(request):
    users = User.objects.all()
    data = {
        "users":users
    }
    return TemplateResponse(request, 'dashboard/hr/staff/list.html',{})

def staff_detail(request):
    status = 'read'
    return TemplateResponse(request, 'dashboard/hr/staff/staff.html', {})

def add_staff(request):
    suppliers = Supplier.objects.all()
    customers = Customer.objects.all()
    staff = User.objects.all()
    data = {
        "suppliers":suppliers,
        "customers":customers,
        "staff":staff
    }
    return TemplateResponse(request, 'dashboard/hr/staff/add_staff.html', data)

def staff_edit(request, pk=None):
    return TemplateResponse(request, 'dashboard/hr/staff/edit_staff.html', {})

def staff_delete(request, pk=None):
    return TemplateResponse(request, 'dashboard/hr/staff/delete_staff.html', {})