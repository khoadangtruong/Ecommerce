from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.fields import TextField

# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(blank=True, upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title