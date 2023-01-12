from django import forms
from .models import Usuario
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, Permission
from campismo.models import Provincia, Campismo, Excursion, Oficina, HabitacionCampismo, InstanciaExcursion

class LoginForm(AuthenticationForm):
    
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['id'] = 'floatingInput'
        self.fields['username'].widget.attrs['placeholder'] = 'Usuario'
        self.fields['username'].widget.attrs['style'] = 'height: 55px;'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['id'] = 'floatingPassword'
        self.fields['password'].widget.attrs['placeholder'] = 'Contraseña'
        self.fields['password'].widget.attrs['style'] = 'height: 55px;'
        self.fields['password'].widget.attrs['aria-describedby'] = 'basic-addon1'
        
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username','password','email','nombre',
                  'apellidos','pais','telefono','sexo')
        widgets = {
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Usuario',
                    'id': 'username'
                }
            ),
            'password': forms.PasswordInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Contraseña',
                    'id': 'password',
                    'aria-describedby': 'basic-addon1'
                }
            ),
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
        }
        
class UsuarioEditForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ('username','email','nombre',
                  'apellidos','pais','telefono','sexo')
        widgets = {
            'username': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Usuario',
                    'id': 'username'
                }
            ),
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
        }
        
class RolForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name',)
        widgets = {
            'name': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Nombre del rol',
                    'id': 'nombre',
                    'style': 'width: 200px;'
                }
            )
        }
        
class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permission
        fields = ('name','content_type','codename')
        widgets = {
            'name': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Nombre del permiso',
                    'id': 'nombre'
                }
            ),
            'content_type': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectContent'
                }
            ),
            'codename': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Codename',
                    'id': 'codename'
                }
            )
        }
    
class ProvinciaForm(forms.ModelForm):
    class Meta:
        model = Provincia
        fields = ('nombre',)
        widgets = {
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Provincia',
                    'id': 'nombre',
                    'style': 'width: 200px;'
                }
            )
        }

class CampismoForm(forms.ModelForm):
    class Meta:
        model = Campismo
        fields = ('nombre','foto','provincia','descripcion','precioTA','precioTB','categoria','tipoTurismo','transporteIncluido')
        widgets = {
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Base de Campismo',
                    'id': 'nombre'
                }
            ),
            'foto': forms.FileInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Foto de Portada',
                    'id': 'foto',
                    'accept': 'image/png, image/jpg'
                }
            ),
            'provincia': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectProvincia'
                }
            ),
            'descripcion': forms.Textarea(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Descripción',
                    'id': 'descripcion'
                }
            ),
            'precioTA': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Pecio Temporada Alta',
                    'id': 'precioTA'
                }
            ),
            'precioTB': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Precio Temporada Baja',
                    'id': 'precioTB'
                }
            ),
            'categoria': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectCategoria'
                }
            ),
            'tipoTurismo': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectTipoTurismo'
                }
            ),
            'transporteIncluido': forms.CheckboxInput(
                attrs= {
                    'class': 'form-check-input',
                    'id': 'isTransporte'
                }
            ),
        }
        
class HabitacionCampismoForm(forms.ModelForm):
    class Meta:
        model = HabitacionCampismo
        fields = ('idHab','campismo','cantidadHuespedes','estado')
        widgets = {
            'idHab': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'No. Habitación',
                    'id': 'idHab'
                }
            ),
            'cantidadHuespedes': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectCantidadHuespedes'
                }
            ),
            'estado': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectEstado'
                }
            ),
        }
        
class OficinaForm(forms.ModelForm):
    class Meta:
        model = Oficina
        fields = ('nombre','ubicacion','direccion','email','telefonos','h_lunes','h_martes','h_miercoles','h_jueves','h_viernes','h_sabado','h_domingo')
        widgets = {
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Nombre de la oficina',
                    'id': 'nombre'
                }
            ),
            'ubicacion': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Ubicación',
                    'id': 'ubicacion'
                }
            ),
            'direccion': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Dirección',
                    'id': 'direccion'
                }
            ),
            'email': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico',
                    'id': 'email'
                }
            ),
            'telefonos': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Teléfonos',
                    'id': 'telefonos'
                }
            ),
            'h_lunes': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Lunes',
                    'id': 'lunes'
                }
            ),
            'h_martes': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Martes',
                    'id': 'martes'
                }
            ),
            'h_miercoles': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Miercóles',
                    'id': 'nombre'
                }
            ),
            'h_jueves': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Jueves',
                    'id': 'jueves'
                }
            ),
            'h_viernes': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Viernes',
                    'id': 'viernes'
                }
            ),
            'h_sabado': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Sábado',
                    'id': 'sabado'
                }
            ),
            'h_domingo': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Domingo',
                    'id': 'domingo'
                }
            ),
        }
        
class ExcursionForm(forms.ModelForm):
    class Meta:
        model = Excursion
        fields = ('nombre','foto','destino','descripcion','precio')
        widgets = {
            'nombre': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Excursión',
                    'id': 'nombre'
                }
            ),
            'foto': forms.FileInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Foto de Portada',
                    'id': 'foto',
                    'accept': 'image/png, image/jpg'
                }
            ),
            'destino': forms.TextInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Destino',
                    'id': 'destino'
                }
            ),
            'descripcion': forms.Textarea(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Descripción',
                    'id': 'descripcion'
                }
            ),
            'precio': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Pecio',
                    'id': 'precio'
                }
            ),
        }
        
class InstanciaForm(forms.ModelForm):
    class Meta:
        model = InstanciaExcursion
        fields = ('fecha','hora','capacidad','estado')
        widgets = {
            'fecha': forms.DateInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Fecha',
                    'id': 'fecha',
                    'type': 'date'
                }
            ),
            'hora': forms.TimeInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Hora',
                    'id': 'hora',
                    'type': 'time'
                }
            ),
            'estado': forms.Select(
                attrs= {
                    'class': 'form-select',
                    'id': 'selectEstado'
                }
            ),
            'capacidad': forms.NumberInput(
                attrs= {
                    'class': 'form-control',
                    'placeholder': 'Capacidad',
                    'id': 'capacidad'
                }
            ),
        }