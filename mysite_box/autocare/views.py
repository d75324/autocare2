from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, ListView
from .models import Vehicle
from django.views import View
from .forms import RegisterForm, ProfileForm, UserForm, VehicleForm
from django.contrib.auth.models import Group
#from django.contrib.auth.decorators import login_required


# custom template view
class CustomTemplateView(TemplateView):
    group_name = None
    group = None  # Definir el atributo group

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            self.group = Group.objects.filter(user=user).first()
            if self.group:
                self.group_name = self.group.name
        context['group_name'] = self.group_name
        return context

# pagina de antes de logeuarse
class CeroView(TemplateView):
    template_name = 'cero.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context

# pagina de inicio una vez logueado
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context

# pagina de Features

class VersionesView(TemplateView):
    template_name = 'versiones.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context    

# pagina de precios
class PricingView(TemplateView):
    template_name = 'pricing.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context    

class CarsView(ListView):
    model = Vehicle
    template_name = 'cars.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context    


    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.groups.filter(name='Mecanicos').exists():
        if self.request.user.is_anonymous:
            return queryset.none()
        else:
            queryset = queryset.filter(owner=self.request.user)
        return queryset

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
            return redirect('home')
        
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)

# pagina de perfil
class ProfileView(CustomTemplateView):
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


'''
# vista para agregar vehiculos :: vista basada en funciones
def vehicle_create_view(request):
    if request.method == "POST":
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cars')
    else:
        form = VehicleForm()
    return render(request, 'vehicle_form.html', {'form': form})
'''
# vista para agregar vehiculos :: vista basada en clases

class VehicleView(TemplateView):
    #model = Vehicle
    template_name = 'cars.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['form'] = VehicleForm()
        context['group_name'] = group_name
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = VehicleForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('profile')
        context = self.get_context_data()
        context['form'] = form
        
        return self.render_to_response(context)
    



'''
# ¿vista basada en función para guardar los cambios del formulario? NOP
@login_required
def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            return redirect('home')
    else:
        form = VehicleForm()

    return render(request, 'cars.html', {'form': form})
'''    

    