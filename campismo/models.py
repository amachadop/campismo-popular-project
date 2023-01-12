from django.db import models
from users.models import Usuario

# Create your models here.
class Provincia(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    
    class Meta:
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'   
        
    def __str__(self):
        return self.nombre

class Campismo(models.Model):
    nombre = models.CharField(max_length=200, unique=True)
    foto = models.ImageField(null=False, upload_to='portadas_campismos/')
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='campismo_provincia')
    descripcion = models.CharField(max_length=1000)
    precioTA = models.IntegerField()
    precioTB = models.IntegerField()
    categoria = models.CharField(max_length=1, choices=[('1','Primera'),('2','Segunda'),('3','Tercera'),('4','Cuarta')], default='4')
    tipoTurismo = models.CharField(max_length=2, choices=[('N','Nacional'),('I','Internacional'),('A','Ambos')], default='A')
    transporteIncluido = models.BooleanField()
    
    class Meta:
        verbose_name = 'Campismo'
        verbose_name_plural = 'Campismos'   
    
class ValoracionCampismo(models.Model):
    campismo = models.ForeignKey(Campismo, on_delete=models.CASCADE, related_name='campismo_valoracion')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_valoracion')
    valoracion = models.IntegerField()
    comentario= models.CharField(max_length=1200)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'ValoracionCampismo'
        verbose_name_plural = 'ValoracionesCampismo'   
    
class HabitacionCampismo(models.Model):
    idHab = models.CharField(max_length=10,primary_key=True)
    campismo = models.ForeignKey(Campismo, on_delete=models.CASCADE, related_name='campismo_habitacion')
    cantidadHuespedes = models.CharField(max_length=1, choices=[('4', 'Cuatro'),('8','Ocho')], default='4')
    estado = models.CharField(max_length=1, choices=[('D', 'Disponible'),('N','No disponible')], default='D')
    
    class Meta:
        verbose_name = 'HabitacionCampismo'
        verbose_name_plural = 'HabitacionesCampismo'   
    
class ReservaCampismo(models.Model):
    idReserva = models.CharField(max_length=8, unique=True,primary_key=True)
    campismo = models.ForeignKey(Campismo, on_delete=models.DO_NOTHING, related_name='campismo_reserva')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_reserva')
    habitacion = models.ForeignKey(HabitacionCampismo, on_delete=models.DO_NOTHING, related_name='habitacion_reserva')
    estado = models.CharField(max_length=2, choices=[('ET', 'En tiempo'),('P','Pasada'),('C','Cancelada')], default='ET')
    fechaEntrada = models.DateField(null=False)
    fechaSalida = models.DateField(null=False)
    cantP = models.IntegerField()
    
    class Meta:
        verbose_name = 'ReservaCampismo'
        verbose_name_plural = 'ReservasCampismo'   
    
class Oficina(models.Model):
    nombre = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    telefonos = models.TextField()
    h_lunes = models.CharField(max_length=150)
    h_martes = models.CharField(max_length=150)
    h_miercoles = models.CharField(max_length=150)
    h_jueves = models.CharField(max_length=150)
    h_viernes = models.CharField(max_length=150)
    h_sabado = models.CharField(max_length=150)
    h_domingo = models.CharField(max_length=150)
    
    class Meta:
        verbose_name = 'Oficina'
        verbose_name_plural = 'Oficinas'   

class Excursion(models.Model):
    nombre = models.CharField(max_length=250)
    foto = models.ImageField(null=False, upload_to='portadas_excursiones/')
    destino = models.CharField(max_length=250)
    descripcion = models.CharField(max_length=2000)
    precio = models.IntegerField()
    
    class Meta:
        verbose_name = 'Excursion'
        verbose_name_plural = 'Excursiones'   
    
class InstanciaExcursion(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='excursion_instancia')
    fecha = models.DateField(null=False)
    hora = models.TimeField(null=False)
    capacidad = models.IntegerField()
    estado = models.CharField(max_length=2, choices=[('P','Pasada'),('A','Activa')], default='A')
    
    class Meta:
        verbose_name = 'InstanciaExcursion'
        verbose_name_plural = 'InstanciaExcursiones'   
    
class ReservaExcursion(models.Model):
    idReserva = models.CharField(max_length=6, unique=True,primary_key=True)
    instancia = models.ForeignKey(InstanciaExcursion, on_delete=models.CASCADE, related_name='instancia_reserva')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_excursion')
    estado = models.CharField(max_length=2, choices=[('ET', 'En tiempo'),('P','Pasada'),('C','Cancelada')], default='ET')
    cantP = models.IntegerField()
    
    class Meta:
        verbose_name = 'ReservaExcursion'
        verbose_name_plural = 'ReservaExcursiones'   
    
class ComentarioExcursion(models.Model):
    excursion = models.ForeignKey(Excursion, on_delete=models.CASCADE, related_name='excursion_comentario')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuario_comentario_excursion')
    texto = models.CharField(max_length=1200)
    padre = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'ComentarioExcursion'
        verbose_name_plural = 'ComentarioExcursiones'                  
