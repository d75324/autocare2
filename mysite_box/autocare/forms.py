from django import forms
from django.contrib.auth.models import User, Group
from .models import Vehicle
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile

class LoginForm(AuthenticationForm):
    pass

class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo Electronico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def clean_email(self):
        email_field = self.cleaned_data['email']

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo electrónico ya se encuentra registrado')
        return email_field

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

