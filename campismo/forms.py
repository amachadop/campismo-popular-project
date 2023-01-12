from django import forms
from users.models import Usuario

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('email','nombre','apellidos','pais','telefono','sexo','descripcion')
        widgets = {
            'email': forms.EmailInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                    'id': 'email'
                }
            ),
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Nombre',
                    'id': 'nombre'
                }
            ),
            'apellidos': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Apellidos',
                    'id': 'apellidos'
                }
            ),
            'pais': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'pais'
                }
            ),
            'telefono': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'teléfono',
                    'id': 'telefono'
                }
            ),
            'sexo': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'sexo'
                }
            ),
            'descripcion': forms.Textarea(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Descripcion',
                    'id': 'descripcion'
                }
            ),
        }