from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *

class RegistrarUsuarioView(APIView):
    
    def post(self, request):
        try:
            nombre = request.data.get('nombre')
            apellido = request.data.get('apellido')
            correo = request.data.get('correo')
            contrasena = request.data.get('contrasena')
            email = correo
            password = contrasena
            user = User.objects.create_user(username=email, email=email, password=password)
            usuario = Usuario(nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena)
            usuario.save()
            return Response({"detail": "User created successfully!"}, status=200)
        except Exception as e:
            return Response({"detail": f"Error: {str(e)}"}, status=400)


class LoginUsuarioView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password= request.data.get('password')
        if not username or not password:
            return Response({'detail': 'Correo y contraseña son requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

        usuarios = User.objects.all()

        for usuario in usuarios:
            print(f"Username: {usuario.password}, Email: {usuario.email}, Activo: {usuario.is_active}")
            
        print("usu", username)
        print("pass", password)
        usuario = authenticate(request, username=username, password=password)
        print("usu", usuario)

        if usuario is None:
            return Response({'detail': 'Credenciales incorrectas.'}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(usuario)
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_200_OK)

class UsuarioViewSet(APIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        reservas = ReservaXVuelo.objects.filter(usuario=usuario)
        if not reservas.exists():
            return Response({"message": "No hay reservas para este usuario."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReservaXVueloSerializer(reservas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AeropuertoViewSet(APIView):
    queryset = Aeropuerto.objects.all()
    serializer_class = AeropuertoSerializer
    
    def get(self, request):
        aeropuerto = Aeropuerto.objects.all()  
        serializer = AeropuertoSerializer(aeropuerto, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VueloViewSet(APIView):
    queryset = Vuelo.objects.all()
    serializer_class = VueloSerializer
    
    def get(self, request):
        origen = request.data.get('origen')
        destino = request.data.get('destino')
        fecha = request.data.get('fecha')
        vuelos = Vuelo.objects.all()
        print(vuelos)
        vuelos = vuelos.filter(origen=origen, destino=destino, fecha=fecha)
        print(vuelos)
        if not vuelos.exists():
            return Response({"message": "No hay vuelos disponibles que coincidan con los parámetros."}, status=status.HTTP_404_NOT_FOUND)

        serializer = VueloSerializer(vuelos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, *args, **kwargs):
        serializer = VueloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VueloXAeropuertoViewSet(APIView):
    queryset = VueloXAeropuerto.objects.all()
    serializer_class = VueloXAeropuertoSerializer
    
    def get(self, request):
        vuelo = VueloXAeropuerto.objects.all()  
        serializer = VueloXAeropuertoSerializer(vuelo, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReservaXVueloViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        reservas = ReservaXVuelo.objects.all()  
        serializer = ReservaXVueloSerializer(reservas, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK) 
    
    def post(self, request):
        vuelo_id = request.data.get('vuelo')
        usuario_id = request.data.get('usuario')

        vuelo_id = int(vuelo_id)
        usuario_id = int(usuario_id)
        try:
            vuelo = Vuelo.objects.get(id=vuelo_id)
        except Vuelo.DoesNotExist:
            return Response({"message": "Vuelo no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response({"message": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if vuelo.disponibilidad <= 0:
            return Response({"message": "No hay disponibilidad para este vuelo."}, status=status.HTTP_400_BAD_REQUEST)
        
        reserva = ReservaXVuelo(vuelo=vuelo, usuario=usuario, estado="Pendiente", asientos=1)
        reserva.save()
        
        vuelo.disponibilidad -= 1
        vuelo.save()

        return Response({
            "mensaje": "Reserva creada",
            "vueloId": vuelo_id,
            "usuarioId": usuario_id,
            "id": reserva.id
        }, status=status.HTTP_201_CREATED)
        
    def delete(self, request, id):
        try:
            reserva = ReservaXVuelo.objects.get(id=id)
        except ReservaXVuelo.DoesNotExist:
            return Response({"message": "Reserva no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        vuelo = reserva.vuelo
        vuelo.disponibilidad += 1
        vuelo.save()
        reserva = ReservaXVuelo(vuelo=vuelo, usuario=reserva.usuario, estado="Cancelada", asientos=1)
        reserva.save()
        return Response({"message": "Reserva cancelada"}, status=status.HTTP_200_OK)
    

class PagoViewSet(APIView):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    
    def get(self, request):
        pago = Pago.objects.all()  
        serializer = PagoSerializer(pago, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)