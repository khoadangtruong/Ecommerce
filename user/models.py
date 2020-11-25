from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=255, blank=True) 
    country = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')

    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + '[' + self.user.username + ']'
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'
