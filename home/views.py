from django.core.paginator import Paginator
from datetime import datetime
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from home.models import Setting, ContactForm, ContactMessage
from product.models import Product, Category, Images, Comment
from home.form import SearchForm
from order.models import ShopCart


def index(request):
    setting = Setting.objects.get(pk = 1)
    category = Category.objects.all()
    products_top10 = Product.objects.all().order_by('?')[:10]
    Laptop = Product.objects.filter(category_id = 1).order_by('?')[:10]
    Smartphone = Product.objects.filter(category_id = 2).order_by('?')[:10]
    Smartphone_single_new_arrived = Product.objects.filter(category_id = 2).order_by('?')[:1]
    Audio = Product.objects.filter(category_id = 12).order_by('?')[:10]
    Desktop = Product.objects.filter(category_id = 8).order_by('?')[:10]
    Tablet = Product.objects.filter(category_id = 9).order_by('?')[:8]
    Gears = Product.objects.filter(category_id = 10).order_by('?')[:10]
    Watch = Product.objects.filter(category_id = 11).order_by('?')[:10]
    page = 'home'
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    popular_products =  Product.objects.all().order_by('num_visits')[:1]
    popular_products_down =  Product.objects.all().order_by('-num_visits')[:1]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:20]
    context = {
        'setting': setting, 
        'page': page,
        'category': category,
        'products_top10': products_top10,
        'Laptop': Laptop,
        'Audio': Audio,
        'Smartphone': Smartphone,
        'Smartphone_single_new_arrived': Smartphone_single_new_arrived,
        'Desktop': Desktop,
        'Tablet': Tablet,
        'Gears': Gears,
        'Watch': Watch,
        'total': total,
        'count': count,
        'recently_views_products': recently_views_products,
        'popular_products_down': popular_products_down,
        'popular_products': popular_products,
    }
    return render(request, 'index.html', context)

def about(request):
    setting = Setting.objects.get(pk = 1)
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    context = {
        'setting': setting,
        'category': category,
        'total': total,
        'count': count
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
    category = Category.objects.all()
    form = ContactForm
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    context = {
        'setting': setting,
        'category': category,
        'form': form,
        'total': total,
        'count': count
        }
    return render(request, 'contact.html', context)

def category_products(request, id, slug):
    setting = Setting.objects.get(pk = 1)
    products = Product.objects.filter(category_id = id)
    category = Category.objects.all()
    catdata = Category.objects.get(pk=id)
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]
    context = {
        'catdata': catdata,
        'products': products,
        'category': category,
        'setting': setting,
        'total': total,
        'count': count,
        'recently_views_products': recently_views_products,
        'popular_products': popular_products,
    }
    return render(request, 'category_products.html', context)

def shop(request):
    setting = Setting.objects.get(pk = 1)
    category = Category.objects.all()

    all_products = Product.objects.all()
    paginator = Paginator(all_products, 10)
    page = request.GET.get('page')
    all_products = paginator.get_page(page)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]
    context = {
        'setting': setting,
        'all_products': all_products,
        'category': category,
        'total': total,
        'count': count,
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
            else:
                products = Product.objects.filter(title__icontains=query, category_id=catid)
            
            category = Category.objects.all()
            current_user = request.user
            shopcart = ShopCart.objects.filter(user_id = current_user.id)
            total = 0
            count = 0
            for rs in shopcart:
                total += rs.product.price * rs.quantity
                count += rs.quantity
            popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
            recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]
            context = {
                'products': products,
                'query': query,
                'category': category,
                'total': total,
                'count': count,
                'recently_views_products': recently_views_products,
                'popular_products': popular_products,
            }
            return render(request, 'search_products.html', context)
    
    return HttpResponseRedirect('/')

def product_page(request, id, slug):
    category = Category.objects.all()
    product = Product.objects.get(pk = id)
    images = Images.objects.filter(product_id=id)

    comments = Comment.objects.filter(product_id=id, status='New')
    paginator = Paginator(comments, 1)
    page = request.GET.get('page')
    comments = paginator.get_page(page)

    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity

    product.num_visits = product.num_visits + 1
    product.last_visit = datetime.now()
    popular_products =  Product.objects.all().order_by('-num_visits')[0:6]
    recently_views_products = Product.objects.all().order_by('-last_visit')[0:6]
    product.save()

    context = {
        'product': product,
        'category': category,
        'images': images,
        'comments': comments,
        'total': total,
        'count': count,
        'recently_views_products': recently_views_products,
        'popular_products': popular_products,
    }

    return render(request, 'product.html', context)

