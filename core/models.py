# coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


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
    banner = models.ImageField(max_length=256, default='', null=True, blank=True, upload_to='banners')

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
    picture = models.ImageField(max_length=256, null=True, blank=True, default='', upload_to='banners')
    priority = models.IntegerField(default=0, choices=priority_choices)
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
    title = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='标题')
    picture = models.ImageField(max_length=256, null=True, blank=True, default='', upload_to='banners', verbose_name='标题图片')
    author = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='作者')
    content = RichTextUploadingField(default='', null=True, blank=True, verbose_name='正文')
    priority = models.IntegerField(default=0, verbose_name='优先级', choices=priority_choices)
    article_type = models.IntegerField(default=0) # 0 一级文章 1 二级文章
    belong = models.ForeignKey(Area, related_name='area_articles', verbose_name='属于')
    cls = models.ForeignKey(Classification, related_name='cls_articles', null=True, blank=True,
                            on_delete=models.SET_NULL, verbose_name='分类')

    def __unicode__(self):
        return '{0}: {1}-{2: %Y-%m-%d %H:%M:%S}'.format(self.belong.name, self.title, self.create_time)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.cls:
            self.article_type = 1
        return super(Article, self).save(force_insert, force_update, using, update_fields)
