import random
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import Setting, ContactForm, ContactMessage, FAQ
from product.models import Product, Category, Images, Comment
from home.form import SearchForm
from django.contrib.auth.decorators import login_required
from user.models import UserProfile
from Ecommerce import settings
from order.models import ShopCart


def index(request):
    if not request.session.has_key('currency'):
        request.session['currency'] = settings.DEFAULT_CURRENCY

    setting = Setting.objects.get(pk = 1)
    products_top10 = Product.objects.all().order_by('?')[:1]
    Laptop = Product.objects.filter(category_id = 1).order_by('?')[:10]
    Smartphone = Product.objects.filter(category_id = 2).order_by('?')[:10]
    Audio = Product.objects.filter(category_id = 12).order_by('?')[:10]
    Desktop = Product.objects.filter(category_id = 8).order_by('?')[:10]
    Tablet = Product.objects.filter(category_id = 9).order_by('?')[:8]
    Gears = Product.objects.filter(category_id = 10).order_by('?')[:10]
    Watch = Product.objects.filter(category_id = 11).order_by('?')[:10]

    featured_products = Product.objects.filter(is_featured = True).order_by('?')[:10]

    best_sellers = Product.objects.all().order_by('-count_sold')[:10]
    audio_best_sellers = Product.objects.filter(category_id = 12).order_by('-count_sold')[:6]
    laptop_best_sellers = Product.objects.filter(category_id = 1).order_by('count_sold')[:8]

    page = 'home'

    popular_products =  Product.objects.all().order_by('num_visits')[1:2]
    popular_products_down =  Product.objects.all().order_by('-num_visits')[10:11]
    main_popular_products_down =  Product.objects.all().order_by('num_visits')[:10]

    recently_views_products = Product.objects.all().order_by('-last_visit')[0:20]

    comments = Comment.objects.all()

    context = {
        'setting': setting, 
        'page': page,
        'products_top10': products_top10,
        'Laptop': Laptop,
        'Audio': Audio,
        'Smartphone': Smartphone,
        'Desktop': Desktop,
        'Tablet': Tablet,
        'Gears': Gears,
        'Watch': Watch,
        'featured_products': featured_products,
        'best_sellers': best_sellers,
        'recently_views_products': recently_views_products,
        'popular_products_down': popular_products_down,
        'popular_products': popular_products,
        'main_popular_products_down': main_popular_products_down,
        'comments': comments,
        'audio_best_sellers': audio_best_sellers,
        'laptop_best_sellers': laptop_best_sellers,
    }
    return render(request, 'index.html', context)

def about(request):
    setting = Setting.objects.get(pk = 1)
    context = {
        'setting': setting,
    }
    return render(request, 'about.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Your message has been sent. Thank you for contacting.')
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk = 1)
    
    form = ContactForm
        
    context = {
        'setting': setting,
        'form': form,
        }
    return render(request, 'contact.html', context)

def category_products(request, id, slug):
    setting = Setting.objects.get(pk = 1)
    products = Product.objects.filter(category_id = id)
    
    catdata = Category.objects.get(pk=id)

    products = Product.objects.filter(category_id = id)
    paginator = Paginator(products, 10)
    page = request.GET.get('page')
    products = paginator.get_page(page)

    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]

    context = {
        'catdata': catdata,
        'products': products,
        'setting': setting,
        'recently_views_products': recently_views_products,
        'popular_products': popular_products,
    }
    return render(request, 'category_products.html', context)

def shop(request):
    setting = Setting.objects.get(pk = 1)

    all_products = Product.objects.all().order_by('?')
    paginator = Paginator(all_products, 20)
    page = request.GET.get('page')
    all_products = paginator.get_page(page)
        
    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]

    context = {
        'setting': setting,
        'all_products': all_products,
        'recently_views_products': recently_views_products,
        'popular_products': popular_products,
        
    }
    return render(request, 'shop.html', context)

def search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
                paginator = Paginator(products, 10)
                page = request.GET.get('page')
                products = paginator.get_page(page)
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
                paginator = Paginator(products, 10)
                page = request.GET.get('page')
                products = paginator.get_page(page)
                

            popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
            recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]

            context = {
                'products': products,
                'query': query,
                'recently_views_products': recently_views_products,
                'popular_products': popular_products,
            }
            return render(request, 'search_products.html', context)
    
    return HttpResponseRedirect('/')

def product_page(request, id, slug):
    
    product = Product.objects.get(pk = id)
    images = Images.objects.filter(product_id=id)

    comments = Comment.objects.filter(product_id=id, status='New')
    paginator = Paginator(comments, 3)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    related_products = list(product.category.products.filter(parent=None).exclude(id=product.id))
    if len(related_products) >= 7:
        related_products = random.sample(related_products, 7)
    
    product.count_sold = product.count_sold + 1

    product.num_visits = product.num_visits + 1
    
    product.last_visit = datetime.now()
    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]

    product.save()

    context = {
        'product': product,
        'images': images,
        'comments': comments,
        'recently_views_products': recently_views_products,
        'popular_products': popular_products,
        'related_products': related_products,
    }

    return render(request, 'product.html', context)

def faq(request):
    faq = FAQ.objects.filter(status="True").order_by('ordernumber')
    paginator = Paginator(faq, 3)
    page = request.GET.get('page')
    faq = paginator.get_page(page)
        
    context = {
        'faq': faq,
    }
    return render(request, 'faq.html', context)

def selectcurrency(request):
    lasturl = request.META.get('HTTP_REFERER')
    if request.method == 'POST':  
        request.session['currency'] = request.POST['currency']
    return HttpResponseRedirect(lasturl)

@login_required(login_url='/login')
def savelangcur(request):
    lasturl = request.META.get('HTTP_REFERER')
    current_user = request.user
    data = UserProfile.objects.get(user_id=current_user.id )
    data.currency_id = request.session['currency']
    return HttpResponseRedirect(lasturl)