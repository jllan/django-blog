from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, View
from pure_pagination import Paginator
from .models import *
from django.conf import settings
from datetime import datetime
import time
import json
import os

# Create your views here.
class IndexView(View):
    def get(self, request):
        article_list = Article.objects.filter(status=0).values('id', 'title', 'url', 'abstract', 'created_time',
                                                               'category__name')
        try:
            page = int(request.GET.get('page', 1))
            page_size = Paginator(article_list, 10, request=request)
            article_list = page_size.page(page)
            print('len article_list', len(article_list.object_list))
            print('article_list',article_list.object_list)
        except Exception as e:
            return HttpResponseRedirect('/')

        for article in article_list.object_list:
            tags = list(Article.objects.filter(title=article['title']).values_list('tags__name', flat=True))
            print('tags:', tags)
            article['tags'] = tags

        category_list = Category.objects.all()
        for category in category_list:
            count = Article.objects.filter(category__name=category.name).count()
            category.count = count

        links = Link.objects.all()

        return render(request, 'index.html', {
            'article_list': article_list,
            'category_list': category_list,
            'links': links
        })

class ArticleView(View):
    def get(self, request, article_url):
        try:
            article_url = int(article_url)
            article = Article.objects.filter(id=article_url, status=0).first()
            return HttpResponseRedirect('/article/{}'.format(article_url))
        except Exception as e:
            article = Article.objects.filter(url=article_url, status=0).first()
        if not article:
            return HttpResponseRedirect('/404')
        tags = list(Article.objects.filter(title=article.title).values_list('tags__name', flat=True))
        return render(request, 'article.html', locals())


class CategoryListVIew(View):
    def get(self, request, category_name):
        archive_list = list(
            Article.objects.filter(category__name=category_name, status=0).values('url', 'title', 'created_time'))
        if len(archive_list) == 0:
            return HttpResponseRedirect('/404')

        category_list = Category.objects.all()
        # 添加分类次数
        for category in category_list:
            count = Article.objects.filter(category__id=category.id).count()
            category.count = count
        # 友情链接
        links = Link.objects.all()
        return render(request, 'category.html', locals())

class TagListVIew(View):
    def get(self, request, tag_name):
        archive_list = list(
            Article.objects.filter(tags__name=tag_name, status=0).values('url', 'title', 'created_time'))
        if len(archive_list) == 0:
            return HttpResponseRedirect('/404')

        category_list = Category.objects.all()
        # 添加分类次数
        for category in category_list:
            count = Article.objects.filter(category__id=category.id).count()
            category.count = count
        # 友情链接
        links = Link.objects.all()
        return render(request, 'category.html', locals())


class AboutView(View):
    def get(self, request):
        article = Article.objects.filter(id=1).first()
        return render(request, 'about.html', locals())
