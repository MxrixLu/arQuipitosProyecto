from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Examen, ImagenResonancia
from .forms import ImagenResonanciaForm
from django.shortcuts import render
from .models import Examen



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