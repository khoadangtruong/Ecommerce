from django.contrib import admin
from home.models import Setting, ContactMessage

class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'address', 'email']

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']

admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Setting, SettingAdmin)