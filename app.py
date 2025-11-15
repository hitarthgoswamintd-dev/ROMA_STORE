from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

from src.shopping_processor import ShoppingQueryProcessor
from src.logger import setup_logger
from src.config import INPUT_CONSTRAINTS

load_dotenv()

app = Flask(__name__)
logger = setup_logger(__name__)

# Enable CORS for Netlify frontend
CORS(app, resources={
    r"/search": {"origins": ["*"]},
    r"/suggestions": {"origins": ["*"]},
    r"/categories": {"origins": ["*"]},
    r"/brands": {"origins": ["*"]},
    r"/health": {"origins": ["*"]},
})

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[
        f"{INPUT_CONSTRAINTS['rate_limit_per_day']} per day",
        f"{INPUT_CONSTRAINTS['rate_limit_per_hour']} per hour"
    ]
)

processor = ShoppingQueryProcessor()

logger.info("ROMA Shopping Agent initialized")

@app.route('/')
def index():
    """Serve the main search interface"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
@limiter.limit(f"{INPUT_CONSTRAINTS['rate_limit_per_minute']} per minute")
def search():
    """Handle search queries"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            logger.warning("Empty search query received")
            return jsonify({
                'success': False,
                'error': 'Query cannot be empty'
            }), 400
        
        if len(query) < INPUT_CONSTRAINTS['min_query_length']:
            logger.warning(f"Query too short: {len(query)} chars")
            return jsonify({
                'success': False,
                'error': f"Query too short (minimum {INPUT_CONSTRAINTS['min_query_length']} characters)"
            }), 400
        
        if len(query) > INPUT_CONSTRAINTS['max_query_length']:
            logger.warning(f"Query too long: {len(query)} chars")
            return jsonify({
                'success': False,
                'error': f"Query too long (maximum {INPUT_CONSTRAINTS['max_query_length']} characters)"
            }), 400
        
        if not any(c.isalnum() for c in query):
            logger.warning("Query contains only special characters")
            return jsonify({
                'success': False,
                'error': 'Query must contain alphanumeric characters'
            }), 400
        
        logger.info(f"Valid search query: {query}")
        result = processor.process_query(query)
        
        logger.info(f"Search completed: {len(result.get('products', []))} results")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Search failed: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/suggestions', methods=['GET'])
def suggestions():
    """Get search suggestions"""
    try:
        query = request.args.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter required'
            }), 400
        
        suggestions = processor.get_suggestions(query)
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/categories', methods=['GET'])
def get_categories():
    """Get available categories"""
    try:
        categories = processor.get_categories()
        return jsonify({
            'success': True,
            'categories': categories
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/brands', methods=['GET'])
def get_brands():
    """Get available brands"""
    try:
        brands = processor.get_brands()
        return jsonify({
            'success': True,
            'brands': brands
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'ROMA Shopping Agent is running!',
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.path}")
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Error: {str(error)}", exc_info=True)
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

@app.errorhandler(429)
def rate_limit_handler(e):
    logger.warning(f"Rate limit exceeded: {request.remote_addr}")
    return jsonify({
        'success': False,
        'error': 'Rate limit exceeded. Max 10 requests per minute.'
    }), 429

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("[ROMA] Shopping Agent Starting...")
    print(f"[SERVER] Running on http://localhost:{port}")
    print("[INFO] Available endpoints:")
    print("   GET  /          - Main interface")
    print("   POST /search    - Search products")
    print("   GET  /suggestions - Get search suggestions")
    print("   GET  /categories - Get product categories")
    print("   GET  /brands    - Get available brands")
    print("   GET  /health    - Health check")
    
    app.run(debug=debug, port=port, host='0.0.0.0')
