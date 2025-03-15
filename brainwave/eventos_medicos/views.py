import random
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from brainwave.brainwave.settings import BASE_DIR
from .models import Examen, ImagenResonancia
from .forms import ImagenResonanciaForm
from django.shortcuts import render
from .models import Examen
import shutil
import os


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

def cargar_imagen(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    if request.method == 'POST':
        form = ImagenResonanciaForm(request.POST, request.FILES)
        if form.is_valid():
            imagen = form.save(commit=False)
            imagen.examen = examen
            imagen.save()
            return JsonResponse({'status': 'success', 'imagen_id': imagen.id})
    return JsonResponse({'status': 'error'})


def ver_imagenes(request, examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    imagenes = examen.imagenes.all()
    return render(request, 'ver_imagenes.html', {'examen': examen, 'imagenes': imagenes})

def lista_imagenes_resonancias(request):
    resonancias = ImagenResonancia.objects.all().order_by('-fecha_subida')
    data = [{"id": r.id, "imagen": r.imagen.url, "fecha": r.fecha_subida, "paciente": r.paciente, "medico": r.medico} for r in resonancias]
    return JsonResponse({"resonancias": data})

def vista_resonancias(request):
    return render(request, 'eventos_medicos/lista_eventos.html')

def generar_imagenes(request):
    imagen_base_path = os.path.join(settings.MEDIA_ROOT, 'resonancias', 'resonancia_magnetica_cerebral_lesiones.webp')
    
    if not os.path.exists(imagen_base_path):
        return JsonResponse({'error': 'La imagen base no existe en media/resonancias/'}, status=400)

    destino_dir = os.path.join(settings.MEDIA_ROOT, 'resonancias')
    os.makedirs(destino_dir, exist_ok=True)
    
    for i in range(1, 10001):
        nombre_paciente = f'Paciente_{i}' 
        nombre_archivo = f'resonancia_paciente_{i}.webp'
        nueva_ruta = os.path.join(destino_dir, nombre_archivo)
        
        shutil.copy(imagen_base_path, nueva_ruta)

        examen = Examen.objects.create(
            paciente=nombre_paciente,
            tipo_examen="Resonancia Magnética",
            descripcion="Examen generado automáticamente para prueba"
        )

        ImagenResonancia.objects.create(
            examen=examen,
            imagen=f'resonancias/{nombre_archivo}',  
            paciente=nombre_paciente,
            medico=f'Médico_{random.randint(1, 100)}'
        )

    return JsonResponse({'status': 'success', 'message': '10,000 imágenes generadas con pacientes diferentes.'})