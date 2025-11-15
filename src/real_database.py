"""
Real Database Integration - Using comprehensive_products.json
Loads and searches from actual comprehensive product database
"""

import json
import os
from typing import List, Dict, Any


class RealProductDatabase:
    """Actual product database using comprehensive_products.json"""
    
    def __init__(self):
        self.products = self._load_products()
        self.categories = self._build_category_index()
        self.brands = self._build_brand_index()
    
    def _load_products(self) -> List[Dict[str, Any]]:
        """Load products from comprehensive_products.json"""
        try:
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'comprehensive_products.json')
            with open(db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: comprehensive_products.json not found at {db_path}")
            return self._fallback_products()
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            return self._fallback_products()
    
    def _fallback_products(self) -> List[Dict[str, Any]]:
        """Fallback products if JSON fails to load"""
        return [
            {
                "name": "MacBook Air M3",
                "price": 114900,
                "rating": 4.8,
                "image_url": "https://via.placeholder.com/300x200/C0C0C0/ffffff?text=MacBook+Air+M3",
                "description": "M3 chip, 15-inch Liquid Retina display, 18-hour battery",
                "buy_link": "https://www.apple.com/in/macbook-air-m3/",
                "category": "electronics",
                "brand": "Apple",
                "color": "silver",
                "platform": "Apple"
            }
        ]
    
    def _build_category_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build category-based index for faster searches"""
        categories = {}
        for product in self.products:
            cat = product.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(product)
        return categories
    
    def _build_brand_index(self) -> Dict[str, List[Dict[str, Any]]]:
        """Build brand-based index for faster searches"""
        brands = {}
        for product in self.products:
            brand = product.get('brand', 'Unknown')
            if brand not in brands:
                brands[brand] = []
            brands[brand].append(product)
        return brands
    
    def search_products(self, 
                       category: str = None,
                       min_price: int = None,
                       max_price: int = None,
                       brand: str = None,
                       color: str = None,
                       platform: str = None) -> List[Dict[str, Any]]:
        """Search products with filters"""
        
        results = self.products
        
        # Apply filters
        if category:
            results = [p for p in results if p.get('category', '').lower() == category.lower()]
        
        if min_price is not None:
            results = [p for p in results if p.get('price', 0) >= min_price]
        
        if max_price is not None:
            results = [p for p in results if p.get('price', 0) <= max_price]
        
        if brand:
            results = [p for p in results if p.get('brand', '').lower() == brand.lower()]
        
        if color:
            results = [p for p in results if p.get('color', '').lower() == color.lower()]
        
        if platform:
            results = [p for p in results if p.get('platform', '').lower() == platform.lower()]
        
        # Sort by rating and price
        return sorted(results, key=lambda x: (-x.get('rating', 0), x.get('price', 0)))
    
    def search_by_keywords(self, keywords: List[str]) -> List[Dict[str, Any]]:
        """Search products by keywords"""
        results = []
        for product in self.products:
            search_text = f"{product.get('name', '')} {product.get('description', '')}".lower()
            if any(keyword.lower() in search_text for keyword in keywords):
                results.append(product)
        return results
    
    def get_categories(self) -> List[str]:
        """Get all available categories"""
        return list(set(p.get('category', 'general') for p in self.products))
    
    def get_brands(self) -> List[str]:
        """Get all available brands"""
        return list(set(p.get('brand', 'Unknown') for p in self.products))
    
    def get_price_range(self, category: str = None) -> Dict[str, int]:
        """Get price range for category"""
        products = self.categories.get(category, self.products)
        prices = [p.get('price', 0) for p in products]
        return {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0
        }
    
    def get_product_count(self) -> Dict[str, int]:
        """Get product counts by category"""
        counts = {}
        for product in self.products:
            cat = product.get('category', 'general')
            counts[cat] = counts.get(cat, 0) + 1
        return counts


# Global database instance
REAL_DB = RealProductDatabase()

# Test the database
if __name__ == "__main__":
    db = RealProductDatabase()
    
    print("=== Real Database Test ===")
    print(f"Total products: {len(db.products)}")
    print(f"Categories: {db.get_categories()}")
    print(f"Brands: {db.get_brands()}")
    print(f"Price ranges: {db.get_price_range()}")
    
    # Test searches
    print("\n=== Search Tests ===")
    
    # Search laptops under 100k
    laptops = db.search_products(category='electronics', max_price=100000)
    print(f"Laptops under 100k: {len(laptops)} products")
    
    # Search Apple products
    apple_products = db.search_products(brand='Apple')
    print(f"Apple products: {len(apple_products)} products")
    
    # Search by keywords
    keyword_results = db.search_by_keywords(['wireless', 'headphones'])
    print(f"Wireless headphones: {len(keyword_results)} products")
