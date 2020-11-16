from .models import Alumno
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django import forms

class AlumnoNuevoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['name', 'last', 'dni', 'ingreso', 'disposicion', 'doc_ingreso', 'calif_anual', 'trayectoria']
        labels = {'name':'', 'last':'', 'ingreso':'', 'dni':'', 'disposicion':'', 
        'doc_ingreso':'Documento presentado al ingreso', 'calif_anual':'Calificador Anual', 'trayectoria':'Calificador Personal'}

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre', 'autofocus':'autofocus'}),
            'last': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'ingreso': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Año de ingreso'}),
            'disposicion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Disposición Interna'}),
            'doc_ingreso': forms.Select(attrs={'class': 'form-control'}),
            'calif_anual': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link a Hoja de Drive (Habilitar Permisos)'}),
            'trayectoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Link a Hoja de Drive (Habilitar Permisos)'}),
        }

class salidaForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['condicion', 'egreso', 'titulo_confeccionado', 
        'titulo_legalizado', 'titulo_retirado', 'fecha_titulo_confeccionado', 
        'fecha_titulo_legalizado', 'fecha_titulo_retirado', 'folio', 'libro', 
        'pase_confeccionado', 'pase_legalizado', 'fecha_pase_confeccionado', 
        'fecha_pase_legalizado']

        labels = {'condicion':'Seleccionar condición', 'egreso':'Año de egreso', 'titulo_confeccionado':'Confeccionado', 
        'titulo_legalizado':'Legalizado', 'titulo_retirado': 'Retirado', 'fecha_titulo_confeccionado': 'Fecha de confección', 
        'fecha_titulo_legalizado': 'Fecha de legalización', 'fecha_titulo_retirado': 'Fecha de retiro', 
        'fecha_pase_confeccionado': 'Fecha de confección del pase', 'fecha_pase_legalizado':'Fecha de envío a legalización del pase'}

        widgets = {
                'condicion': forms.Select(attrs={'class': 'form-control', 'autofocus':'autofocus'}),
                'egreso': forms.TextInput(attrs={'class': 'form-control'}),           
                'fecha_titulo_confeccionado': forms.TextInput(attrs={'class': 'form-control'}),
                'fecha_titulo_legalizado': forms.TextInput(attrs={'class': 'form-control'}),
                'fecha_titulo_retirado': forms.TextInput(attrs={'class': 'form-control'}),
                'folio': forms.TextInput(attrs={'class': 'form-control'}),
                'libro': forms.TextInput(attrs={'class': 'form-control'}),
                'fecha_pase_confeccionado': forms.TextInput(attrs={'class': 'form-control'}),
                'fecha_pase_legalizado': forms.TextInput(attrs={'class': 'form-control'}),

            }

class PasswordsChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Contraseña actual", widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password1 = forms.CharField(label="Nueva contraseña", widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))
    new_password2 = forms.CharField(label="Confirmar contraseña", widget=forms.PasswordInput(attrs={'class':'form-control', 'type':'password'}))

    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']