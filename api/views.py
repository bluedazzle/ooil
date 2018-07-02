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

    def get(self, request, *args, **kwargs):
        keyword=self.request.GET.get('keyword', None)
        queryset = self.get_queryset()
        queryset = queryset.filter(belong_id=self.site.id, article_type=0)
        cls_set = Classification.objects.filter(belong_id=self.site.id)
        if keyword:
            queryset = queryset.filter(title__icontains=keyword)
            cls_set = cls_set.filter(title__icontains=keyword)
        result = [itm for itm in queryset]
        for itm in cls_set:
            result.append(itm)
        result = sorted(result, key=lambda x: x.priority, reverse=True)
        return self.render_to_response({'article_list': result})


class ArticleListView(CheckSiteMixin, StatusWrapMixin, MultipleJsonResponseMixin, ListView):
    model = Article
    paginate_by = 100

    def get_queryset(self):
        # cid = self.request.GET.get
        queryset = super(ArticleListView, self).get_queryset()
        queryset = queryset.filter(belong_id=self.site.id, cls__id=self.kwargs.get('cid'))
        return queryset


class ArticleDetailView(CheckSiteMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    model = Article
    pk_url_kwarg = 'aid'