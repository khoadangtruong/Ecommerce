from django.contrib import admin
from blog.models import Blog

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_tag']
    list_filter = ['created_at',]

admin.site.register(Blog)