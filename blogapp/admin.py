from django.contrib import admin
from blogapp.models import *
# Register your models here.
admin.site.register(ProfileName)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag', 'title', 'description', 'slug', 'created_at')
    search_fields = ('title', 'creator')



admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'slug', 'created_at')
    search_fields = ('title', 'creator')

    class Media:
        js = ("https://cdn.tiny.cloud/1/pvc4ir3y3m926ajbtvymmuia4120k3zo0k19dalsyuv591c3/tinymce/6/tinymce.min.js",
              "js/tinymce.js", )


admin.site.register(Post, PostAdmin)
