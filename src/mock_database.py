import json
from typing import List, Dict, Any
import os


class MockProductDatabase:
    """Mock product database for testing shopping queries"""
    
    def __init__(self, data_file: str = None):
        if data_file is None:
            data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'mock_products.json')
        
        self.products = self._load_mock_data(data_file)
    
    def _load_mock_data(self, data_file: str) -> List[Dict[str, Any]]:
        """Load mock product data from JSON file"""
        try:
            with open(data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return [
                {
                    "name": "Red Nike Air Max",
                    "price": 2499,
                    "rating": 4.5,
                    "image_url": "https://via.placeholder.com/300x200/ff0000/ffffff?text=Nike+Red",
                    "description": "Comfortable running shoes with Air Max cushioning",
                    "buy_link": "https://amazon.in/nike-red",
                    "category": "apparel",
                    "brand": "Nike",
                    "color": "red",
                    "platform": "Amazon"
                }
            ]
    
    def search_products(self, query: str = None, category: str = None, 
                       max_price: int = None, brand: str = None, 
                       color: str = None, platform: str = None) -> List[Dict[str, Any]]:
        """Search products based on various criteria"""
        
        filtered_products = self.products
        
        if category:
            filtered_products = [p for p in filtered_products if p['category'] == category]
        
        if max_price:
            filtered_products = [p for p in filtered_products if p['price'] <= max_price]
        
        if brand:
            filtered_products = [p for p in filtered_products if brand.lower() in p['brand'].lower()]
        
        if color:
            filtered_products = [p for p in filtered_products if color.lower() in p['color'].lower()]
        
        if platform:
            filtered_products = [p for p in filtered_products if p['platform'].lower() == platform.lower()]
        
        if query:
            query_words = query.lower().split()
            filtered_products = [
                p for p in filtered_products 
                if any(word in p['name'].lower() or 
                      word in p['description'].lower() or
                      word in p['category'].lower() or
                      word in p['brand'].lower() or
                      word in p['color'].lower()
                      for word in query_words)
            ]
        
        if query and 'non-apple' in query.lower():
            filtered_products = [p for p in filtered_products if 'apple' not in p['brand'].lower()]
        
        filtered_products.sort(key=lambda x: (-x['rating'], x['price']))
        
        return filtered_products
    
    def get_product_by_id(self, product_id: int) -> Dict[str, Any]:
        """Get a specific product by ID (index)"""
        if 0 <= product_id < len(self.products):
            return self.products[product_id]
        return None
    
    def get_categories(self) -> List[str]:
        """Get unique categories"""
        return list(set(p['category'] for p in self.products))
    
    def get_brands(self) -> List[str]:
        """Get unique brands"""
        return list(set(p['brand'] for p in self.products))
    
    def get_colors(self) -> List[str]:
        """Get unique colors"""
        return list(set(p['color'] for p in self.products))
    
    def get_platforms(self) -> List[str]:
        """Get unique platforms"""
        return list(set(p['platform'] for p in self.products))
    
    def get_price_range(self, category: str = None) -> Dict[str, int]:
        """Get min and max prices for filtering"""
        products = self.products
        if category:
            products = [p for p in products if p['category'] == category]
        
        if not products:
            return {'min': 0, 'max': 0}
        
        prices = [p['price'] for p in products]
        return {'min': min(prices), 'max': max(prices)}
    
    def add_product(self, product: Dict[str, Any]):
        """Add a new product to mock database"""
        self.products.append(product)
    
    def get_top_rated(self, category: str = None, limit: int = 3) -> List[Dict[str, Any]]:
        """Get top rated products"""
        products = self.products
        if category:
            products = [p for p in products if p['category'] == category]
        
        return sorted(products, key=lambda x: x['rating'], reverse=True)[:limit]


if __name__ == "__main__":
    db = MockProductDatabase()
    
    print("=== Testing Mock Database ===")
    print(f"Total products: {len(db.products)}")
    print(f"Categories: {db.get_categories()}")
    print(f"Brands: {db.get_brands()}")
    
    print("\n=== Search Tests ===")
    
    # Test basic search
    results = db.search_products(query="red shoes")
    print(f"Search 'red shoes': {len(results)} results")
    
    # Test category search
    results = db.search_products(category="mobiles", max_price=15000)
    print(f"Mobiles under ₹15,000: {len(results)} results")
    
    # Test brand exclusion
    results = db.search_products(query="non-apple laptops")
    print(f"Non-Apple laptops: {len(results)} results")
    
    # Test top rated
    results = db.get_top_rated(category="electronics", limit=3)
    print(f"Top 3 electronics: {[r['name'] for r in results]}")
