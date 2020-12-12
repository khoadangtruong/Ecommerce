from django.contrib import admin
from newsletter.models import NewsletterUser

# Register your models here.
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'created_at']
    list_filter = ['created_at']

admin.site.register(NewsletterUser, NewsletterAdmin)