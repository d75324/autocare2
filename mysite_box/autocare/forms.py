from django import forms
from django.contrib.auth.models import User, Group
from .models import Vehicle, Service
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Correo Electrónico')
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Esta cuenta está inactiva.', code='inactive')

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    group = forms.ModelChoiceField(queryset=Group.objects.filter(name__in=['Mecanicos', 'Particulares']), initial=Group.objects.get(name='Particulares'), required=True, label='Tipo de Uso: ')

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email_field = self.cleaned_data['email']
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo electrónico ya se encuentra registrado')
        return email_field

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            group = self.cleaned_data['group']
            user.groups.add(group)
        return user


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        # Filtra los usuarios que pertenecen al grupo "Mecánicos" a través del perfil
        self.fields['car_mechanic'].queryset = User.objects.filter(groups__name='Mecanicos')

# Formulario para editar la información de los usuarios. Como estoy usando
# dos tablas, una parte va a impactar en User y otra parte en Profile
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'location', 'telephone']

# formulario para carga de vehiculos
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['plate', 'brand', 'moddel', 'year', 'color', 'mileage', 'car_mechanic']

# formulario para agregar vehiculos. Aca necesito que por default la placa sea la del vehiculo en el cual doy click...

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['vehicle', 'date', 'kilometers', 'service_type', 'coments', 'cost']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ServiceForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user)
        else:
            self.fields['vehicle'].queryset = Vehicle.objects.none()
        self.fields['vehicle'].required = True
        self.fields['vehicle'].empty_label = None
