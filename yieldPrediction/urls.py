from django.urls import path
from . import views

urlpatterns = [
    path('', views.predictor, name = 'predictor'),
    path('send_otp/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
]
