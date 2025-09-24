# ProyectoDjango/libro_app/models.py
from django.db import models
import xml.etree.ElementTree as ET

class Book(models.Model):
    
    xml_id = models.CharField(max_length=20, help_text="ID del libro en el XML")
    title = models.CharField(max_length=200, help_text="Título del libro")
    author = models.CharField(max_length=100, help_text="Autor del libro")
    genre = models.CharField(max_length=50, help_text="Género del libro")
    price = models.DecimalField(max_digits=6, decimal_places=2, help_text="Precio del libro")
    publish_date = models.DateField(help_text="Fecha de publicación")
    description = models.TextField(help_text="Descripción del libro")
    
    class Meta:
        managed = False
        
    def __str__(self):
        return f"{self.title} - {self.author}"
    
    @classmethod
    def get_xml_structure_info(cls):
        
        return {
            'xml_root': 'catalog',
            'xml_element': 'book',
            'required_fields': ['id', 'title', 'author', 'genre', 'price', 'publish_date', 'description']
        }


class XMLProcessor:
    
    
    @staticmethod
    def validate_xml_structure(xml_content):
        
        try:
            root = ET.fromstring(xml_content)
            
            if root.tag != 'catalog':
                return False, "El elemento raíz debe ser 'catalog'"
            
            books = root.findall('book')
            if len(books) == 0:
                return False, "No se encontraron elementos 'book' en el XML"
            
            return True, f"XML válido con {len(books)} libros"
            
        except ET.ParseError as e:
            return False, f"Error de formato XML: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    @staticmethod
    def get_basic_stats_preview(xml_content):
        
        try:
            root = ET.fromstring(xml_content)
            books = root.findall('book')
            
            genres = set()
            authors = set()
            
            for book in books:
                genre_elem = book.find('genre')
                author_elem = book.find('author')
                
                if genre_elem is not None and genre_elem.text:
                    genres.add(genre_elem.text)
                if author_elem is not None and author_elem.text:
                    authors.add(author_elem.text)
            
            return {
                'total_books': len(books),
                'unique_genres': len(genres),
                'unique_authors': len(authors),
                'preview_complete': True
            }
            
        except Exception:
            return {
                'total_books': 0,
                'unique_genres': 0,
                'unique_authors': 0,
                'preview_complete': False
            }