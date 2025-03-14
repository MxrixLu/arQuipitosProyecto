from django import forms
from .models import ImagenResonancia

class ImagenResonanciaForm(forms.ModelForm):
    class Meta:
        model = ImagenResonancia
        fields = ['imagen']  # Solo el campo de la imagen

class ImagenResonanciaForm(forms.ModelForm):
    class Meta:
        model = ImagenResonancia
        fields = ['imagen']

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen:
            # Verifica que el archivo sea una imagen
            if not imagen.content_type.startswith('image'):
                raise forms.ValidationError("El archivo debe ser una imagen.")
            # Limita el tamaño del archivo (por ejemplo, 5 MB)
            if imagen.size > 5 * 1024 * 1024:
                raise forms.ValidationError("La imagen no puede superar los 5 MB.")
        return imagen