from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UsuarioManager(BaseUserManager):
    def _create_user(self, username, email, nombre, apellidos, pais, is_verificado, password, is_staff, is_superuser, **extra_fields):
        user = self.model(
            username = username,
            email = email,
            nombre = nombre,
            apellidos = apellidos,
            pais = pais,
            is_verificado = is_verificado,
            is_staff = is_staff,
            is_superuser = is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_user(self, username, email, nombre, apellidos, pais, password, **extra_fields):
        return self._create_user(username, email, nombre, apellidos, pais, False, password, False, False, **extra_fields)
    
    def create_superuser(self, username, email, nombre, apellidos, pais, password, **extra_fields):
        return self._create_user(username, email, nombre, apellidos, pais, True, password, True, True, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    PAISES = [
        ('SN','Seleccionar país de residencia'),
        ('CUB','Cuba'),
        ('USA','Estados Unidos'),
        ('ESP','España'),
    ]
    username = models.CharField(unique=True, primary_key=True, max_length=50)
    foto = models.ImageField(null=True, upload_to='perfiles/')
    email = models.EmailField(unique=True, max_length=254, null=False)
    nombre = models.CharField(max_length=200,null=False)
    apellidos = models.CharField(max_length=200,null=False)
    pais = models.CharField(max_length=200,choices=PAISES, default='SN')
    telefono = models.CharField(max_length=200,null=True, unique=True)
    descripcion = models.TextField(null=True)
    sexo = models.CharField(max_length=1, choices=[('S', 'Sin especificar'), ('H', 'Hombre'), ('M', 'Mujer')], default='S')
    is_verificado = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    registrado = models.DateField(auto_now_add=True)
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellidos', 'pais']
    
    def __str__(self):
        return f'{self.username}'