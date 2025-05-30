from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('mi_app.urls')),  # <-- cambia 'mi_app' por el nombre real de tu app
    path('admin/', admin.site.urls),
]
