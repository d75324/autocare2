from django.urls import path
from .views import HomeView, PricingView, CarsView, RegisterView, VersionesView, CeroView, ProfileView, VehicleView, AddServiceView, ServicesView
#, profile_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('cero/', CarsView.as_view(), name='cero'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('cars/', VehicleView.as_view(), name='cars'),
    path('register/', RegisterView.as_view(), name='register'),
    path('versiones/', VersionesView.as_view(), name='versiones'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('service/', AddServiceView.as_view(), name='service'),
    path('servicelist/', ServicesView.as_view(), name='servicelist'),
    #path('create_vehicle/', create_vehicle, name='create_vehicle'),

    #esta es la url que voy a usar en particular y profesional.html
    #path('profile2/', profile_view, name='profile2'),

]