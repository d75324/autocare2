from django.urls import path
from .views import HomeView, PricingView, CarsView, RegisterView, VersionesView, CeroView, ProfileView, VehicleView, AddServiceView, ServicesView, VehicleServiceListView
#, profile_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('cars/', VehicleView.as_view(), name='cars'),
    path('register/', RegisterView.as_view(), name='register'),
    path('versiones/', VersionesView.as_view(), name='versiones'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('service/', AddServiceView.as_view(), name='service'),
    path('servicelist/', ServicesView.as_view(), name='servicelist'),
    #path('vehicle/<str:plate>/services/', VehicleServiceListView.as_view(), name='vehicle_service_list'),
    #path('create_vehicle/', create_vehicle, name='create_vehicle'),

]