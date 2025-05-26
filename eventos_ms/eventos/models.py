from django.db import models

# Create your models here.

class Evento(models.Model):

    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    hora = models.TimeField()
    lugar = models.CharField(max_length=100)
    descripcion = models.TextField()

    opciones_tipo = [
        ('consulta', 'Consulta'),
        ('examen', 'Examen'),
        ('cirugia', 'Cirugía'),
        ('prescripcion', 'Prescripción'),
    ]


    pacinete = models.ForeignKey('Paciente', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    edad = models.IntegerField()
    opciones_sexo = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
    ]
    sexo = models.CharField(max_length=10, choices=opciones_sexo)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Doctor(models.Model):
    id = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre