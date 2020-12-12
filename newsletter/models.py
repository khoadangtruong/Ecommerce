from django.db import models
from django.forms import ModelForm

# Create your models here.
class NewsletterUser(models.Model):
    email = models.EmailField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class NewsletterForm(ModelForm):
    class Meta:
        model = NewsletterUser
        fields = ['email']