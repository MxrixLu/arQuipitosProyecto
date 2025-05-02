from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def medical_history(request):
    if request.method == 'GET':
        # Example response for GET request
        return JsonResponse({
            'message': 'Medical history retrieved successfully',
            'data': []
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Process the received data here
            return JsonResponse({
                'message': 'Medical history created successfully',
                'data': data
            })
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)