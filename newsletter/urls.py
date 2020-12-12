from django.urls import path
from newsletter import views

urlpatterns = [
    path('subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('subscribe/', views.newsletter_unsubscribe, name='newsletter_unsubscribe'),
]