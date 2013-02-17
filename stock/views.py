# -*- coding: utf-8 -*-
from stock.models import Article
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect

def find_article(request, article_ean):
    if article_ean:
        try:
            article = get_object_or_404(Article, ean=article_ean)
        except Http404:
            article = None
    else:
        article = None
    return render(request, "stock/search_article.html", {
                                     "article" : article
                                     },
                             )

def remove_article(request):    
    if request.POST:
        try:
            article = Article.objects.get(ean=request.POST["ean"][:-1])
            #article.stock -= 1
            #article.save()
            return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean": article.ean }))
        except (KeyError, Article.DoesNotExist):
            return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean":""}))
    else:
        return HttpResponseRedirect(reverse("stock.views.find_article", kwargs={"article_ean":""}))

