from django.contrib import admin
from documents.models import BarcodePage

class BarcodePageAdmin(admin.ModelAdmin):
    filter_horizontal = ["produits",]

admin.site.register(BarcodePage, BarcodePageAdmin)
