from django.urls import path
from api import views

urlpatterns = [
    path('phone_auth/', views.PhoneNumberAuthView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('user/<pk>/', views.UserView.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]