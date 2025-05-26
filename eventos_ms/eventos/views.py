import eventos.logic as logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

@api_view(['GET', 'POST'])
def eventos(request):
    if request.method == 'GET':
        eventos = logic.get_eventos()
        return JsonResponse([event.__dict__ for event in eventos], safe=False, status=200)

    elif request.method == 'POST':
        # Parse the incoming JSON data
        data = JSONParser().parse(request)
        # Here you would typically save the data to the database
        response_data = {"message": "Data received", "data": data}
        return JsonResponse(response_data, status=201)