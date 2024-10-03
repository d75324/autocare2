from django.urls import path
from .views import HomeView, PricingView, CarsView, RegisterView, VersionesView, CeroView, ProfileView
#, profile_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cero/', CeroView.as_view(), name='cero'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('cars/', CarsView.as_view(), name='cars'),
    path('register/', RegisterView.as_view(), name='register'),
    path('versiones/', VersionesView.as_view(), name='versiones'),
    path('profile/', ProfileView.as_view(), name='profile'),
    #esta es la url que voy a usar en particular y profesional.html
    #path('profile2/', profile_view, name='profile2'),

]