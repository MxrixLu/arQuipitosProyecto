import eventos.logic as logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def eventos(request):
    if request.method == 'GET':
        eventos = logic.get_eventos()
        print(f"Retrieved {len(eventos)} eventos from the database.")
        return JsonResponse([event.__dict__ for event in eventos], safe=False, status=200)