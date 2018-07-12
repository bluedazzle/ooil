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
    title = models.CharField(max_length=100, default='', verbose_name='网页标题')
    name = models.CharField(max_length=50, verbose_name='地区名称')
    slug = models.CharField(max_length=50, unique=True, verbose_name='唯一识别码')
    banner = models.ImageField(max_length=256, default='', null=True, blank=True, upload_to='banners',
                               verbose_name='地区封面图')
    description = models.CharField(max_length=100, default='', null=True, blank=True, verbose_name='摘要')
    wx_app_id = models.CharField(max_length=64, null=True, blank=True)
    wx_secret = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '地区'
        verbose_name_plural = '地区'


class Classification(BaseModel):
    priority_choices = [
        (0, '最低优'),
        (1, '低优'),
        (2, '普通'),
        (3, '高优'),
        (4, '最高优'),
    ]
    title = models.CharField(max_length=100, verbose_name='分类标题')
    description = models.CharField(max_length=100, null=True, blank=True, default='', verbose_name='分类描述（选填）')
    picture = models.ImageField(max_length=256, null=True, blank=True, default='', upload_to='banners',
                                verbose_name='分类封面图')
    priority = models.IntegerField(default=0, choices=priority_choices, verbose_name='分类优先级')
    article_type = models.IntegerField(default=1)
    belong = models.ForeignKey(Area, related_name='area_fir_cls', verbose_name='分类属于')

    def __unicode__(self):
        return '{0}：{1}'.format(self.belong.name, self.title)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'


class Article(BaseModel):
    priority_choices = [
        (0, '最低优'),
        (1, '低优'),
        (2, '普通'),
        (3, '高优'),
        (4, '最高优'),
    ]
    title = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='标题')
    description = models.CharField(max_length=200, default='', null=True, blank=True, verbose_name='简介')
    picture = models.ImageField(max_length=256, null=True, blank=True, default='', upload_to='banners',
                                verbose_name='标题图片')
    author = models.CharField(max_length=50, default='', null=True, blank=True, verbose_name='作者')
    content = RichTextUploadingField(default='', null=True, blank=True, verbose_name='正文')
    priority = models.IntegerField(default=0, verbose_name='优先级', choices=priority_choices)
    article_type = models.IntegerField(default=0)  # 0 一级文章 1 二级文章
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

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
