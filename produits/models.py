# -*- coding: utf-8 -*-
from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

#####################
# Fournisseurs
#####################
class Fournisseur(models.Model):
    nom = models.CharField(max_length=200,
        help_text="Le nom complet du fournisseur")
    nom_court = models.SlugField("Nom abrégé", max_length=50,
        help_text="Le nom abrégé du fournisseur, généré automatiquement")
    contact = models.CharField(max_length=200, blank=True)
    telephone = models.CharField("Téléphone", max_length=20)
    fax = models.CharField(max_length=20)
    email = models.EmailField("E-Mail", blank=True,
        help_text="L'adresse mail où envoyer les commandes, facultative.")

    class Meta:
        ordering = ["nom",]

    def __unicode__(self):
        return self.nom


#####################
# Produits
#####################
def validate_ean(value):
    if not len(value)==12:
        raise ValidationError(u"Le code EAN %s n'a pas la longueur requise (12)" % value)
    if not value.isdigit():
        raise ValidationError(u"Le code EAN %s n'est pas composé que de chiffres" % value)

def get_next_ean():
    l = [int(p.ean[3:]) for p in Produit.objects.all() if p.ean[:3]=="299"]
    if l:
        next = max(l)+1
    else:
        next = 1
    return u"299" + "%09d" % next


class Produit(models.Model):
    TVA_CHOICES = (
        (Decimal(".06"), '6%'),
        (Decimal(".21"), '21%'),
    )
    nom = models.CharField(max_length=200,
        help_text="Le nom complet du produit")
    nom_court = models.SlugField("Nom abrégé", max_length=50,
        help_text="Le nom abrégé du produit, généré automatiquement")
    prix_achat = models.DecimalField("Prix d'achat", max_digits=8, decimal_places=2)
    prix_vente = models.DecimalField("Prix de vente", max_digits=8, decimal_places=2)
    tva = models.DecimalField("Taux de TVA", max_digits=2, decimal_places=2, default=.21, choices=TVA_CHOICES)
    stock = models.IntegerField(help_text="Quantité d'article restant en stock")
    seuil = models.IntegerField(default=5, help_text="Seuil à partir duquel réapprovisionner automatiquement l'article")
    lot = models.IntegerField(default=10, help_text="Quantité à recommander par défaut")
    fournisseur = models.ForeignKey(Fournisseur)
    ean = models.CharField(max_length=12, validators=[validate_ean,], unique=True, default=get_next_ean,
        help_text="Le code EAN13 du produit, soit 12 chiffres. Proposé automatiquement. Devrait commencer par 299 pour les codes internes.")

    class Meta:
        ordering = ["nom",]
    
    def __unicode__(self):
        return self.nom

    def approvisionnement(self):
        return self.stock > self.seuil
    approvisionnement.boolean = True

######################
# Ticket
######################
class Ticket(models.Model):
    moment = models.DateTimeField(default=timezone.now())
    auteur = models.ForeignKey(User)
    total = models.DecimalField("Total pour ce ticket", max_digits=8, decimal_places=2, blank=True, null=True)
    
    class Meta:
        ordering = ["-moment",]
    
    def __unicode__(self):
        return u"%s - %s" % (self.moment, self.auteur)
    
    def save(self, *args, **kwargs):
        self.total = self.mouvementticket_set.aggregate(models.Sum("total_ttc"))['total_ttc__sum']
        super(Ticket, self).save(*args, **kwargs)

##########################
# Mouvement
##########################
class Mouvement(models.Model):
    auteur = models.ForeignKey(User)
    moment = models.DateTimeField(default=timezone.now())
    produit = models.ForeignKey(Produit)
    qte = models.IntegerField("Quantité",
        help_text="La quantité liée à ce mouvement, NEGATIVE pour une entrée en stock, POSITIVE pour une sortie !")

    class Meta:
        ordering = ["-moment",]

    def __unicode__(self):
        return u"%s, %s, %s, %s" % (timezone.localtime(self.moment), self.auteur, self.produit, self.qte)

    def save(self, *args, **kwargs):
        if not self.id: # le sotck n'est mis à jour que sur la création d'un mouvement
            self.produit.stock -= self.qte # le mouvement par défaut est un retrait, il faut une quantité négative pour une entrée en stock !!!
            self.produit.save()
        super(Mouvement, self).save(*args, **kwargs)

#############################
# Mouvement ticket
#############################
class MouvementTicket(Mouvement):
    ticket = models.ForeignKey(Ticket)
    total_htva = models.DecimalField("Total hors TVA", max_digits=8, decimal_places=2, blank=True, null=True)
    total_tva = models.DecimalField("Total TVA", max_digits=8, decimal_places=2, blank=True, null=True)
    total_ttc = models.DecimalField("Total TVA comprise", max_digits=8, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.auteur = self.ticket.auteur
        self.total_htva = self.qte * self.produit.prix_vente
        self.total_tva = self.total_htva * (1+self.produit.tva)
        self.total_ttc = self.total_htva + self.total_tva
        super(MouvementTicket, self).save(*args, **kwargs) 
        self.ticket.save() # Pour mettre à jour le total sur le ticket

    def prix_unitaire(self):
        from django.utils.formats import localize
        return localize(self.produit.prix_vente)
    prix_unitaire.verbose_name = "Prix unitaire"
