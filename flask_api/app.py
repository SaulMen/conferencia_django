# flask_api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime
import statistics

app = Flask(__name__)
CORS(app)

class XMLProcessor:
    def __init__(self):
        self.books = []
        
    def parse_xml(self, xml_content):
        try:
            root = ET.fromstring(xml_content)
            self.books = []
            
            for book in root.findall('book'):
                book_data = {
                    'id': book.get('id'),
                    'author': self._get_text(book, 'author'),
                    'title': self._get_text(book, 'title'),
                    'genre': self._get_text(book, 'genre'),
                    'price': float(self._get_text(book, 'price', '0')),
                    'publish_date': self._get_text(book, 'publish_date'),
                    'description': self._get_text(book, 'description')
                }
                self.books.append(book_data)
            
            return True, f"Se procesaron {len(self.books)} libros exitosamente"
        except ET.ParseError as e:
            return False, f"Error al parsear XML: {str(e)}"
        except Exception as e:
            return False, f"Error inesperado: {str(e)}"
    
    def _get_text(self, element, tag, default=''):
        child = element.find(tag)
        return child.text if child is not None and child.text else default
    
    def get_basic_info(self):
        if not self.books:
            return {'error': 'No hay libros procesados'}
        
        genres = Counter(book['genre'] for book in self.books)
        authors = Counter(book['author'] for book in self.books)
        
        total_books = len(self.books)
        avg_price = statistics.mean(book['price'] for book in self.books if book['price'] > 0)
        
        return {
            'total_books': total_books,
            'unique_genres': len(genres),
            'unique_authors': len(authors),
            'average_price': round(avg_price, 2),
            'most_common_genre': genres.most_common(1)[0] if genres else None,
            'most_prolific_author': authors.most_common(1)[0] if authors else None,
            'books_sample': self.books[:3]  
        }
    
    def analyze_by_genre(self):
        if not self.books:
            return {'error': 'No hay libros procesados'}
        
        genres = Counter(book['genre'] for book in self.books)
        genre_details = defaultdict(list)
        
        for book in self.books:
            genre_details[book['genre']].append({
                'title': book['title'],
                'author': book['author'],
                'price': book['price']
            })
        
        return {
            'genres': dict(genres),
            'genre_details': dict(genre_details),
            'total_genres': len(genres)
        }
    
    def analyze_prices(self):
        if not self.books:
            return {'error': 'No hay libros procesados'}
        
        prices = [book['price'] for book in self.books if book['price'] > 0]
        
        if not prices:
            return {'error': 'No se encontraron precios válidos'}
        
        expensive_books = sorted(self.books, key=lambda x: x['price'], reverse=True)[:5]
        cheap_books = sorted(self.books, key=lambda x: x['price'])[:5]
        
        return {
            'price_stats': price_stats,
            'price_ranges': price_ranges,
            'most_expensive': expensive_books,
            'cheapest': cheap_books
        }
    
    def analyze_publication_timeline(self):
        if not self.books:
            return {'error': 'No hay libros procesados'}
        
        years = defaultdict(int)
        monthly_data = defaultdict(int)
        
        for book in self.books:
            try:
                date_str = book['publish_date']
                if date_str:
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                    year = date_obj.year
                    month_year = f"{date_obj.year}-{date_obj.month:02d}"
                    
                    years[str(year)] += 1
                    monthly_data[month_year] += 1
            except ValueError:
                continue
        
        peak_year = max(years.items(), key=lambda x: x[1]) if years else None
        
        return {
            'timeline': dict(years),
            'monthly_timeline': dict(monthly_data),
            'peak_year': peak_year,
            'total_years': len(years)
        }
    
    def get_author_analysis(self):
        if not self.books:
            return {'error': 'No hay libros procesados'}
        
        author_data = defaultdict(lambda: {
            'books': [],
            'total_books': 0,
            'genres': set(),
            'total_price': 0
        })
        
        for book in self.books:
            author = book['author']
            author_data[author]['books'].append({
                'title': book['title'],
                'genre': book['genre'],
                'price': book['price']
            })
            author_data[author]['total_books'] += 1
            author_data[author]['genres'].add(book['genre'])
            author_data[author]['total_price'] += book['price']
        
        # Convertir sets a listas para JSON
        for author in author_data:
            author_data[author]['genres'] = list(author_data[author]['genres'])
            author_data[author]['avg_price'] = round(
                author_data[author]['total_price'] / author_data[author]['total_books'], 2
            ) if author_data[author]['total_books'] > 0 else 0
        
        return dict(author_data)

processor = XMLProcessor()

@app.route('/process_xml', methods=['POST'])
def process_xml():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        
        if not xml_content.strip():
            return jsonify({'error': 'No se proporcionó contenido XML'}), 400
        
        success, message = processor.parse_xml(xml_content)
        
        if success:
            basic_info = processor.get_basic_info()
            return jsonify({
                'success': True,
                'message': message,
                'basic_info': basic_info
            })
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/books_by_genre', methods=['POST'])
def books_by_genre():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        
        if xml_content:
            processor.parse_xml(xml_content)
        
        result = processor.analyze_by_genre()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/price_analysis', methods=['POST'])
def price_analysis():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        
        if xml_content:
            processor.parse_xml(xml_content)
        
        result = processor.analyze_prices()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/publication_timeline', methods=['POST'])
def publication_timeline():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        
        if xml_content:
            processor.parse_xml(xml_content)
        
        result = processor.analyze_publication_timeline()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/author_analysis', methods=['POST'])
def author_analysis():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        
        if xml_content:
            processor.parse_xml(xml_content)
        
        result = processor.get_author_analysis()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/search_books', methods=['POST'])
def search_books():
    try:
        data = request.get_json()
        xml_content = data.get('xml_content', '')
        search_term = data.get('search_term', '').lower()
        search_field = data.get('search_field', 'title')
        
        if xml_content:
            processor.parse_xml(xml_content)
        
        if not processor.books:
            return jsonify({'error': 'No hay libros procesados'})
        
        filtered_books = []
        for book in processor.books:
            field_value = book.get(search_field, '').lower()
            if search_term in field_value:
                filtered_books.append(book)
        
        return jsonify({
            'results': filtered_books,
            'total_found': len(filtered_books),
            'search_term': search_term,
            'search_field': search_field
        })
        
    except Exception as e:
        return jsonify({'error': f'Error del servidor: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'OK',
        'message': 'Flask API está funcionando correctamente',
        'books_loaded': len(processor.books)
    })

@app.route('/', methods=['GET'])
def index():
    
    return jsonify({
        'name': 'XML Book Catalog API',
        'version': '1.0',
        'description': 'API para procesar y analizar catálogos de libros en formato XML',
        'endpoints': [
            '/process_xml',
            '/books_by_genre',
            '/price_analysis',
            '/publication_timeline',
            '/author_analysis',
            '/search_books',
            '/health'
        ]
    })

if __name__ == '__main__':
    print("Iniciando Flask API...")
    print("API de procesamiento XML para catálogo de libros")
    print("Disponible en: http://localhost:5000")
    print("Endpoints disponibles:")
    print("   - POST /process_xml")
    print("   - POST /books_by_genre")
    print("   - POST /price_analysis")
    print("   - POST /publication_timeline")
    print("   - POST /author_analysis")
    print("   - POST /search_books")
    print("   - GET /health")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
    price_stats = {
        'min': min(prices),
        'max': max(prices),
        'average': round(statistics.mean(prices), 2),
        'median': round(statistics.median(prices), 2)
    }
        
    # Rangos de precios
    price_ranges = {
        '$0-10': len([p for p in prices if 0 <= p <= 10]),
        '$10-20': len([p for p in prices if 10 < p <= 20]),
        '$20-30': len([p for p in prices if 20 < p <= 30]),
        '$30-40': len([p for p in prices if 30 < p <= 40]),
        '$40+': len([p for p in prices if p > 40])
    }