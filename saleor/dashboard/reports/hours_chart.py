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

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import User
from ...sale.models import Sales, SoldItem
from ...product.models import Product, ProductVariant
from ...decorators import permission_decorator, user_trail

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')


def get_hours_results(date, l, h):
	try:
		sales_at_date = Sales.objects.filter(created__contains=date)
		sales_at_h = sales_at_date.filter(created__hour__range=[l,h])
		try:
			amount = Sales.objects.filter(pk__in=sales_at_h).aggregate(Sum('total_net'))['total_net__sum']
			if amount is not None:
				return amount
			else:
				amount = 0
				return amount
		except ObjectDoesNotExist:
			amount = 0
			return amount
	except ObjectDoesNotExist:
		amount = 0
		return amount