from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db import models
from currencies.models import Currency
from django.dispatch import receiver
from allauth.account.signals import user_signed_up

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=255, blank=True) 
    country = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='images/')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.user.username
    
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + '[' + self.user.username + ']'
    
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    # @receiver(user_signed_up)
    # def populate_profile(sociallogin, user, **kwargs):

    #     user.profile = UserProfile()

    #     # if sociallogin.account.provider == 'facebook':
    #     #     user_data = user.socialaccount_set.filter(provider='facebook')[0].extra_data
    #     #     picture_url = "http://graph.facebook.com/" + sociallogin.account.uid + "/picture?type=large"
    #     #     email = user_data['email']
    #     #     full_name = user_data['name']

    #     if sociallogin.account.provider == 'google':
    #         user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
    #         image_url = user_data.get('image')
    #         email = user_data.get('email')

        #     user.profile.image = image_url
        #     user.profile.email = email
        #     user.profile.save()
            