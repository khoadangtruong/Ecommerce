from order.models import ShopCart, Order, OrderProduct
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
    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {
        'profile': profile,
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
    return render(request, 'login_form.html')

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
    context = {
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
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
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
        form = PasswordChangeForm(request.user)
        context = {
            'form': form,
        }
        return render(request, 'user_password.html', context)

def user_comments(request):
    current_user = request.user
    comments = Comment.objects.filter(user_id = current_user.id)
    context = {
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def user_deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id = current_user.id).delete()
    messages.success(request, 'Comment deleted')
    return HttpResponseRedirect('/user/comments/')

@login_required(login_url='/login')
def user_orders(request):
    current_user = request.user
    orders = Order.objects.filter(user_id = current_user.id)
    context = {
        'orders': orders,
    }
    return render(request, 'user_orders.html', context)

@login_required(login_url='/login')
def user_orderdetail(request, id):
    current_user = request.user
    order = Order.objects.get(user_id = current_user.id, id = id)
    orderitems = OrderProduct.objects.filter(order_id = id)
    context = {
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)
