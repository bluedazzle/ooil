from django.contrib import admin
from core.models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("create_time", 'article_type', 'original_create_time')
        form = super(ArticleAdmin, self).get_form(request, obj, **kwargs)
        return form


class AreaAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("create_time", 'modify_time', 'original_create_time')
        form = super(AreaAdmin, self).get_form(request, obj, **kwargs)
        return form

class ClassificationAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ("create_time", 'modify_time', 'article_type', 'original_create_time')
        form = super(ClassificationAdmin, self).get_form(request, obj, **kwargs)
        return form

admin.site.register(Area, AreaAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Classification, ClassificationAdmin)