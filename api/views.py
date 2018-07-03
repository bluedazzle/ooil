# coding: utf-8
from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.views.generic import DetailView
from django.views.generic import ListView

from core.Mixin.CheckMixin import CheckSiteMixin
from core.Mixin.StatusWrapMixin import StatusWrapMixin
from core.dss.Mixin import MultipleJsonResponseMixin, JsonResponseMixin
from core.models import *


class IndexArticleListView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, ListView):
    model = Article
    static_root = '/static/media/'
    exclude_attr = ['content']

    def get(self, request, *args, **kwargs):
        keyword = self.request.GET.get('keyword', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(belong_id=self.site.id, article_type=0)
        cls_set = Classification.objects.filter(belong_id=self.site.id)
        if keyword:
            queryset = self.get_queryset().filter(belong_id=self.site.id, title__icontains=keyword)
            cls_set = cls_set.filter(title__icontains=keyword)
        result = [itm for itm in queryset]
        for itm in cls_set:
            result.append(itm)
        result = sorted(result, key=lambda x: x.priority, reverse=True)
        return self.render_to_response({'article_list': result, "is_paginated": False})


class ArticleListView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Article
    paginate_by = 100
    static_root = '/static/media/'
    exclude_attr = ['content']

    def get_queryset(self):
        # cid = self.request.GET.get
        queryset = super(ArticleListView, self).get_queryset()
        queryset = queryset.filter(belong_id=self.site.id, cls__id=self.kwargs.get('cid'))
        return queryset


# class ArticleCreateView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
#     model = Article
#     http_method_names = ['post']
#
#     def post(self, request, *args, **kwargs):
#         author = request.POST.get('author')
#         content = request.POST.get('content')
#
#
# class ClassificationCreateView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
#     model = Classification
#     http_method_names = ['post']


class ArticleDetailView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Article
    static_root = '/static/media/'
    pk_url_kwarg = 'aid'


class AreaDetailView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Area
    static_root = '/static/media/'
    # pk_url_kwarg = 'aid'

    def get_object(self, queryset=None):
        objs = self.model.objects.filter(slug=self.site_slug)
        if objs.exists():
            return objs[0]
        return None
