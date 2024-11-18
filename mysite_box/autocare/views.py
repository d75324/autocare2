from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView, DetailView
from .models import Vehicle, Service
from django.views import View
from .forms import RegisterForm, ProfileForm, UserForm, VehicleForm, ServiceForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

# pagina de antes de logeuarse
class CeroView(TemplateView):
    template_name = 'cero.html'


# pagina de inicio una vez logueado
class HomeView(TemplateView):
    template_name = 'home.html'


# pagina de Features

class VersionesView(TemplateView):
    template_name = 'versiones.html'


class PricingView(TemplateView):
    template_name = 'pricing.html'


# registro de usuarios
class RegisterView(View):

    def get(self, request):
        data = {
            'form' : RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request):
        user_creation_form = RegisterForm(data=request.POST)
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            #request.group
            return redirect('profile')
        else:
            data = {
                'form': user_creation_form
            }
            return render(request, 'registration/register.html', data)

# pagina de perfil
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.groups.filter(name='Mecanicos').exists():
        if self.request.user.is_anonymous:
            return queryset.none()
        else:
            return queryset.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if self.request.user.is_anonymous:
            context['object_list'] = Vehicle.objects.none()
        else:
            context['object_list'] = Vehicle.objects.filter(owner=self.request.user)
        context ['user_form'] = UserForm(instance=user)
        context ['profile_form'] = ProfileForm(instance=user.profile)
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # si todo está ok, redirecciono a la página de perfil actualizada
            return redirect('profile')

        #si alguno de los datos no es válido
        context = self.get_context_data
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profile/profile.html', context)

# vista para agregar vehiculos :: vista basada en clases

#class VehicleListView(ListView):
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = VehicleForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.groups.filter(name='Mecanicos').exists():
        if self.request.user.is_anonymous:
            return queryset.none()
        else:
            return queryset.filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('profile')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response({'form':form})
            #return self.render_to_response(context)


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'vehicle_detail.html'


class AddServiceView(TemplateView):
    #model = Service
    template_name = 'service.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ServiceForm()
        return context

    def get(self, request, pk, *args, **kwargs):
        context = self.get_context_data()
        vehicle = get_object_or_404(Vehicle, pk=pk)
        context['form'] = ServiceForm(
            initial={'vehicle': vehicle},
            user=request.user
        )
        return self.render_to_response(context)

    def post(self, request, pk, *args, **kwargs):
        vehicle = get_object_or_404(Vehicle, pk=pk)
        form = ServiceForm(request.POST, user=request.user)  # Paso el usuario al formulario
        if form.is_valid():
            service = form.save(commit=False)
            service.owner = request.user
            service.save()
            return redirect('profile')
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

# vista del histórico de servicios - nop!

class ServicesView(ListView):
    model = Service
    template_name = 'servicelist.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Service.objects.none()
        else:
            return Service.objects.filter(vehicle__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)
        return context

class VehicleServiceListView(TemplateView):
    pass

class VehicleDeleteView(DeleteView):
    model = Vehicle
    template_name = 'vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.service_set.all().delete()  # Borrar también los servicios asociados
        return super().delete(request, *args, **kwargs)
