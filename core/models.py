# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone


# Create your models here.


class BaseModel(models.Model):
    create_time = models.DateTimeField(default=timezone.now)
    modify_time = models.DateTimeField(auto_now=True)
    original_create_time = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        abstract = True


class Area(BaseModel):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)
    banner = models.CharField(max_length=256, default='', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Classification(BaseModel):
    priority_choices = [
        (0, '最低优'),
        (1, '低优'),
        (2, '普通'),
        (3, '高优'),
        (4, '最高优'),
    ]
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True, default='')
    picture = models.CharField(max_length=256, null=True, blank=True, default='')
    priority = models.IntegerField(default=0)
    article_type = models.IntegerField(default=1)
    belong = models.ForeignKey(Area, related_name='area_fir_cls')

    def __unicode__(self):
        return '{0}：{1}'.format(self.belong.name, self.title)


class Article(BaseModel):
    priority_choices = [
        (0, '最低优'),
        (1, '低优'),
        (2, '普通'),
        (3, '高优'),
        (4, '最高优'),
    ]
    title = models.CharField(max_length=50, default='', null=True, blank=True)
    picture = models.CharField(max_length=256, null=True, blank=True, default='')
    author = models.CharField(max_length=50, default='', null=True, blank=True)
    content = models.TextField(default='', null=True, blank=True)
    priority = models.IntegerField(default=0)
    article_type = models.IntegerField(default=0) # 0 一级文章 1 二级文章
    belong = models.ForeignKey(Area, related_name='area_articles')
    cls = models.ForeignKey(Classification, related_name='cls_articles', null=True, blank=True,
                            on_delete=models.SET_NULL)

    def __unicode__(self):
        return '{0}: {1}-{2: %Y-%m-%d %H:%M:%S}'.format(self.belong.name, self.title, self.create_time)
