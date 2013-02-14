from django.contrib import admin
from produits.models import Fournisseur, Produit

class ProduitInline(admin.TabularInline):
    model = Produit
    extra = 0

class FournisseurAdmin(admin.ModelAdmin):
    prepopulated_fields = {"nom_court":('nom',)}
    list_display = ["nom", "contact", "telephone", "fax", "email"]
    search_fields = ["nom", "contact"]

    inlines = [ProduitInline,]

class ProduitAdmin(admin.ModelAdmin):
    prepopulated_fields = {"nom_court":('nom',)}
    list_display = ["nom", "fournisseur", "prix_achat", "prix_vente", "tva", "stock", "seuil", "approvisionnement"]
    search_fields = ["nom", "fournisseur"]

admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Produit, ProduitAdmin)
