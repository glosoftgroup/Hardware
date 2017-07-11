from django.conf.urls import url
from django.contrib.auth.decorators import login_required, permission_required

from . import views
from . import charts
from django.conf import settings
from django.conf.urls.static import static
# from wkhtmltopdf.views import PDFTemplateView


urlpatterns = [
		url(r'^$', views.sales_reports, name='sales_reports'),
		url(r'^sales/$', views.sales_list, name='sales_list'),
		url(r'^detail/(?P<pk>[0-9]+)/$', views.sales_detail, name='sale-detail'),
		url(r'^product_reports/$', views.product_reports, name='products_reports'),
		url( r'^products_search/$', views.products_search, name = 'products_search' ),
		url( r'^products_paginate/$', views.products_paginate, name = 'products_paginate' ),
		url(r'^prd/$', views.product_reorder, name='products_reorder'),
		url( r'^prs/$', views.products_reorder_search, name = 'products_reorder_search' ),
		url( r'^prp/$', views.products_reorder_paginate, name = 'products_reorder_paginate' ),

		url(r'^purchases_reports/$', views.purchases_reports, name='purchases_reports'),
		url(r'^balancesheet_reports/$', views.balancesheet_reports, name='balancesheet_reports'),
		url(r'^chart/$', views.get_dashboard_data, name='chart'), 
		url( r'^sales_search/$', views.sales_search, name = 'sales_search' ),
		url( r'^sales_paginate/$', views.sales_paginate, name = 'sales_paginate' ),
		# url( r'^chart_pdf/$', charts.chart_pdf, name = 'chart_pdf' ),
		url(r'^cpdf/(?P<image>.+)/$', charts.chart_pdf, name='chart_pdf'),
		url(r'^csv/(?P<image>.+)/$', charts.sales_export_csv, name='chart_csv'),
		# url(r'^pdf/$', PDFTemplateView.as_view(template_name='dashboard/reports/sales/charts/pdf/pdf.html',filename='my_pdf.pdf'),
			# name='chart_pdf'),

		url( r'^datechart/$', charts.sales_date_chart, name = 'sales_date_chart' ),
		url( r'^productchart/$', charts.sales_product_chart, name = 'sales_product_chart' ),
		url( r'^ptd/$', charts.get_product_sale_details, name = 'get_product_sale_details' ),
		url( r'^category/$', charts.sales_category_chart, name = 'sales_category_chart' ),
		url( r'^catd/$', charts.get_category_sale_details, name = 'get_category_sale_details' ),
		url( r'^userchart/$', charts.sales_user_chart, name = 'sales_user_chart' ),
		url( r'^utd/$', charts.get_user_sale_details, name = 'get_user_sale_details' ),
		url( r'^tellerchart/$', charts.sales_terminal_chart, name = 'sales_terminal_chart' ),
		url( r'^ttd/$', charts.get_terminal_sale_details, name = 'get_terminal_sale_details' ),
		url( r'^weekfilter/$', charts.get_sales_by_week, name = 'get_sales_by_week' ),

		# url(r'^$', permission_required('userprofile.view_user', login_url='account_login'))     
]

if settings.DEBUG:
	# urlpatterns += [ url(r'^static/(?P<path>.*)$', serve)] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)