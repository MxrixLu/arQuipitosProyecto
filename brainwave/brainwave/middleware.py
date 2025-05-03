# brainwave/middleware.py

from django.http import HttpResponseBadRequest

class SQLInjectionProtectionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP', '--', ';']

    def __call__(self, request):
        # Revisar el path de la URL
        path = request.path.upper()
        if any(keyword in path for keyword in self.keywords):
            return HttpResponseBadRequest("Solicitud bloqueada: contenido sospechoso en la URL.")

        # Revisar los parámetros GET
        for key, value in request.GET.items():
            if any(keyword in value.upper() for keyword in self.keywords):
                return HttpResponseBadRequest("Solicitud bloqueada: contenido sospechoso en los parámetros.")

        return self.get_response(request)
