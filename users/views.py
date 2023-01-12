from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import View, TemplateView, CreateView, ListView, DeleteView, FormView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import login, logout
from .models import Usuario
from django.urls import reverse_lazy
from .forms import LoginForm, UsuarioForm, RolForm, UsuarioEditForm, PermissionForm, ProvinciaForm, CampismoForm, HabitacionCampismoForm, OficinaForm, ExcursionForm, InstanciaForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.decorators import login_required, permission_required
from campismo.models import Provincia, Campismo, Excursion, Oficina, HabitacionCampismo, InstanciaExcursion
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage

from .tokens import account_activation_token

# Create your views here.
class Principal(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    permission_required = ('users.acceso_panel',)
    template_name = 'panel_principal.html'

class IniciarSesion(FormView): 
    template_name = 'iniciar_sesion.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(IniciarSesion,self).dispatch(request,*args,**kwargs)
        
    def form_valid(self, form):
        login(self.request,form.get_user())
        return super(IniciarSesion,self).form_valid(form)
            
@login_required
def desconectar(request):
    logout(request)
    return redirect('index')
    
class RegistrarUsuario(View):
    template_name = 'registrar_usuario.html'
    success_url = reverse_lazy('index')
    
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        else:
            return super(RegistrarUsuario,self).dispatch(request,*args,**kwargs)
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        f = request.POST
        
        if not Usuario.objects.filter(username=f['username']).exists():
            if not Usuario.objects.filter(email=f['email']).exists():
                if f['password1'] == f['password2']:
                    user = Usuario(
                        username = f['username'],
                        email = f['email'],
                        nombre = f['nombre'],
                        apellidos = f['apellidos'],
                        pais = f['pais']
                    )
                    
                    user.set_password(f['password1'])
                    user.save()
                    
                    login(request, user)
                    
                    return redirect('index')
                else:
                    return render(request, self.template_name, {
                        'error': 'pass'
                    })
            else:
                return render(request, self.template_name, {
                    'error': 'email'
                })
        else:
            return render(request, self.template_name, {
                'error': 'user'
            })
            
class ListarUsuarios(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = ('users.view_usuario')
    model = Usuario
    template_name = 'panel_usuarios.html'
    context_object_name = 'usuarios'
    queryset = Usuario.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tabs'] = 'usuarios'
        return context

class CrearUsuarios(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = ('users.add_usuario')
    model = Usuario
    form_class = UsuarioForm
    template_name = 'panel_info_usuarios.html'
    success_url = reverse_lazy('panel_usuarios')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['accion'] = 'crear'
        context['grupos'] = Group.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        user = self.get_form().save(commit=False)
        user.set_password(request.POST['password'])
        user.save()
        user.groups.clear()
        grupos = request.POST.getlist('roles')
        for g in grupos:
            user.groups.add(Group.objects.get(name=g))
        return redirect('panel_usuarios')

class EditarUsuario(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('users.change_usuario')
    model = Usuario
    form_class = UsuarioEditForm
    template_name = 'panel_info_usuarios.html'
    success_url = reverse_lazy('panel_usuarios')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['accion'] = 'editar'
        context['grupos'] = Group.objects.all()
        context['object_grupos'] = self.get_object().groups.all().values_list('name')
        return context
    
    def post(self, request, *args, **kwargs):
        f = self.get_form()
        user = Usuario.objects.get(username=self.get_object().username)
        user.username = f['username'].value()
        user.email = f['email'].value()
        user.nombre = f['nombre'].value()
        user.apellidos = f['apellidos'].value()
        user.pais = f['pais'].value()
        user.telefono = f['telefono'].value()
        user.sexo = f['sexo'].value()
        user.save()
        user.groups.clear()
        grupos = request.POST.getlist('roles')
        for g in grupos:
            user.groups.add(Group.objects.get(name=g))
        
        return redirect('panel_usuarios')

class EliminarUsuario(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = ('users.delete_usuario')
    model = Usuario
    success_url = reverse_lazy('panel_usuarios')
        
class AdminRoles(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = ('auth.view_group')
    model = Group
    form_class = RolForm
    context_object_name = 'grupos'
    template_name = 'panel_roles.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tabs'] = 'roles'
        context['form'] = self.form_class
        return context
    
    def post(self, request, *args, **kwargs):
        f = request.POST
        
        if not Group.objects.filter(name=f['name']).exists():
            Group.objects.create(name = f['name'])
        
        return redirect('panel_roles')

class EditarRoles(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('auth.change_group')
    model = Group
    form_class = RolForm
    template_name = 'panel_editar_roles.html'
    success_url = reverse_lazy('panel_roles')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['permisos'] = Permission.objects.all() 
        return context
        
@login_required
@permission_required('auth.change_group')
def agregar_permisos(request, pk):
    grupo = Group.objects.get(pk=pk)
    perm = Permission.objects.get(name=request.POST['permiso'])
    grupo.permissions.add(perm)
    return redirect('editar_roles',pk)

@login_required
@permission_required('auth.change_group')
def remover_permisos(request, pk, id):
    grupo = Group.objects.get(pk=pk)
    perm = Permission.objects.get(pk=id)
    grupo.permissions.remove(perm)
    return redirect('editar_roles',pk)

class EliminarRoles(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = ('auth.delete_group')
    model = Group        
    success_url = reverse_lazy('panel_roles')
        
class AdminPermisos(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    permission_required = ('auth.view_permission', 'auth.add_permission')
    model = Permission
    form_class = PermissionForm
    context_object_name = 'permisos'
    template_name = 'panel_permisos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['tabs'] = 'permisos'
        context['form'] = self.form_class
        return context
    
    def post(self, request, *args, **kwargs):
        permiso = self.form_class(request.POST)
        permiso.save()
        return redirect('panel_permisos')
    
class EliminarPermiso(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = ('auth.delete_permission')
    model = Permission
    success_url = reverse_lazy('panel_permisos')
    
class ListarProvincias(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('campismo.view_provincia')
    model = Provincia
    form_class = ProvinciaForm
    template_name = 'panel_provincias.html'
    context_object_name = 'provincias'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'provincias'
        context['form'] = self.form_class
        return context
    
    def post(self, request, *args, **kwargs):
        provincia = self.form_class(request.POST)
        provincia.save()
        return redirect('panel_provincias')

@login_required
@permission_required('campismo.change_provincia')
def editar_provincia(request, pk):
    provincia = Provincia.objects.get(pk=pk)
    provincia.nombre = request.POST['nombre']
    provincia.save()
    
    return redirect('panel_provincias')

class EliminarProvincia(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('campismo.delete_provincia')
    model = Provincia
    success_url = reverse_lazy('panel_provincias')

class ListarCampismos(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('campismo.view_campismo')
    model = Campismo
    context_object_name = 'campismos'
    template_name = 'panel_bases_campismos.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'campismos'
        return context

class CrearCampismo(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('campismo.add_campismo')
    model = Campismo
    form_class = CampismoForm
    template_name = 'panel_info_campismos.html'
    success_url = reverse_lazy('panel_base_campismos')
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['accion'] = 'crear'
        return contexto

class EditarCampismo(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('campismo.change_campismo')
    model = Campismo
    form_class = CampismoForm
    template_name = 'panel_info_campismos.html'
    success_url = reverse_lazy('panel_base_campismos')
    
    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['accion'] = 'editar'
        return contexto

class EliminarCampismo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('campismo.delete_campismo')
    model = Campismo
    success_url = reverse_lazy('panel_base_campismos')

class ListarHabitacionesCampismo(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('campismo.view_habitacioncampismo')
    model = HabitacionCampismo
    form_class = HabitacionCampismoForm
    template_name = 'panel_habitaciones_campismo.html'
    
    def get(self, request,pk, *args, **kwargs):
        object = Campismo.objects.get(pk=pk)
        context = {}
        context['habitaciones'] = HabitacionCampismo.objects.filter(campismo=object)
        context['object'] = object
        context['form'] = self.form_class
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        object = Campismo.objects.get(pk=pk)
        hab = HabitacionCampismo(
            idHab = request.POST['idHab'],
            campismo = object,
            cantidadHuespedes = request.POST['cantidadHuespedes'],
            estado = request.POST['estado']
        )
        hab.save()
        return redirect('listar_habitaciones',pk)

@login_required
@permission_required('campismo.change_habitacioncampismo')
def editar_habitacion(request, pk, id):
    hab = HabitacionCampismo.objects.get(pk=id)
    hab.estado = request.POST['estado']
    hab.save()
    return redirect('listar_habitaciones',pk)    
    
class EliminarHabitacionCampismo(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('campismo.delete_habitacioncampismo')
    model = HabitacionCampismo
    
    def get_success_url(self):
        return reverse_lazy('listar_habitaciones', kwargs={'pk': self.object.campismo.pk})

class ListarExcursiones(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('campismo.view_excursion')
    model = Excursion
    context_object_name = 'excursiones'
    template_name = 'panel_excursiones.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'excursiones'
        return context

class CrearExcursion(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    permission_required = ('campismo.add_excursion')
    model = Excursion
    form_class = ExcursionForm
    template_name = 'panel_info_excursiones.html'
    success_url = reverse_lazy('panel_excursiones')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'crear'
        return context
    
class EditarExcursion(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    permission_required = ('campismo.change_excursion')
    model = Excursion
    form_class = ExcursionForm
    template_name = 'panel_info_excursiones.html'
    success_url = reverse_lazy('panel_excursiones')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'editar'
        return context
    
class EliminarExcursion(LoginRequiredMixin, PermissionRequiredMixin,DeleteView):
    permission_required = ('campismo.delete_excursion')
    model = Excursion
    success_url = reverse_lazy('panel_excursiones')

class ListarInstancias(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('campismo.view_instanciaexcursion')
    model = InstanciaExcursion
    form_class = InstanciaForm
    template_name = 'panel_instancia_excursiones.html'
    
    def get(self, request,pk, *args, **kwargs):
        object = Excursion.objects.get(pk=pk)
        context = {}
        context['instancias'] = InstanciaExcursion.objects.filter(excursion=object)
        context['object'] = object
        context['form'] = self.form_class
        return render(request, self.template_name, context)
    
    def post(self, request, pk, *args, **kwargs):
        object = Excursion.objects.get(pk=pk)
        inst = InstanciaExcursion(
            excursion = object,
            fecha = request.POST['fecha'],
            hora = request.POST['hora'],
            capacidad = request.POST['capacidad'],
            estado = request.POST['estado']
        )
        inst.save()
        return redirect('listar_instancias',pk)   

class EliminarInstancia(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('campismo.delete_instanciaexcursion')
    model = InstanciaExcursion
    
    def get_success_url(self):
        return reverse_lazy('listar_instancias', kwargs={'pk':self.object.excursion.pk})

class ListarOficinas(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = ('campismo.view_oficina')
    model = Oficina
    context_object_name = 'oficinas'
    template_name = 'panel_oficinas.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tabs'] = 'oficinas'
        return context
    
class CrearOficina(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('campismo.add_oficina')
    model = Oficina
    form_class = OficinaForm
    template_name = 'panel_info_oficinas.html'
    success_url = reverse_lazy('panel_oficinas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'crear'
        return context
    
class EditarOficina(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('campismo.change_oficina')
    model = Oficina
    form_class = OficinaForm
    template_name = 'panel_info_oficinas.html'
    success_url = reverse_lazy('panel_oficinas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = 'editar'
        return context

class EliminarOficina(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('campismo.delete_oficina')
    model = Oficina
    success_url = reverse_lazy('panel_oficinas')

class VerificarUsuario(LoginRequiredMixin, DetailView):
    model = Usuario
    context_object_name = 'usuario'
    template_name = 'verificacion_menu.html'

def activateEmail(request, user, to_email):
    usuario = Usuario.objects.get(username=user)
    mail_subject = 'Activate your user account.'
    message = render_to_string('template_activate_account.html', {
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user)),
        'token': account_activation_token.make_token(usuario),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        print('enviado')
    else:
        print('error en el envio')
    
    return redirect('perfil', user)
        
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(username=uid)
    except(TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        user.is_verificado = True
        user.save()

        print('usuario verificado correctamente')
    else:
        print('usuario no verificado')
    
    return redirect('perfil', user.username)