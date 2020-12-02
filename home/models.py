from django.forms import ModelForm, TextInput, Textarea
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    title = models.CharField(max_length = 512)
    keywords = models.CharField(max_length = 512)
    description = models.CharField(max_length = 1000)
    company = models.CharField(max_length = 512)
    address = models.CharField(blank = True, max_length = 512)
    phone = models.CharField(max_length = 12)
    fax = models.CharField(blank = True, max_length = 20)
    email = models.EmailField(max_length = 512)
    smtpserver = models.CharField(blank = True, max_length = 512)
    smtpemail = models.CharField(blank=True,max_length = 512)
    smtppassword = models.CharField(blank=True,max_length = 512)
    smtpport = models.CharField(blank=True,max_length = 20)
    icon = models.ImageField(blank=True,upload_to = 'images/')
    facebook = models.CharField(blank=True,max_length = 50)
    instagram = models.CharField(blank=True,max_length = 50)
    twitter = models.CharField(blank=True,max_length = 50)
    youtube = models.CharField(blank=True, max_length = 50)
    aboutus = RichTextUploadingField(blank = True)
    contact = RichTextUploadingField(blank = True)
    references = RichTextUploadingField(blank = True)
    status = models.CharField(max_length=10,choices = STATUS)
    create_at = models.DateTimeField(auto_now_add = True)
    update_at = models.DateTimeField(auto_now = True)

    def __str__(self):
        return self.title

class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    subject = models.CharField(max_length=255, blank=True)
    message = models.TextField(max_length=512, blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    ip = models.CharField(max_length=255, blank=True)
    note = models.CharField(max_length=255, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'subject', 'email', 'message']

class FAQ(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    ) 
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=255)
    answer = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question