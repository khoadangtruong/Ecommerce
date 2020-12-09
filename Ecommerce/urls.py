"""Ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from home import views
from order import views as OrderViews
from user import views as UserViews

urlpatterns = [
    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('home/',include('home.urls')),
    path('product/',include('product.urls')),
    path('order/',include('order.urls')),
    path('user/',include('user.urls')),
    path('blog/',include('blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('currencies/',include('currencies.urls')),

    path('selectcurrency', views.selectcurrency, name='selectcurrency'),
    path('savelangcur', views.savelangcur, name='savelangcur'),

    path('about/',views.about, name='about'),
    path('faq/',views.faq, name='faq'),
    path('contact/',views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('shop/', views.shop, name='shop'),
    path('category/<int:id>/<slug:slug>', views.category_products, name = 'category_products'),
    path('product/<int:id>/<slug:slug>', views.product_page, name = 'product_page'),
    
    path('shopcart/',OrderViews.shopcart, name='shopcart'),
    path('order_form/',OrderViews.orderproduct, name='orderproduct'),

    path('login/',UserViews.login_form, name='login_form'),
    path('logout/',UserViews.logout_func, name='logout_func'),
    path('register/',UserViews.register_form, name='register_form'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
