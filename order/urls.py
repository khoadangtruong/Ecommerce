from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct', views.orderproduct, name='orderproduct'),
    path('payment-complete', views.payment_complete, name="payment_complete"),
]