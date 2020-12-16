import json
from django.utils.crypto import get_random_string
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from user.models import UserProfile
from product.models import Product
from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct, Payment, OrderPaymentForm
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth.models import User
from django.views.generic import View
import stripe
stripe.api_key = "sk_test_51HyuDiAODGeOESBEJRMK2nSBNQAFoL1jeXdCyFMZNY8irbolH4rhVg6gKRUYbIo8WmdQwb9ILdms3UEuWacS6WBL00AKIj92rW"

# Create your views here.
def index(request):
    return HttpResponse('My order page')

@login_required(login_url='/login')
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    product = Product.objects.get(pk=id)
    checkproduct = ShopCart.objects.filter(product_id=id)
    
    if checkproduct:
        control = 1
    else:
        control = 0
    
    if request.method == 'POST':
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, 'Product added to cart')
        return HttpResponseRedirect(url)
    
    else:
        if control == 1:
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request, 'Product added to cart')
        return HttpResponseRedirect(url)
        
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity 
    context = {
        'shopcart': shopcart,
        'total': total,
    }

    return render(request, 'shopcart.html', context)

@login_required(login_url='/login')
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item has been deleted from cart.")
    return HttpResponseRedirect("/shopcart")


def payment_complete(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, id=body['orderID'])
    payment = Payment(
        user=request.user,
        charge_id=body['payID'],
        amount=order.total
    )
    payment.save()

    # assign the payment to order
    order.payment = payment
    order.save()
    messages.success(request, "Payment was successful")
    return redirect('home')


def orderproduct(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id = current_user.id)
    total = 0
    count = 0
    for rs in shopcart:
        total += rs.product.price * rs.quantity
        count += rs.quantity 

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.city = form.cleaned_data['city']
            data.phone = form.cleaned_data['phone']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = current_user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            

            ShopCart.objects.filter(user_id=current_user.id).delete()
            request.session['cart_item'] = 0 
            messages.success(request, 'Your order has been completed.')
            return render(request, 'Order_Completed.html', {'ordercode': ordercode})
        
        
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderproduct')

    form = OrderForm()
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {
        'shopcart': shopcart,
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'order_form.html', context)

class Checkoutpayment(View):
    
    def get(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user)
        current_user = self.request.user
        shopcart = ShopCart.objects.filter(user_id = current_user.id)
        total = 0
        count = 0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
            count += rs.quantity 
        context = {
            'shopcart': shopcart,
            'order': order,
            'total': total
        }
        return render(self.request, 'checkoutpayment.html', context)
    
    def post(self, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user)
        shopcart = ShopCart.objects.filter(user_id = self.request.user.id)
        total = 0
        count = 0
        for rs in shopcart:
            total += rs.product.price * rs.quantity
            count += rs.quantity 
        form = OrderPaymentForm(self.request.POST or None)
        if form.is_valid():
            data = Order()
            data.first_name = form.cleaned_data.get('first_name')
            data.last_name = form.cleaned_data.get('last_name')
            data.address = form.cleaned_data.get('address')
            data.city = form.cleaned_data.get('city')
            data.phone = form.cleaned_data.get('phone')
            data.user_id = self.request.user.id
            data.total = total
            payment_option = form.cleaned_data.get('payment_option')
            data.save()

            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id = data.id
                detail.product_id = rs.product_id
                detail.user_id = self.request.user.id
                detail.quantity = rs.quantity
                detail.price = rs.product.price
                detail.amount = rs.amount
                detail.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=self.request.user.id).delete()
            self.request.session['cart_item'] = 0 

            if payment_option == "S":
                return redirect('payment', payment_option="stripe")

            if payment_option == "P":
                return redirect('payment', payment_option="paypal")
                
            messages.info(self.request, "Invalid payment option")
            return redirect('checkout')
        
        else:
            return redirect('checkout')
class PaymentView(View):
    
    def get(self, *args, **kwargs):
        return render(self.request, 'payment.html')
    
    def post(self, request, *args, **kwargs):
        order = Order.objects.filter(user=self.request.user)
        shopcart = ShopCart.objects.filter(user_id = self.request.user.id)
        try:
            customer = stripe.Customer.create(
                email = self.request.user.email,
                description=self.request.user.username,
                source = self.request.POST['stripeToken']
            )
            amount = order.get_total()
            charge = stripe.Charge.create(
                amount= amount * 100,
                currency="usd",
                customer = customer,
                description="Test payment",
            )
            payment = Payment(
                user=self.request.user,
                charge_id=charge['id'],
                amount=amount
            )

            payment.save()
            order.payment = payment
            order.save()
            messages.success(self.request, "Completed payment!")
            return redirect('home')
        except stripe.error.CardError as e:
            messages.info(self.request, f"{e.error.message}")
            return redirect('home')
        except stripe.error.InvalidRequestError as e:
            messages.success(self.request, "Invalid request")
            return redirect('home')
        except stripe.error.AuthenticationError as e:
            messages.success(self.request, "Authentication error")
            return redirect('home')
        except stripe.error.APIConnectionError as e:
            messages.success(self.request, "Check your connection")
            return redirect('home')
        except stripe.error.StripeError as e:
            messages.success(
                self.request, "There was an error please try again")
            return redirect('home')
        except Exception as e:
            messages.success(
                self.request, "Thank you for your payment")
            return redirect('home')
        
        