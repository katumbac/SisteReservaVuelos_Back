from rest_framework import serializers
from .models import Usuario, Aeropuerto, Vuelo, VueloXAeropuerto, ReservaXVuelo, Pago
   
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class AeropuertoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aeropuerto
        fields = "__all__"

class VueloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vuelo
        fields = "__all__"

class ReservaXVueloSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    vuelo = VueloSerializer(read_only=True)

    class Meta:
        model = ReservaXVuelo
        fields = "__all__"

class PagoSerializer(serializers.ModelSerializer):
    reserva = ReservaXVueloSerializer(read_only=True)

    class Meta:
        model = Pago
        fields = "__all__"

class VueloXAeropuertoSerializer(serializers.ModelSerializer):
    vuelo = VueloSerializer(read_only=True)
    aeropuerto = AeropuertoSerializer(read_only=True)
    
    class Meta:
        model = VueloXAeropuerto
        fields = "__all__"

    def create(self, validated_data):
        vuelo_data = validated_data.pop('vuelo')
        aeropuerto_data = validated_data.pop('aeropuerto')
        vuelo = Vuelo.objects.get(id=vuelo_data['id_vuelo'])
        aeropuerto = Aeropuerto.objects.get(id=aeropuerto_data['id_aeropuerto'])
        vuelo_aeropuerto = VueloXAeropuerto.objects.create(
            vuelo=vuelo,
            aeropuerto=aeropuerto,
            tipo=validated_data['tipo']
        )
        return vuelo_aeropuerto