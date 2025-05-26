import eventos.logic as logic
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def eventos(request):
    try:
        if request.method == 'GET':
            return logic.get_eventos()
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            return logic.create_evento(data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)