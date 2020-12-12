from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from newsletter.models import NewsletterUser, NewsletterForm

# Create your views here.
def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            if NewsletterUser.objects.filter(email = instance.email).exists():
                messages.warning(request, 'Your email allready subscribed!')
                return HttpResponseRedirect('/subscribe')
            else:
                instance.save()
                messages.success(request, 'Thank you for your subscription!')
            
                subject = 'Thank You For Joining Newsletter.'
                from_email = settings.EMAIL_HOST_USER
                to_email = [instance.email]
                signup_message = 'Welcome To OneTech Website'
                send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)

                return HttpResponseRedirect('/subscribe')

    form = NewsletterForm
        
    context = {
        'form': form,
    }

    return render(request, 'subscribe.html', context)

def newsletter_unsubscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit = False)
            if NewsletterUser.objects.filter(email = instance.email).exists():
                NewsletterUser.objects.filter(email = instance.email).delete()
                messages.success(request, 'Your email has been removed!')
                
                subject = 'You have been unsubscribe! '
                from_email = settings.EMAIL_HOST_USER
                to_email = [instance.email]
                signup_message = 'Sorry to see you go. Let us if there is an issue.'
                send_mail(subject=subject, from_email=from_email, recipient_list=to_email, message=signup_message, fail_silently=False)

                return HttpResponseRedirect('/unsubscribe')
            else:
                messages.warning(request, 'Sorry but we did not find your email address!')
                return HttpResponseRedirect('/unsubscribe')

    
    form = NewsletterForm
        
    context = {
        'form': form,
    }

    return render(request, 'unsubscribe.html', context)