from django.db import models

# Create your models here.

class HistorialMedico(models.Model):
    created_at = models.DateField(auto_now_add=True)
    paciente = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    sexo = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    contraindicaciones = models.TextField(blank=True, null=True)
    diagnostico = models.TextField()
    tratamiento = models.TextField()
    seguimiento = models.TextField()
