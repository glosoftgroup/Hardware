from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.utils.translation import pgettext_lazy
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.db.models import Q

from ...core.utils import get_paginator_items
from ..views import staff_member_required
from ...userprofile.models import User, UserTrail
from ...customer.models import Customer
from ...decorators import permission_decorator, user_trail
import logging

debug_logger = logging.getLogger('debug_logger')
info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

@staff_member_required
# @permission_decorator('userprofile.view_user')
def users(request):
	try:
		users = Customer.objects.all().order_by('-id')
		page = request.GET.get('page', 1)
		paginator = Paginator(users, 10)
		try:
			users = paginator.page(page)
		except PageNotAnInteger:
			users = paginator.page(1)
		except InvalidPage:
			users = paginator.page(1)
		except EmptyPage:
			users = paginator.page(paginator.num_pages)
		user_trail(request.user.name, 'accessed customers page', 'view')
		info_logger.info('User: ' + str(request.user.name) + 'view customers')
		if request.GET.get('initial'):
			return HttpResponse(paginator.num_pages)
		else:
			return TemplateResponse(request, 'dashboard/customer/users.html',{'users': users, 'pn': paginator.num_pages})
	except TypeError as e:
		error_logger.error(e)
		return TemplateResponse(request, 'dashboard/customer/users.html', {'users': users, 'pn': paginator.num_pages})

@staff_member_required
@permission_decorator('userprofile.add_user')
def user_add(request):
	try:
		user_trail(request.user.name, 'accessed add customer page', 'view')
		info_logger.info('User: ' + str(request.user.name) + 'accessed add customer page')
		return TemplateResponse(request, 'dashboard/customer/add_user.html',{'permissions':"permissions", 'groups':"groups"})
	except TypeError as e:
		error_logger.error(e)
		return HttpResponse('error accessing add users page')

@staff_member_required
@csrf_exempt
def user_process(request):
	user = User.objects.all()
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')
		# password = request.POST.get('password')
		# encr_password = make_password(password)

		mobile = request.POST.get('mobile')
		image= request.FILES.get('image')
		groups = request.POST.getlist('groups[]')
		new_user = Customer.objects.create(
			name = name,
			email = email,			

			mobile = mobile,
			image = image
		)
		try:
			new_user.save()
		except:
			error_logger.info('Error when saving ')
		last_id = Customer.objects.latest('id')
		if groups:
			permissions = Permission.objects.filter(group__name__in=groups)
			last_id.user_permissions.add(*permissions)
			gps = Group.objects.filter(name__in=groups)
			last_id.groups.add(*gps)
			last_id.save()
		user_trail(request.user.name, 'created customer: '+str(name),'add')
		info_logger.info('User: '+str(request.user.name)+' created customer:'+str(name))
		return HttpResponse(last_id.id)

def user_detail(request, pk):
	user = get_object_or_404(Customer, pk=pk)
	user_trail(request.user.name, 'accessed detail page to view customer: ' + str(user.name), 'view')
	info_logger.info('User: ' + str(request.user.name) + ' accessed detail page to view customer:' + str(user.name))
	return TemplateResponse(request, 'dashboard/customer/detail.html', {'user':user})

def user_delete(request, pk):
	user = get_object_or_404(Customer, pk=pk)
	if request.method == 'POST':
		user.delete()
		user_trail(request.user.name, 'deleted customer: '+ str(user.name))
		return HttpResponse('success')
def user_edit(request, pk):
	user = get_object_or_404(Customer, pk=pk)		
	ctx = {'user': user}
	user_trail(request.user.name, 'accessed edit page for customer '+ str(user.name),'update')
	info_logger.info('User: '+str(request.user.name)+' accessed edit page for customer: '+str(user.name))
	return TemplateResponse(request, 'dashboard/customer/edit_user.html', ctx)

def user_update(request, pk):
	user = get_object_or_404(Customer, pk=pk)
	if request.method == 'POST':
		name = request.POST.get('name')
		email = request.POST.get('email')		
		nid = request.POST.get('nid')
		mobile = request.POST.get('mobile')
		image= request.FILES.get('image')		
		if image :
			user.name = name
			user.email = email			
			user.nid = nid
			user.mobile = mobile
			user.image = image
			user.save()
			user_trail(request.user.name, 'updated customer: '+ str(user.name))
			info_logger.info('User: '+str(request.user.name)+' updated customer: '+str(user.name))
			return HttpResponse("success with image")
		else:
			user.name = name
			user.email = email			
			user.nid = nid
			user.mobile = mobile
			user.save()
			user_trail(request.user.name, 'updated customer: '+ str(user.name))
			info_logger.info('User: '+str(request.user.name)+' updated customer: '+str(user.name))
			return HttpResponse("success without image")


def customer_pagination(request):
	page = int(request.GET.get('page', 1))
	list_sz = request.GET.get('size')
	p2_sz = request.GET.get('psize')
	select_sz = request.GET.get('select_size')

	users = Customer.objects.all().order_by('-id')
	if list_sz:
		paginator = Paginator(users, int(list_sz))
		users = paginator.page(page)
		return TemplateResponse(request, 'dashboard/customer/pagination/p2.html',
								{'users':users, 'pn': paginator.num_pages, 'sz': list_sz, 'gid': 0})
	else:
		paginator = Paginator(users, 10)
	if p2_sz:
		paginator = Paginator(users, int(p2_sz))
		users = paginator.page(page)
		return TemplateResponse(request, 'dashboard/customer/pagination/paginate.html', {"users":users})

	try:
		users = paginator.page(page)
	except PageNotAnInteger:
		users = paginator.page(1)
	except InvalidPage:
		users = paginator.page(1)
	except EmptyPage:
		users = paginator.page(paginator.num_pages)
	return TemplateResponse(request, 'dashboard/customer/pagination/paginate.html', {"users":users})

@staff_member_required
def customer_search(request):
	if request.is_ajax():
		page = request.GET.get('page', 1)
		list_sz = request.GET.get('size', 10)
		p2_sz = request.GET.get('psize')
		q = request.GET.get('q')
		if list_sz is None:
			sz = 10
		else:
			sz = list_sz

		if q is not None:
			queryset_list = Customer.objects.filter(
				Q(name__icontains=q)|
				Q(email__icontains=q) |
				Q(mobile__icontains=q)
			).order_by('-id')
			paginator = Paginator(queryset_list, 10)

			try:
				queryset_list = paginator.page(page)
			except PageNotAnInteger:
				queryset_list = paginator.page(1)
			except InvalidPage:
				queryset_list = paginator.page(1)
			except EmptyPage:
				queryset_list = paginator.page(paginator.num_pages)
			users = queryset_list
			if p2_sz:
				users = paginator.page(page)
				return TemplateResponse(request, 'dashboard/customer/pagination/paginate.html', {"users":users})

			return TemplateResponse(request, 'dashboard/customer/pagination/search.html',
			{"users":users, 'pn': paginator.num_pages, 'sz': sz, 'q': q})


		