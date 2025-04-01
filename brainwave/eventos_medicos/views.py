import random
import os
import shutil
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.conf import settings
from django.utils.timezone import now
from .models import Examen, ImagenResonancia, DiagnosticoMRI
from .forms import ImagenResonanciaForm

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media')

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
    data = [
        {"id": r.id, "imagen": r.imagen.url, "fecha": r.fecha_subida, "paciente": r.paciente, "medico": r.medico, "descripcion": r.descripcion,  
            "diagnostico_url": f"/diagnostico/{r.diagnostico.id}/" if r.diagnostico else None}
        for r in resonancias
    ]
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
        
        generar_diagnostico_mri(examen.id)
        
        

    return JsonResponse({'status': 'success', 'message': '10,000 imágenes generadas con pacientes diferentes.'})

def eliminar_imagenes(request):
    destino_dir = os.path.join(settings.MEDIA_ROOT, 'resonancias')
    
    if os.path.exists(destino_dir):
        for archivo in os.listdir(destino_dir):
            if archivo.startswith("resonancia_paciente_") and archivo.endswith(".webp"):
                os.remove(os.path.join(destino_dir, archivo))
    
    ImagenResonancia.objects.filter(imagen__startswith="resonancias/resonancia_paciente_").delete()
    Examen.objects.filter(descripcion="Examen generado automáticamente para prueba").delete()
    
    return JsonResponse({'status': 'success', 'message': 'Imágenes y registros eliminados.'})

def generar_diagnosticos_masivos(request):
    destino_dir = os.path.join(settings.MEDIA_ROOT, 'resonancias')
    os.makedirs(destino_dir, exist_ok=True)

    imagen_base_path = os.path.join(destino_dir, 'imagen_1.png')
    if not os.path.exists(imagen_base_path):
        return JsonResponse({'error': 'No existe la imagen base en media/resonancias/'}, status=400)

    diagnosticos_texto = [
        "El paciente presenta signos de epilepsia.",
        "No se observan anomalías en la resonancia.",
        "Posible indicio de tumor cerebral.",
        "Se detectan áreas de inflamación en la corteza cerebral.",
        "El paciente muestra signos de esclerosis múltiple.",
        "Presencia de lesión vascular, posible ACV."
    ]

    examenes = list(Examen.objects.all())
    nuevos_diagnosticos = []
    for i in range(2, 100):
        nombre_paciente = f'Paciente_{i}'
        nombre_medico = f'Médico_{random.randint(1, 100)}'
        nombre_archivo = f'imagen_{i}.png'
        nueva_ruta = os.path.join(destino_dir, nombre_archivo)
        shutil.copy(imagen_base_path, nueva_ruta)

        examen = random.choice(examenes) if examenes else Examen.objects.create(
            paciente=nombre_paciente,
            tipo_examen="Resonancia Magnética",
            descripcion="Examen generado automáticamente para pruebas"
        )

        diagnostico = DiagnosticoMRI(
            medico=nombre_medico,
            paciente=nombre_paciente,
            examen=examen,
            imagen=f'resonancias/{nombre_archivo}',
            analisis=random.choice(diagnosticos_texto)
        )
        nuevos_diagnosticos.append(diagnostico)

    DiagnosticoMRI.objects.bulk_create(nuevos_diagnosticos)
    
    return JsonResponse({'status': 'success', 'message': '1,000 diagnósticos generados.'})

def generar_diagnostico_mri( examen_id):
    examen = get_object_or_404(Examen, id=examen_id)
    
    imagen_resonancia = ImagenResonancia.objects.filter(examen=examen).order_by('-fecha_subida').first()
    
    if not imagen_resonancia:
        print(f"No se encontró imagen para el examen {examen_id}")
        return  

    diagnosticos_texto = [
        "El paciente presenta signos de epilepsia.",
        "No se observan anomalías en la resonancia.",
        "Posible indicio de tumor cerebral.",
        "Se detectan áreas de inflamación en la corteza cerebral.",
        "El paciente muestra signos de esclerosis múltiple.",
        "Presencia de lesión vascular, posible ACV."
    ]

    analisis = random.choice(diagnosticos_texto)

    diagnostico = DiagnosticoMRI.objects.create(
        medico=imagen_resonancia.medico,
        paciente=imagen_resonancia.paciente,
        examen=examen,
        imagen=imagen_resonancia.imagen,
        analisis=analisis
    )

    imagen_resonancia.descripcion = diagnostico.analisis  
    imagen_resonancia.diagnostico = diagnostico  
    imagen_resonancia.save()

    print(f"Imagen {imagen_resonancia.id} actualizada con diagnóstico: {imagen_resonancia.descripcion}")

def listar_diagnosticos(request):
    diagnosticos = DiagnosticoMRI.objects.select_related("examen").order_by('-id')
    data = [
        {
            "id": d.id,
            "medico": d.medico,
            "paciente": d.paciente,
            "examen": d.examen.tipo_examen,
            "imagen": d.imagen.url,
            "analisis": d.analisis
        }
        for d in diagnosticos
    ]
    return JsonResponse({"diagnosticos": data})

def eliminar_diagnosticos(request):
    destino_dir = os.path.join(settings.MEDIA_ROOT, 'resonancias')
    
    if os.path.exists(destino_dir):
        for archivo in os.listdir(destino_dir):
            if archivo.startswith("resonancia_paciente_") and archivo.endswith(".webp"):
                os.remove(os.path.join(destino_dir, archivo))

    DiagnosticoMRI.objects.all().delete()
    
    return JsonResponse({'status': 'success', 'message': 'Diagnósticos eliminados.'})


