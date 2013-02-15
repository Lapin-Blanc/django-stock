from django.contrib import admin
from produits.models import Fournisseur, Produit, Mouvement, Ticket, MouvementTicket

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
    list_filter = ["fournisseur__nom"]
    search_fields = ["nom", "fournisseur__nom"]

class MouvementAdmin(admin.ModelAdmin):
    list_display = ["moment", "auteur", "produit", "qte"]

class MouvementTicketInline(admin.TabularInline):
    fields = ["produit", "qte", "prix_unitaire", "total_htva", "total_tva", "total_ttc"]
    readonly_fields = ["prix_unitaire", "total_htva", "total_tva", "total_ttc"]
    model = MouvementTicket
    extra = 0

class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["total",]
    inlines = [MouvementTicketInline,]

admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Mouvement, MouvementAdmin)
admin.site.register(Ticket, TicketAdmin)
