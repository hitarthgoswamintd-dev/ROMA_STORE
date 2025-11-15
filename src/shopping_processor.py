from typing import List, Dict, Any
from .budget_analyzer import BudgetAnalyzer
from .mock_database import MockProductDatabase
from .config import SCORING_WEIGHTS, COLOR_KEYWORDS
from .logger import setup_logger

logger = setup_logger(__name__)


class ShoppingQueryProcessor:
    """Main processor for shopping queries using budget analysis and mock database"""
    
    def __init__(self):
        self.budget_analyzer = BudgetAnalyzer()
        self.database = MockProductDatabase()
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process a shopping query and return curated results"""
        
        try:
            logger.info(f"Processing query: {user_query}")
            
            analysis = self.budget_analyzer.analyze_budget(user_query)
            logger.debug(f"Analysis result: {analysis}")
            
            search_results = self.database.search_products(
                query=user_query,
                category=analysis['category'],
                max_price=analysis['max_budget']
            )
            logger.debug(f"Found {len(search_results)} products")
            
            filtered_results = self._filter_and_rank(
                search_results, 
                user_query, 
                analysis
            )
            response = {
                'success': True,
                'query': user_query,
                'analysis': analysis,
                'products': filtered_results[:3],  # Top 3 results
                'total_found': len(search_results),
                'category': analysis['category'],
                'max_budget': analysis['max_budget']
            }
            
            logger.info(f"Query processed successfully: {len(response['products'])} results returned")
            return response
            
        except Exception as e:
            logger.error(f"Query processing failed: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e),
                'query': user_query,
                'products': []
            }
    
    def _filter_and_rank(self, products: List[Dict], query: str, analysis: Dict) -> List[Dict]:
        """Advanced filtering and ranking of products"""
        
        if not products:
            return []
        
        query_lower = query.lower()
        scored_products = []
        
        for product in products:
            score = 0
            product_text = f"{product['name']} {product['description']} {product['brand']} {product['color']}".lower()
            
            keywords = query_lower.split()
            for keyword in keywords:
                if keyword in product_text:
                    score += 2
            
            for color in COLOR_KEYWORDS:
                if color in query_lower and color in product['color'].lower():
                    score += 3
            
            brand_lower = product['brand'].lower()
            if brand_lower in query_lower:
                score += 2
            
            if analysis['max_budget']:
                price_ratio = product['price'] / analysis['max_budget']
                if price_ratio <= 1.0:
                    score += (1.0 - price_ratio) * 2
                else:
                    score -= 5
            
            score += product['rating'] * 1.5
            
            if analysis['category'] and product['category'] == analysis['category']:
                score += 1
            
            scored_products.append((score, product))
        scored_products.sort(key=lambda x: x[0], reverse=True)
        
        return [product for score, product in scored_products]
    
    def get_suggestions(self, query: str) -> Dict[str, Any]:
        """Get search suggestions and category recommendations"""
        
        analysis = self.budget_analyzer.analyze_budget(query)
        
        suggestions = {
            'categories': [],
            'price_range': None,
            'popular_brands': [],
            'sample_products': []
        }
        
        if not analysis['category']:
            suggestions['categories'] = self.budget_analyzer.get_category_suggestions(query)
        
        if analysis['category']:
            price_range = self.database.get_price_range(analysis['category'])
            suggestions['price_range'] = {
                **price_range,
                'currency': 'INR'
            }
            
            products = self.database.search_products(category=analysis['category'])
            brands = list(set(p['brand'] for p in products))
            suggestions['popular_brands'] = brands[:5]
            suggestions['sample_products'] = products[:3]
        
        return suggestions
    
    def get_categories(self) -> List[str]:
        """Get available product categories"""
        return self.database.get_categories()
    
    def get_brands(self) -> List[str]:
        """Get available brands"""
        return self.database.get_brands()


if __name__ == "__main__":
    processor = ShoppingQueryProcessor()
    
    test_queries = [
        "red running shoes under budget",
        "non-Apple laptops under 50000",
        "cheap mobile phones",
        "blue denim jacket",
        "wireless headphones under 3000"
    ]
    
    print("=== Shopping Query Processor Tests ===")
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        result = processor.process_query(query)
        
        if result['success']:
            print(f"✅ Found {result['total_found']} products")
            print(f"📊 Category: {result['category']}")
            print(f"💰 Max Budget: ₹{result['max_budget']:,}")
            for i, product in enumerate(result['products'], 1):
                print(f"  {i}. {product['name']} - ₹{product['price']:,} ({product['rating']}⭐)")
        else:
            print(f"❌ Error: {result['error']}")
        
        print("-" * 50)
