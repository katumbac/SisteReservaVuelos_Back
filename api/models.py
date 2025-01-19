from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.   
class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contrasena = models.CharField(max_length=255)
    registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Aeropuerto(models.Model):
    nombre = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=100)
    pais = models.CharField(max_length=100)
    codigo_iata = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.nombre

class Vuelo(models.Model):
    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    fecha = models.DateField()
    horario = models.TimeField()
    disponibilidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.origen} -> {self.destino}"


class VueloXAeropuerto(models.Model):
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    aeropuerto = models.ForeignKey(Aeropuerto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=7, choices=[('origen', 'Origen'), ('destino', 'Destino')])

    class Meta:
        unique_together = ['vuelo', 'aeropuerto', 'tipo']

    def __str__(self):
        return f"{self.vuelo} - {self.aeropuerto} ({self.tipo})"

class ReservaXVuelo(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada')
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    vuelo = models.ForeignKey(Vuelo, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES)
    asientos = models.IntegerField()

    def __str__(self):
        return f"Reserva {self.id} - {self.usuario.nombre} {self.estado}"

class Pago(models.Model):
    METODO_PAGO_CHOICES = [
        ('tarjeta', 'Tarjeta'),
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia')
    ]
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado')
    ]

    reserva = models.ForeignKey(ReservaXVuelo, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES)
    fecha_pago = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_PAGO_CHOICES)

    def __str__(self):
        return f"Pago {self.id} - {self.monto} - {self.estado}"