# -*- coding: utf-8 -*-
from stock.models import Article
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from stock.models import Mouvement
from django.contrib.auth.decorators import login_required

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
            article = Article.objects.get(ean=request.POST["ean"][:-1])
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

