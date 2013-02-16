from django.db import models
from stock.models import Article

class BarcodePage(models.Model):
    titre = models.CharField(max_length=50)
    produits = models.ManyToManyField(Article)
    
    class Meta:
        verbose_name = "Page de codes-barres"
        verbose_name_plural = "Pages de codes-barres"

    def __unicode__(self):
        return self.titre
    
    def get_absolute_url(self):
        return u"/documents/barcodepage/%s/" % self.id
