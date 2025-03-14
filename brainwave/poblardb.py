import os
import django
import random
from django.utils.timezone import now
from brainwave.eventos_medicos.models import Examen, ImagenResonancia

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brainwave.settings")
django.setup()

def poblar_base_de_datos():
    imagenes_path = "imagenes_data_set/"  # Ruta donde están las imágenes
    imagenes = [img for img in os.listdir(imagenes_path) if img.endswith(('jpg', 'png', 'jpeg', 'webp'))]
    
    if not imagenes:
        print("No hay imágenes en la carpeta.")
        return

    pacientes = ["Juan Pérez", "María Gómez", "Carlos López", "Ana Rodríguez"]
    tipos_examen = ["IRM", "PET", "Tomografía"]
    
    for i, imagen in enumerate(imagenes, start=1):
        paciente = random.choice(pacientes)
        tipo_examen = random.choice(tipos_examen)
        
        # Crear un nuevo examen
        examen = Examen.objects.create(
            paciente=paciente,
            fecha=now(),
            tipo_examen=tipo_examen,
            descripcion=f"Examen {tipo_examen} de {paciente} generado automáticamente."
        )
        
        # Asociar imagen al examen
        imagen_resonancia = ImagenResonancia.objects.create(
            medico="Dr. Smith",
            paciente=paciente,
            examen=examen,
            imagen=f"resonancias/{imagen}",  # Se guarda la ruta relativa
            fecha_subida=now()
        )
        
        print(f"✔️ Se creó el examen y la imagen: {imagen} para {paciente}")

if __name__ == "__main__":
    poblar_base_de_datos()
