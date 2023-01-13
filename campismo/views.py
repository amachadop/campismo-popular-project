from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, UpdateView, View, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from users.models import Usuario
from .forms import PerfilForm
from django.db.models import Avg, Count, Sum
from datetime import datetime, timedelta, date
import collections
import random
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
import json
from django.contrib.auth.models import Group, Permission

# Create your views here.
class Index(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actual'] = 'i'
        context['campismos'] = Campismo.objects.all()
        context['excursiones'] = Excursion.objects.all()
        return context

class Perfil(LoginRequiredMixin, DetailView):
    template_name = 'perfil_usuario.html'
    context_object_name = 'usuario'
    model = Usuario
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'perfil'
        return context
    
    def post(self, request, *args, **kwargs):
        if request.POST['password1'] == "" or request.POST['password2'] == "":
            context = self.get_context_data(**kwargs)
            context['error'] = 'Existen campos vacíos'
            return render(request, self.template_name, context)
        else:
            if request.POST['password1'] == request.POST['password2']:
                user = self.get_object()
                user.set_password(request.POST['password1'])
                user.save()
                return redirect('perfil', self.get_object().username)
            else:
                context = self.get_context_data(**kwargs)
                context['error'] = 'Las contraseñas no coinciden'
                return render(request, self.template_name, context)

class EditarPerfil(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = PerfilForm
    template_name = 'perfil_editar.html'
    
    def get_success_url(self):
        return reverse_lazy('perfil', kwargs={'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'perfil'
        return context
  
class Campismos(TemplateView):
    template_name = 'buscar_campismos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actual'] = 'c'
        context['provincias'] = Provincia.objects.all()
        return context

class ListaCampismos(ListView):
    model = Campismo
    
    def get_queryset(self,**kwargs):
        if kwargs['provincia'] == "Cualquiera":
            campismos = Campismo.objects.all().annotate(rate=Avg('campismo_valoracion__valoracion'))
        else:
            campismos = Campismo.objects.filter(provincia__nombre=kwargs['provincia']).annotate(rate=Avg('campismo_valoracion__valoracion'))

        if kwargs['val'] != 1:
            campismos = campismos.filter(rate__gte=kwargs['val'])

        if kwargs['categoria'] != 0:
            campismos = campismos.filter(categoria=str(kwargs['categoria']))

        if kwargs['turismo'] != 'C':
            campismos = campismos.filter(tipoTurismo=kwargs['turismo'])

        campismos = campismos.filter(precioTB__gte=kwargs['minPrecio'],precioTA__lte=kwargs['maxPrecio'])

        if kwargs['keywords'] == "*all":
            campismos = list(campismos.values())
        else:
            campismos = list(campismos.filter(nombre__contains=kwargs['keywords']).values())
        return campismos
    
    def get(self, request, *args, **kwargs):
        if (len(self.get_queryset(**kwargs)) > 0):
            data = {'message': "success",
                    'campismos': self.get_queryset(**kwargs), 'provincias': list(Provincia.objects.all().values())}
        else:
            data = {'message': "Not Found"}
        return JsonResponse(data)

class CampisoDetalles(DetailView):
    model = Campismo
    template_name = 'detalles_campismos.html'

    def get(self, request, *args, **kwargs):
        context = {}
        
        context['campismo'] = self.get_object()
        
        if not request.user.is_anonymous:
            context['valoracion'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), usuario=request.user)
        else:
            context['valoracion'] = 0
        
        vals = ValoracionCampismo.objects.filter(campismo=self.get_object()).order_by('-fecha')
        
        rate = 0

        for x in vals:
            rate = rate + x.valoracion

        if vals.count() != 0:
            rate = round(rate / vals.count(), 1)
            
        context['vals'] = vals
        context['rate'] = rate
        context['excelente'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), valoracion=5)
        context['buena'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), valoracion=4)
        context['regular'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), valoracion=3)
        context['pobre'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), valoracion=2)
        context['mala'] = ValoracionCampismo.objects.filter(campismo=self.get_object(), valoracion=1)
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        val = ValoracionCampismo(
            campismo = self.get_object(),
            usuario = request.user,
            valoracion = request.POST['valoracion'],
            comentario = request.POST['comentario']
        )
        val.save()
        return redirect('campD', self.get_object().id)

class ReservarCampismo(LoginRequiredMixin,View):
    template_name = 'reservar_campismos.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['campismo'] = Campismo.objects.get(pk=kwargs['id'])
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        fechaEntrada = request.POST['fechas'].split("to")[0].split(" ")[0]
        fechaSalida = request.POST['fechas'].split("to")[1].split(" ")[1]
        cantP = int(request.POST['cantidad'])
        id = kwargs['id']
        
        print(fechaEntrada,fechaSalida)
        
        entrada = datetime.strptime(fechaEntrada, '%Y-%m-%d')
        salida = datetime.strptime(fechaSalida, '%Y-%m-%d')

        all_dates = []
        habitaciones_disponibles = []

        habitaciones_campismo = HabitacionCampismo.objects.filter(
            campismo=id, estado='D').values()

        while entrada <= salida:
            all_dates.append(entrada.strftime('%Y-%m-%d'))
            entrada = entrada + timedelta(days=1)

        for hab in habitaciones_campismo:
            reservas = ReservaCampismo.objects.filter(
                habitacion=hab['idHab']).values()
            hab_dates = []
            for r in reservas:
                date_entrada = datetime.strptime(date.strftime(
                    r['fechaEntrada'], '%Y-%m-%d'), '%Y-%m-%d')
                date_salida = datetime.strptime(date.strftime(
                    r['fechaSalida'], '%Y-%m-%d'), '%Y-%m-%d')
                while date_entrada <= date_salida:
                    hab_dates.append(date_entrada.strftime('%Y-%m-%d'))
                    date_entrada = date_entrada + timedelta(days=1)
            count = 0
            for d in all_dates:
                if d not in hab_dates:
                    count += 1
            if count == len(all_dates):
                habitaciones_disponibles.append(hab)

        if len(habitaciones_disponibles) == 0:
            return render(request, self.template_name,{
                'campismo': Campismo.objects.get(pk=id),
                'error': 'Lo sentimos. No quedan habitaciones disponibles'
            })
        else:
            hab_con_8 = []
            hab_con_4 = []
            hab_a_reservar = []

            for hab in habitaciones_disponibles:
                if int(hab['cantidadHuespedes']) == 4:
                    hab_con_4.append(hab)
                else:
                    hab_con_8.append(hab)

            cant = cantP
            while cant > 0:
                if len(hab_con_8) > 0:
                    if cant > 4:
                        hab_a_reservar.append(hab_con_8.pop(0))
                        cant -= 8
                    else:
                        if len(hab_con_4) == 0:
                            hab_a_reservar.append(hab_con_8.pop(0))
                            cant -= 4
                else:
                    if len(hab_con_4) > 0:
                        hab_a_reservar.append(hab_con_4.pop(0))
                        cant -= 4
                    else:
                        break

            cant_total = 0
            for h in hab_a_reservar:
                cant_total += int(h['cantidadHuespedes'])

            if cant_total >= cantP:
                for hab in hab_a_reservar:
                    c = Campismo.objects.get(pk=id)
                    h = HabitacionCampismo.objects.get(
                        idHab=hab['idHab'])
                    print(h.cantidadHuespedes)
                    if cantP < int(h.cantidadHuespedes):
                        huespedes = cantP
                    else:
                        huespedes = int(h.cantidadHuespedes)
                    nueva_reserva = ReservaCampismo(idReserva=generarIdReserva(), campismo=c, usuario=request.user,
                                                    habitacion=h, estado='ET',
                                                    fechaEntrada=fechaEntrada, fechaSalida=fechaSalida,
                                                    cantP=huespedes)
                    nueva_reserva.save()
                    cantP -= int(h.cantidadHuespedes)

                return redirect('reservas', request.user.username)
            else:
                return render(request, self.template_name,{
                    'campismo': Campismo.objects.get(pk=id),
                    'error': 'No se encontraron habitaciones disponibles para su cantidad de personas en las fechas escogidas'
                })

def getFechasCanceladas(_request, id):
    all_dates = []
    fechas_cancel = []

    reservas = ReservaCampismo.objects.filter(
        campismo=id, estado='ET').values()

    for r in reservas:
        date_entrada = datetime.strptime(date.strftime(
            r['fechaEntrada'], '%Y-%m-%d'), '%Y-%m-%d')
        date_salida = datetime.strptime(date.strftime(
            r['fechaSalida'], '%Y-%m-%d'), '%Y-%m-%d')
        while date_entrada <= date_salida:
            all_dates.append(date_entrada.strftime('%Y-%m-%d'))
            date_entrada = date_entrada + timedelta(days=1)

    result = collections.Counter(all_dates)

    cant_hab_disponibles = HabitacionCampismo.objects.filter(campismo=id, estado='D').values('estado').annotate(
        cant=Count('estado'))
    if cant_hab_disponibles.count() == 0:
        cant_hab_disponibles = 0
    else:
        cant_hab_disponibles = cant_hab_disponibles.get()['cant']

    for fecha, cant in result.items():
        if cant == cant_hab_disponibles:
            fechas_cancel.append(fecha)

    if (len(fechas_cancel) > 0):
        data = {'message': "success", 'fechas_cancel': fechas_cancel}
    else:
        data = {'message': "Not Found"}

    return JsonResponse(data)

def generarIdReserva():
    abecedario = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    id = ''
    for x in range(8):
        if x < 3:
            id += random.choice(abecedario)
        else:
            id += str(random.randint(1, 9))

    if len(list(ReservaCampismo.objects.filter(idReserva=id, estado='ET').values())) > 0:
        return generarIdReserva()
    else:
        return id

class Excursiones(TemplateView):
    template_name = 'buscar_excursiones.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["actual"] = 'e'
        return context
    
class ListaExcursiones(ListView):
    model = Excursion
    
    def get_queryset(self, **kwargs):
        excursiones = Excursion.objects.filter(precio__gte=kwargs['precioMin'], precio__lte=kwargs['precioMax'])

        if kwargs['keywords'] == '*all':
            excursiones = list(excursiones.values())
        else:
            e = excursiones
            e = list(e.filter(nombre__contains=kwargs['keywords']).values())
            if len(e) == 0:
                excursiones = list(excursiones.filter(
                    destino__contains=kwargs['keywords']).values())
            else:
                excursiones = e

        for e in excursiones:
            i = InstanciaExcursion.objects.filter(
                excursion=e['id'], estado='A').count()
            e['instancias'] = i
            if i == 0 and kwargs['disponible'] == 'True':
                excursiones.remove(e)
                
        return excursiones
    
    
    def get(self, request, *args, **kwargs):
        excursiones = self.get_queryset(**kwargs)
        if len(excursiones) > 0:
            data = {
                'message': 'success',
                'excursiones': excursiones
            }
        else:
            data = {
                'message': 'Not Found'
            }

        return JsonResponse(data)     

class ExcursionDetalle(DetailView):
    model = Excursion
    template_name = 'detalles_excursiones.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        
        context['excursion'] = self.get_object()
        
        instancias = list(InstanciaExcursion.objects.filter(excursion=self.get_object(), estado='A').values('id', 'fecha', 'capacidad').order_by('fecha'))

        for i in instancias:
            reservas = list(ReservaExcursion.objects.filter(instancia=i['id'], estado='ET').values())
            x = 0
            for r in reservas:
                x += r['cantP']
            i['reservas'] = x
        
        context['instancias'] = instancias
        
        comentarios_padres = ComentarioExcursion.objects.filter(excursion=self.get_object(), padre=0).order_by('-fecha')
        comentarios_hijos = []
        for c in comentarios_padres:
            hijos = ComentarioExcursion.objects.filter(excursion=self.get_object(), padre=c.pk)
            elemento = {}
            elemento['padre'] = c.pk
            elemento['hijos'] = hijos
            comentarios_hijos.append(elemento)
        
        context['padres'] = comentarios_padres
        context['hijos'] = comentarios_hijos
        
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        comentario = ComentarioExcursion(excursion=self.get_object(), usuario=request.user, texto=request.POST['texto'],
                                         padre=request.POST['comm'])
        comentario.save()
        return redirect('excD', self.get_object().pk)
 
class ReservarExcursion(LoginRequiredMixin, View): 
    template_name = 'reservar_excursion.html'
    
    def get(self, request, *args, **kwargs):
        context = {}
        context['instancia'] = InstanciaExcursion.objects.get(pk=kwargs['id'])
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):

        capacidad = InstanciaExcursion.objects.get(pk=kwargs['id']).capacidad
        cantR = InstanciaExcursion.objects.filter(pk=kwargs['id']).annotate(total=Sum('instancia_reserva__cantP')).values().get()['total']

        if cantR is None:
            cantR = 0

        if (capacidad - cantR) >= int(request.POST['cantP']):
            nuevo = ReservaExcursion(idReserva=generarIdReservaExcursion(),
                                    instancia=InstanciaExcursion.objects.get(pk=kwargs['id']), usuario=request.user,
                                    estado="ET", cantP=int(request.POST['cantP']))
            nuevo.save()
            return redirect('reservas', request.user.username)
        else:
            return render(request, self.template_name, {
                'instancia': InstanciaExcursion.objects.get(pk=kwargs['id']),
                'error': 'Su cantidad de personas excede a la cantidad de personas disponibles'
            })
        
@login_required
def responder_comentario(request, pk, exc):
    comentario = ComentarioExcursion(excursion=Excursion.objects.get(pk=exc), usuario=request.user, texto=request.POST['texto'],
                                         padre=request.POST['comm'])
    comentario.save()
    return redirect('excD', exc)
       
def generarIdReservaExcursion():
    abecedario = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    id = ''
    for x in range(6):
        if x < 2:
            id += random.choice(abecedario)
        else:
            id += str(random.randint(1, 9))

    if len(list(ReservaExcursion.objects.filter(idReserva=id, estado='ET').values())) > 0:
        return generarIdReservaExcursion()
    else:
        return id
        
class Oficinas(TemplateView):
    template_name = 'buscar_oficinas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['actual'] = 'o'
        return context
   
class ListarOficinas(ListView):
    model = Oficina
    
    def get_queryset(self, **kwargs):
        if kwargs['keywords'] == "*all":
            oficina = list(Oficina.objects.all().values())
        else:
            oficina = list(Oficina.objects.filter(nombre__contains=kwargs['keywords']).values())
        return oficina
    
    def get(self, request, *args, **kwargs):
        oficina = self.get_queryset(**kwargs)
        if len(oficina) > 0:
            data = {
                'message': 'success',
                'oficinas': oficina
            }
        else:
            data = {
                'message': 'Not Found'
            }

        return JsonResponse(data)
    
class CambiarFoto(LoginRequiredMixin, TemplateView):
    template_name = 'cambiar_foto.html'
    
    def post(self, request, *args, **kwargs):
        ruta=request.FILES.get('foto') #Retorna la ruta del archivo
        user = Usuario.objects.get(username=kwargs['pk'])
        user.foto = ruta
        user.save()
        return redirect('perfil', kwargs['pk'])

class Reservas(LoginRequiredMixin, TemplateView):
    template_name = 'reservas.html'
    
    def get_queryset(self, model, idR, user):
        if idR == "":
            query = model.objects.filter(usuario=Usuario.objects.get(username=user))
        else:
            query = model.objects.filter(idReserva__contains=idR, usuario=Usuario.objects.get(username=user))
        return query
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas_campismo'] = self.get_queryset(ReservaCampismo, kwargs['idR'], kwargs['pk'])
        context['reservas_excursion'] = self.get_queryset(ReservaExcursion, kwargs['idR'], kwargs['pk']) 
        context['tabs'] = 'reservas'
        return context
    
    def dispatch(self, request, *args, **kwargs):
        usuario = Usuario.objects.get(username=kwargs['pk'])
        if request.user != usuario:
            return redirect('index')
        else:
            return super(Reservas,self).dispatch(request,*args,**kwargs)
    
    def get(self, request, *args, **kwargs):
        kwargs['idR'] = ''
        return render(request, self.template_name, self.get_context_data(**kwargs))
        
    def post(self, request, *args, **kwargs):
        kwargs['idR'] = request.POST['keywords']
        return render(request, self.template_name, self.get_context_data(**kwargs))

class CancelarReservaCampismo(LoginRequiredMixin, DeleteView):
    model = ReservaCampismo
    
    def get_success_url(self):
        return reverse_lazy('reservas', kwargs={'pk':self.kwargs['username']})
    
class CancelarReservaExcursion(LoginRequiredMixin, DeleteView):
    model = ReservaExcursion
    
    def get_success_url(self):
        return reverse_lazy('reservas', kwargs={'pk':self.kwargs['username']})

    
    