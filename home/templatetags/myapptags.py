  
from django import template
from django.db.models import Sum
from django.urls import reverse

from Ecommerce import settings
from order.models import ShopCart
from product.models import Category, Product

register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count

@register.simple_tag
def shopcarttotal(userid):
    shopcart = ShopCart.objects.filter(user_id=userid)
    total = sum(product.price * product.quantity for product in shopcart)
    return total

