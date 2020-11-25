from user.models import UserProfile
from django.contrib import admin

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'country', 'image_tag']

admin.site.register(UserProfile, UserProfileAdmin)
