from django.urls import path
from .views import HomeView, PricingView, CarsView, RegisterView, VersionesView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('register/', RegisterView.as_view(), name='register'),
    path('versiones/', VersionesView.as_view(), name='versiones'),
]