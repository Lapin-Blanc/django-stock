from django.conf.urls import patterns, include, url
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template
from stock.models import Article

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # stock
    url(r'^stock/article/(?P<object_id>\d+)/$', object_detail, {'queryset' : Article.objects.all()}),
    url(r'^stock/article/(?P<action>display|add|remove)/(?P<article_ean>|\d{6,})$', "stock.views.find_article"),
    url(r'^stock/article/do/(?P<action>display|add|remove)/$', "stock.views.manage_article"),
    # docuemnts
    url(r'^documents/barcodepage/(?P<page_id>\d+)/$', 'documents.views.print_barcode_page'),
    
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', {'login_url' : '/accounts/login/?next=/'}),
    
    url(r'^$', 'django_shop.views.index'),

)
