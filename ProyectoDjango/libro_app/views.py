# ProyectoDjango/libro_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import XMLProcessor, Book
import requests
import json


FLASK_API_URL = 'http://localhost:5000'

def index(request):
    
    context = {
        'page_title': 'Procesador XML - Catálogo de Libros',
        'description': 'Sistema de análisis XML sin persistencia en base de datos',
        'xml_structure_info': Book.get_xml_structure_info()
    }
    return render(request, 'libro_app/index.html', context)

@csrf_exempt
def validate_xml_structure(request):
    
    if request.method == 'POST':
        try:
            xml_content = request.POST.get('xml_content', '')
            
            if not xml_content.strip():
                return JsonResponse({
                    'success': False, 
                    'error': 'No se proporcionó contenido XML'
                })
            
            
            is_valid, message = XMLProcessor.validate_xml_structure(xml_content)
            
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'error': f'Estructura XML inválida: {message}'
                })
            
            
            preview_stats = XMLProcessor.get_basic_stats_preview(xml_content)
            
            return JsonResponse({
                'success': True,
                'message': message,
                'preview_stats': preview_stats,
                'ready_for_processing': True
            })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def upload_xml(request):
    
    if request.method == 'POST':
        try:
            xml_content = request.POST.get('xml_content', '')
            
            if not xml_content.strip():
                return JsonResponse({
                    'success': False, 
                    'error': 'No se proporcionó contenido XML'
                })
            
            
            is_valid, validation_message = XMLProcessor.validate_xml_structure(xml_content)
            if not is_valid:
                return JsonResponse({
                    'success': False,
                    'error': f'XML inválido: {validation_message}'
                })
            
            
            response = requests.post(
                f'{FLASK_API_URL}/process_xml',
                json={'xml_content': xml_content},
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                flask_data = response.json()
                return JsonResponse({
                    'success': True,
                    'django_validation': validation_message,
                    'flask_processing': flask_data,
                    'architecture_note': 'Validación en Django MVT + Procesamiento en Flask API'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Error en API Flask: {response.status_code}'
                })
                
        except requests.exceptions.ConnectionError:
            return JsonResponse({
                'success': False,
                'error': 'No se puede conectar con la API Flask. Asegúrate de que esté ejecutándose en puerto 5000.'
            })
        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'Timeout al conectar con Flask API.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Error inesperado: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def get_books_by_genre(request):
    
    if request.method == 'POST':
        try:
            xml_content = request.POST.get('xml_content', '')
            
            if not xml_content.strip():
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó contenido XML'
                })
            
            response = requests.post(
                f'{FLASK_API_URL}/books_by_genre',
                json={'xml_content': xml_content},
                timeout=30
            )
            
            if response.status_code == 200:
                return JsonResponse({
                    'success': True,
                    'data': response.json(),
                    'source': 'Flask API con ElementTree'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Error en la API Flask'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def get_price_analysis(request):
    
    if request.method == 'POST':
        try:
            xml_content = request.POST.get('xml_content', '')
            
            if not xml_content.strip():
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó contenido XML'
                })
            
            response = requests.post(
                f'{FLASK_API_URL}/price_analysis',
                json={'xml_content': xml_content},
                timeout=30
            )
            
            if response.status_code == 200:
                return JsonResponse({
                    'success': True,
                    'data': response.json(),
                    'source': 'Flask API con ElementTree'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Error en la API Flask'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def get_publication_timeline(request):
    
    if request.method == 'POST':
        try:
            xml_content = request.POST.get('xml_content', '')
            
            if not xml_content.strip():
                return JsonResponse({
                    'success': False,
                    'error': 'No se proporcionó contenido XML'
                })
            
            response = requests.post(
                f'{FLASK_API_URL}/publication_timeline',
                json={'xml_content': xml_content},
                timeout=30
            )
            
            if response.status_code == 200:
                return JsonResponse({
                    'success': True,
                    'data': response.json(),
                    'source': 'Flask API con ElementTree'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Error en la API Flask'
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def get_system_info(request):
    
    system_info = {
        'architecture': 'Django MVT + Flask API',
        'django_role': 'Frontend con patrón MVT',
        'flask_role': 'API backend con ElementTree',
        'data_persistence': 'Sin base de datos - procesamiento en memoria',
        'mvt_pattern': {
            'Model': 'Estructura de datos y validaciones (models.py)',
            'View': 'Lógica de negocio y comunicación con API (views.py)',
            'Template': 'Presentación HTML con JavaScript (templates/)'
        },
        'mvc_vs_mvt': {
            'MVC_Controller': 'Maneja entrada del usuario y coordina Model/View',
            'MVT_View': 'Funciona como Controller + maneja lógica de negocio',
            'MVT_Template': 'Reemplaza la Vista del MVC tradicional'
        }
    }
    
    return JsonResponse(system_info)
