from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dj_rest_auth.views import LoginView
from api import views as api_views
from api.views import *



urlpatterns = [
    #Registrar
    path('registrarse/', RegistrarUsuarioView.as_view(), name="Registrarse"),
    path('login/', LoginUsuarioView.as_view(), name="Login"),
    #Vuelo
    path('vuelos', VueloViewSet.as_view(), name="Buscar Vuelos"),
    path('vuelos/<int:pk>', VueloViewSet.as_view(), name='Editar vuelo'),
    path('crear_vuelos', VueloViewSet.as_view(), name="Crear Vuelos"),
    
    #Reserva
    path('reservas', ReservaXVueloViewSet.as_view(), name="Reservar Vuelos"),
    path('reservas/<int:id>', ReservaXVueloViewSet.as_view(), name='Cancelar Reserva'),
    
    #Usuario
    path('usuarios/<int:usuario_id>/reservas/', UsuarioViewSet.as_view(), name='Reservas Por Usuario'),
]