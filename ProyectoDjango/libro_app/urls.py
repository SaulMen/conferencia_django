# ProyectoDjango/ProyectoDjango/urls.py
from django.urls import path
from . import views

app_name = 'libro_app'

urlpatterns = [
    # home
    path('', views.index, name='index'),
    
    # endpoints para procesamiento xml 
    path('validate_xml/', views.validate_xml_structure, name='validate_xml'),
    path('upload_xml/', views.upload_xml, name='upload_xml'),
    
    # endpoints para analisis
    path('books_by_genre/', views.get_books_by_genre, name='books_by_genre'),
    path('price_analysis/', views.get_price_analysis, name='price_analysis'),
    path('publication_timeline/', views.get_publication_timeline, name='publication_timeline'),
    
    path('system_info/', views.get_system_info, name='system_info'),
]