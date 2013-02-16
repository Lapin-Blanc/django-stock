from django.conf.urls import patterns, include, url
from django.views.generic.list_detail import object_detail
from stock.models import Article

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # stock
    url(r'^stock/article/(?P<object_id>\d+)/$', object_detail, {'queryset' : Article.objects.all()}),
    # docuemnts
    url(r'^documents/barcodepage/(?P<page_id>\d+)/$', 'documents.views.print_barcode_page'),
)
