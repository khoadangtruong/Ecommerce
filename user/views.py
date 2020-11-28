from order.models import ShopCart
from django.contrib.auth.forms import PasswordChangeForm
from user.form import RegisterForm, ProfileUpdateForm, UserUpdateForm
from user.models import UserProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from product.models import Category, Comment
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
@login_required(login_url='/login')
def index(request):
    category = Category.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity 
    context = {
        'category': category,
        'profile': profile,
        'total': total,
        'count': count
    }
    return render(request, 'user_profile.html', context)

def login_form(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id = current_user.id)
            request.session['userimage'] = userprofile.image.url

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, 'Error! Username or password is incorrect')
            return HttpResponseRedirect('/login')

    category = Category.objects.all()
    context = {
        'category': category,
    }
    return render(request, 'login_form.html', context)

def logout_func(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request, "Your account has been created")

            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/register')

    form = RegisterForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'register_form.html', context)

@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) 
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        count = 0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
            count += rs.quantity 
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form,
            'total': total,
            'count': count
        }
        return render(request, 'user_update.html', context)

@login_required(login_url='/login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>'+ str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        current_user = request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        count = 0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
            count += rs.quantity
        context = {
            'category': category,
            'form': form,
            'total': total,
            'count': count
        }
        return render(request, 'user_password.html', context)

def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity
    context = {
        'category': category,
        'comments': comments,
        'total': total,
        'count': count
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id = current_user.id).delete()
    messages.success(request, 'Comment deleted')
    return HttpResponseRedirect('/user/comments/')