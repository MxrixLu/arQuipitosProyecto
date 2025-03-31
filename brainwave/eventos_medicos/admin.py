from django.contrib import admin
from .models import Examen  
from .models import ImagenResonancia
from .models import DiagnosticoMRI

admin.site.register(Examen)  
admin.site.register(ImagenResonancia)
admin.site.register(DiagnosticoMRI)