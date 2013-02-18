from django.contrib import admin
from stock.models import Fournisseur, Article, Mouvement, Ticket, MouvementTicket

class ArticleInline(admin.TabularInline):
    model = Article
    extra = 0

class FournisseurAdmin(admin.ModelAdmin):
    prepopulated_fields = {"nom_court":('nom',)}
    list_display = ["nom", "contact", "telephone", "fax", "email"]
    search_fields = ["nom", "contact"]

    inlines = [ArticleInline,]

class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {"nom_court":('nom',)}
    list_display = ["nom", "fournisseur", "prix_achat", "prix_vente", "tva", "stock", "seuil", "approvisionnement"]
    list_filter = ["fournisseur__nom"]
    search_fields = ["nom", "fournisseur__nom"]

class MouvementAdmin(admin.ModelAdmin):
    list_filter = ['auteur',]
    date_hierarchy = 'moment'
    list_display = ["moment", "auteur", "article", "qte"]

class MouvementTicketInline(admin.TabularInline):
    fields = ["article", "qte", "prix_unitaire", "total_htva", "total_tva", "total_ttc"]
    readonly_fields = ["prix_unitaire", "total_htva", "total_tva", "total_ttc"]
    model = MouvementTicket
    extra = 0

class TicketAdmin(admin.ModelAdmin):
    readonly_fields = ["total",]
    inlines = [MouvementTicketInline,]

admin.site.register(Fournisseur, FournisseurAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Mouvement, MouvementAdmin)
admin.site.register(Ticket, TicketAdmin)
