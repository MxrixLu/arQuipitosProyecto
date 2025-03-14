from django.db import models

# Create your models here.
from django.db import models

class Examen(models.Model):
    paciente = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)
    tipo_examen = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Examen de {self.paciente} - {self.tipo_examen}"
    
class ImagenResonancia(models.Model):
    id = models.AutoField(primary_key=True)
    medico = models.CharField(max_length=255, null=True, blank=True)  
    paciente = models.CharField(max_length=255, null=True, blank=True)  
    examen = models.ForeignKey(Examen, related_name='imagenes', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='resonancias/')
    fecha_subida = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Imagen para {self.examen}"