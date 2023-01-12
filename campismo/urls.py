from django.urls import path
from .views import Index, Reservas, CancelarReservaCampismo, CancelarReservaExcursion, Perfil, CambiarFoto, EditarPerfil, Campismos, ListaCampismos, ReservarCampismo, CampisoDetalles,Excursiones,ExcursionDetalle, responder_comentario,ListaExcursiones,ReservarExcursion,Oficinas, getFechasCanceladas, ListarOficinas

urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('perfil/<str:pk>/', Perfil.as_view(), name='perfil'),
    path('perfil/<str:pk>/cambiar_foto/', CambiarFoto.as_view(), name='cambiar_foto'),
    path('perfil/<str:pk>/editar/', EditarPerfil.as_view(), name='editar_usuario'),
    path('campismos/', Campismos.as_view(), name="campismos"),
    path('campismos/<int:pk>/', CampisoDetalles.as_view(), name="campD"),
    path('campismos/reservar/<int:id>/', ReservarCampismo.as_view(), name="reservar_campismo"),
    path('campismos/buscar/lista/<str:keywords>/<str:provincia>/<int:val>/<int:minPrecio>/<int:maxPrecio>/<int:categoria>/<str:turismo>/', ListaCampismos.as_view(), name="getCampismosList"),
    path('campismos/reservar/<int:id>/getFechasCancel/', getFechasCanceladas, name="getFechasCancel"),
    path('excursiones/', Excursiones.as_view(), name="excursiones"),
    path('excursiones/<int:pk>/responder_comentario/<int:exc>', responder_comentario, name="responder_comentario"),
    path('excursiones/<int:pk>/', ExcursionDetalle.as_view(), name="excD"),
    path('excursiones/reservar/<int:id>/', ReservarExcursion.as_view(), name="reservar_excursiones"),
    path('excursiones/lista/<str:keywords>/<str:disponible>/<int:precioMin>/<int:precioMax>/', ListaExcursiones.as_view()),
    path('oficinas/', Oficinas.as_view(), name="oficinas"),
    path('oficinas/<str:keywords>', ListarOficinas.as_view()),
    path('<str:pk>/mis_reservas/', Reservas.as_view(), name='reservas'),
    path('<str:username>/mis_reservas/cancelar_campismo/<str:pk>/', CancelarReservaCampismo.as_view(), name='cancelar_campismo'),
    path('<str:username>/mis_reservas/cancelar_excursion/<str:pk>/', CancelarReservaExcursion.as_view(), name='cancelar_excursiones'),
]