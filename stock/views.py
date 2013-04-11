# -*- coding: utf-8 -*-
from stock.models import Article
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from stock.models import Mouvement, Article, Ticket
from django.contrib.auth.decorators import login_required

from django.core import serializers

@login_required
def find_article(request, article_ean, action):
    if article_ean:
        try:
            article = get_object_or_404(Article, ean=article_ean)
        except Http404:
            article = None
    else:
        article = None
    return render(request, "stock/search_article.html", {
                                     "article" : article,
                                     "action" : action,
                                     },
                             )

@login_required
def manage_article(request, action):    
    if request.POST:
        try:
            ean = request.POST["ean"]
            if len(ean)==13:
                ean = ean[:-1]
            article = Article.objects.get(ean=ean)
            qty = request.POST.get("qty", None)
            if qty and qty.isdigit():
               qty = int(qty)
            else:
               qty = 0
            if not action=="display":
                if action=="add":
                    qty = -qty
                m = Mouvement(auteur=request.user, article=article, qte = qty)
                m.save() 
            return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean": article.ean, "action": action}))
        except (KeyError, Article.DoesNotExist):
            return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean":"", "action": action}))
    else:
        return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean":"", "action": action}))

@login_required
def ticket(request):
    articles_json = serializers.serialize("json",Article.objects.all())
    return render(request, "stock/ticket_form.html", {"articles_json" : articles_json})

@login_required
def validate_ticket(request):
    ticket = Ticket(auteur=request.user)
    ticket.save()
    index = [i[7:] for i in request.POST if i.find("article")==0]
    nb_articles = len(index)
    for i in index:
        qty = request.POST["qty"+i]
        ean = request.POST["article"+i]
        article = Article.objects.get(ean=ean)
        ticket.mouvementticket_set.create(qte=int(qty), article=article)
    return HttpResponseRedirect("/stock/ticket/%s/" % ticket.id)

