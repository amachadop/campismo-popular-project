from django.urls import path
from .views import EditarUsuario,Principal, IniciarSesion, RegistrarUsuario, AdminPermisos, AdminRoles, ListarUsuarios, EliminarUsuario, CrearUsuarios, EliminarRoles, EditarRoles
from .views import EliminarInstancia,ListarInstancias,CrearExcursion,EditarExcursion,EliminarExcursion,CrearOficina,EditarOficina,EliminarOficina,editar_habitacion,EliminarHabitacionCampismo,ListarHabitacionesCampismo,EditarCampismo,EliminarCampismo,CrearCampismo,editar_provincia,agregar_permisos, remover_permisos, EliminarPermiso, desconectar, ListarProvincias, ListarCampismos, ListarExcursiones, ListarOficinas, EliminarProvincia
from .views import activate, VerificarUsuario, activateEmail

urlpatterns = [
    path('administracion/', Principal.as_view(), name='panel_administrador'),
    path('iniciar_sesion/', IniciarSesion.as_view(), name='iniciar_sesion'),
    path('desconectar/', desconectar, name='desconectar'),
    path('registrar_usuario/', RegistrarUsuario.as_view(), name='crear_usuario'),
    path('administracion/usuarios/', ListarUsuarios.as_view(), name='panel_usuarios'),
    path('administracion/usuarios/crear/', CrearUsuarios.as_view(), name='panel_crear_usuarios'),
    path('administracion/usuarios/eliminar/<str:pk>/', EliminarUsuario.as_view(), name='eliminar_usuarios'),
    path('administracion/usuarios/editar/<str:pk>/', EditarUsuario.as_view(), name='editar_usuarios'),
    path('administracion/roles/', AdminRoles.as_view(), name='panel_roles'),
    path('administracion/roles/eliminar/<int:pk>/', EliminarRoles.as_view(), name='eliminar_roles'),
    path('administracion/roles/editar/<int:pk>/', EditarRoles.as_view(), name='editar_roles'),
    path('administracion/roles/editar/<int:pk>/agregar_permisos/', agregar_permisos, name='agregar_permisos'),
    path('administracion/roles/editar/<int:pk>/remover_permisos/<int:id>/', remover_permisos, name='remover_permisos'),
    path('administracion/permisos/', AdminPermisos.as_view(), name='panel_permisos'),
    path('administracion/permisos/eliminar/<int:pk>', EliminarPermiso.as_view(), name='eliminar_permisos'),
    
    #rutas de verificacion
    path('verificarUsuario/<str:pk>/', VerificarUsuario.as_view(), name='verificar_usuario'),
    path('verificarUsuario/<str:user>/by_email/<str:to_email>/', activateEmail, name='verificar_by_email'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    
    #rutas especialista
    path('administracion/provincias/', ListarProvincias.as_view(), name='panel_provincias'),
    path('administracion/provincias/eliminar/<int:pk>', EliminarProvincia.as_view(), name='eliminar_provincias'),
    path('administracion/provincias/editar/<int:pk>', editar_provincia, name='editar_provincias'),
    path('administracion/base_campismos/', ListarCampismos.as_view(), name='panel_base_campismos'),
    path('administracion/base_campismos/nuevo/', CrearCampismo.as_view(), name='crear_base_campismos'),
    path('administracion/base_campismos/eliminar/<str:pk>', EliminarCampismo.as_view(), name='eliminar_base_campismos'),    
    path('administracion/base_campismos/editar/<str:pk>', EditarCampismo.as_view(), name='editar_base_campismos'),
    path('administracion/base_campismos/<str:pk>/habitaciones/', ListarHabitacionesCampismo.as_view(), name='listar_habitaciones'),
    path('administracion/base_campismos/<str:pk>/habitaciones/editar/<int:id>', editar_habitacion, name='editar_habitaciones'),
    path('administracion/base_campismos/<str:id>/habitaciones/eliminar/<int:pk>/', EliminarHabitacionCampismo.as_view(), name='eliminar_habitaciones'),
    path('administracion/excursiones/', ListarExcursiones.as_view(), name='panel_excursiones'),
    path('administracion/excursiones/crear/', CrearExcursion.as_view(), name='crear_excursiones'),
    path('administracion/excursiones/editar/<int:pk>/', EditarExcursion.as_view(), name='editar_excursiones'),
    path('administracion/excursiones/eliminar/<int:pk>/', EliminarExcursion.as_view(), name='eliminar_excursiones'),
    path('administracion/excursiones/<int:pk>/instancias/', ListarInstancias.as_view(), name='listar_instancias'),
    path('administracion/excursiones/<int:id>/instancias/eliminar/<int:pk>/', EliminarInstancia.as_view(), name='eliminar_instancias'),
    path('administracion/oficinas/', ListarOficinas.as_view(), name='panel_oficinas'),
    path('administracion/oficinas/crear/', CrearOficina.as_view(), name='crear_oficinas'),
    path('administracion/oficinas/editar/<int:pk>/', EditarOficina.as_view(), name='editar_oficinas'),
    path('administracion/oficinas/eliminar/<int:pk>/', EliminarOficina.as_view(), name='eliminar_oficinas'),
]
