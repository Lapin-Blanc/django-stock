from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    
    # docuemnts
    url(r'^documents/barcodepage/(?P<page_id>\d+)/$', 'documents.views.print_barcode_page'),
)
