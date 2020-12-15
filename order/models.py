from django.forms import ModelForm
from django.contrib.auth.models import User
from product.models import Product
from django.db import models

class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title
    
    @property
    def price(self):
        return (self.product.price)
    
    @property
    def amount(self):
        return (self.quantity * self.product.price)
            

class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']

class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=255, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=12, blank=True)
    address = models.CharField(max_length=512, blank=True)
    city = models.CharField(max_length=255, blank=True) 
    country = models.CharField(max_length=255, blank=True)
    total = models.FloatField()
    status = models.CharField(max_length=255, choices=STATUS, default='New')
    ip = models.CharField(max_length=255, blank=True)
    adminnote = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment = models.ForeignKey("Payment", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address', 'city', 'country']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=255, choices=STATUS, default='New')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    charge_id = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username