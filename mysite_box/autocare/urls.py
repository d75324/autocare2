from django.urls import path
from .views import HomeView, PricingView, CarsListView, RegisterView, VersionesView, CeroView, ProfileView, VehicleListView, AddServiceView, ServicesView, VehicleServiceListView, VehicleDetailView
#, profile_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('pricing/', PricingView.as_view(), name='pricing'),
    path('cars/', CarsListView.as_view(), name='cars'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicle_detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('versiones/', VersionesView.as_view(), name='versiones'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('service/', AddServiceView.as_view(), name='service'),
    path('servicelist/', ServicesView.as_view(), name='servicelist'),
    #path('vehicle/<str:plate>/services/', VehicleServiceListView.as_view(), name='vehicle_service_list'),
    #path('create_vehicle/', create_vehicle, name='create_vehicle'),

]
