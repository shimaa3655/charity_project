from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [
    path('checkout/', views.payment, name='donate'),
    path('payment-success/', views.payment_successful, name='successful'),
    path('payment-failed/', views.payment_failed, name='cancelled'),
    path('paypal-ipn/', views.paypal_ipn, name='paypal-ipn'),
]