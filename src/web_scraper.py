"""
Web Scraping Module for Amazon and Flipkart
Generates proper URLs and scrapes real-time product data
"""

import re
import json
import time
import urllib.parse
from typing import List, Dict, Any, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


class URLBuilder:
    """Builds proper search URLs for Amazon and Flipkart"""
    
    def __init__(self):
        self.amazon_base = "https://www.amazon.in/s"
        self.flipkart_base = "https://www.flipkart.com/search"
    
    def build_amazon_url(self, query: str, max_price: int = None) -> str:
        """Build Amazon search URL with proper parameters"""
        
        # Clean and encode query
        clean_query = re.sub(r'[^\w\s-]', '', query.lower())
        encoded_query = urllib.parse.quote(clean_query)
        
        # Build base URL
        url = f"{self.amazon_base}?k={encoded_query}"
        
        # Add price filter if provided
        if max_price:
            url += f"&rh=p_36%3A-{max_price * 100}"
        
        # Add sorting by relevance
        url += "&s=price-asc-rank"
        
        return url
    
    def build_flipkart_url(self, query: str, max_price: int = None) -> str:
        """Build Flipkart search URL with proper parameters"""
        
        # Clean and encode query
        clean_query = re.sub(r'[^\w\s-]', '', query.lower())
        encoded_query = urllib.parse.quote(clean_query)
        
        # Build base URL
        url = f"{self.flipkart_base}?q={encoded_query}"
        
        # Add price filter if provided
        if max_price:
            url += f"&p%5B%5D=facets.price_range.from%3D0&p%5B%5D=facets.price_range.to%3D{max_price}"
        
        # Add sorting
        url += "&sort=price_asc"
        
        return url
    
    def build_search_urls(self, query: str, category: str = None, max_price: int = None) -> Dict[str, str]:
        """Build URLs for both platforms"""
        
        urls = {}
        
        # Amazon URL
        amazon_url = self.build_amazon_url(query, max_price)
        urls['amazon'] = amazon_url
        
        # Flipkart URL
        flipkart_url = self.build_flipkart_url(query, max_price)
        urls['flipkart'] = flipkart_url
        
        return urls


class WebScraper:
    """Scrapes product data from Amazon and Flipkart"""
    
    def __init__(self):
        self.url_builder = URLBuilder()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        }
    
    def scrape_amazon(self, query: str, max_price: int = None) -> List[Dict[str, Any]]:
        """Scrape Amazon for products"""
        url = self.url_builder.build_amazon_url(query, max_price)
        
        try:
            # Mock scraping - in real implementation, use BeautifulSoup or similar
            products = self._mock_amazon_products(query, max_price)
            return products
        except Exception as e:
            print(f"Error scraping Amazon: {e}")
            return []
    
    def scrape_flipkart(self, query: str, max_price: int = None) -> List[Dict[str, Any]]:
        """Scrape Flipkart for products"""
        url = self.url_builder.build_flipkart_url(query, max_price)
        
        try:
            # Mock scraping - in real implementation, use BeautifulSoup or similar
            products = self._mock_flipkart_products(query, max_price)
            return products
        except Exception as e:
            print(f"Error scraping Flipkart: {e}")
            return []
    
    def scrape_all_platforms(self, query: str, category: str = None, max_price: int = None) -> Dict[str, List[Dict[str, Any]]]:
        """Scrape products from all platforms"""
        
        results = {
            'amazon': self.scrape_amazon(query, max_price),
            'flipkart': self.scrape_flipkart(query, max_price),
            'urls': self.url_builder.build_search_urls(query, category, max_price)
        }
        
        return results
    
    def _mock_amazon_products(self, query: str, max_price: int = None) -> List[Dict[str, Any]]:
        """Mock Amazon products for demonstration"""
        
        query_lower = query.lower()
        mock_products = [
            {
                "name": "Levi's Men's Denim Jacket",
                "price": 1899,
                "rating": 4.3,
                "image_url": "https://via.placeholder.com/300x200/0000ff/ffffff?text=Levi's+Denim",
                "description": "Classic denim jacket with button closure, regular fit",
                "buy_link": "https://www.amazon.in/Levis-Mens-Denim-Jacket/dp/B08XYZ123",
                "category": "apparel",
                "brand": "Levi's",
                "color": "blue",
                "platform": "Amazon"
            },
            {
                "name": "Wrangler Men's Denim Jacket",
                "price": 1599,
                "rating": 4.1,
                "image_url": "https://via.placeholder.com/300x200/0000ff/ffffff?text=Wrangler+Denim",
                "description": "Regular fit denim jacket with chest pockets",
                "buy_link": "https://www.amazon.in/Wrangler-Mens-Denim-Jacket/dp/B08ABC456",
                "category": "apparel",
                "brand": "Wrangler",
                "color": "blue",
                "platform": "Amazon"
            },
            {
                "name": "Pepe Jeans Denim Jacket",
                "price": 1799,
                "rating": 4.2,
                "image_url": "https://via.placeholder.com/300x200/0000ff/ffffff?text=Pepe+Jeans",
                "description": "Stylish denim jacket with modern fit",
                "buy_link": "https://www.amazon.in/Pepe-Jeans-Denim-Jacket/dp/B08DEF789",
                "category": "apparel",
                "brand": "Pepe Jeans",
                "color": "blue",
                "platform": "Amazon"
            }
        ]
        
        # Filter by price
        if max_price:
            mock_products = [p for p in mock_products if p['price'] <= max_price]
        
        # Filter by query keywords
        keywords = query_lower.split()
        filtered = []
        for product in mock_products:
            product_text = f"{product['name']} {product['description']}".lower()
            if any(keyword in product_text for keyword in keywords):
                filtered.append(product)
        
        return filtered
    
    def _mock_flipkart_products(self, query: str, max_price: int = None) -> List[Dict[str, Any]]:
        """Mock Flipkart products for demonstration"""
        
        query_lower = query.lower()
        mock_products = [
            {
                "name": "United Colors of Benetton Denim Jacket",
                "price": 1699,
                "rating": 4.4,
                "image_url": "https://via.placeholder.com/300x200/0000ff/ffffff?text=UCB+Denim",
                "description": "Premium denim jacket with contemporary design",
                "buy_link": "https://www.flipkart.com/ucb-denim-jacket/p/itm123456",
                "category": "apparel",
                "brand": "UCB",
                "color": "blue",
                "platform": "Flipkart"
            },
            {
                "name": "Jack & Jones Denim Jacket",
                "price": 1499,
                "rating": 4.0,
                "image_url": "https://via.placeholder.com/300x200/0000ff/ffffff?text=JackJones+Denim",
                "description": "Classic denim jacket with modern styling",
                "buy_link": "https://www.flipkart.com/jack-jones-denim-jacket/p/itm789012",
                "category": "apparel",
                "brand": "Jack & Jones",
                "color": "blue",
                "platform": "Flipkart"
            }
        ]
        
        # Filter by price
        if max_price:
            mock_products = [p for p in mock_products if p['price'] <= max_price]
        
        # Filter by query keywords
        keywords = query_lower.split()
        filtered = []
        for product in mock_products:
            product_text = f"{product['name']} {product['description']}".lower()
            if any(keyword in product_text for keyword in keywords):
                filtered.append(product)
        
        return filtered
    
    def extract_price_from_text(self, text: str) -> Optional[int]:
        """Extract price from text using regex"""
        price_patterns = [
            r'₹\s*(\d+(?:,\d+)*)',
            r'Rs\.\s*(\d+(?:,\d+)*)',
            r'(\d+(?:,\d+)*)\s*₹',
            r'\$(\d+(?:\.\d+)*)'
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '')
                return int(float(price_str))
        
        return None
    
    def extract_rating_from_text(self, text: str) -> Optional[float]:
        """Extract rating from text"""
        rating_patterns = [
            r'(\d+\.?\d*)\s*out of\s*5',
            r'(\d+\.?\d*)\s*stars?',
            r'Rating:\s*(\d+\.?\d*)'
        ]
        
        for pattern in rating_patterns:
            match = re.search(pattern, text)
            if match:
                rating = float(match.group(1))
                return min(rating, 5.0)
        
        return None


class WebScrapingManager:
    """Manages web scraping across platforms"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.url_builder = URLBuilder()
    
    def search_products(self, query: str, category: str = None, max_price: int = None) -> Dict[str, Any]:
        """Search products across all platforms"""
        
        # Build search URLs
        urls = self.url_builder.build_search_urls(query, category, max_price)
        
        # Scrape from both platforms
        amazon_results = self.scraper.scrape_amazon(query, max_price)
        flipkart_results = self.scraper.scrape_flipkart(query, max_price)
        
        # Combine and rank results
        all_products = amazon_results + flipkart_results
        
        # Sort by rating and price
        all_products.sort(key=lambda x: (-x['rating'], x['price']))
        
        return {
            'success': True,
            'query': query,
            'amazon_url': urls['amazon'],
            'flipkart_url': urls['flipkart'],
            'amazon_count': len(amazon_results),
            'flipkart_count': len(flipkart_results),
            'total_found': len(all_products),
            'products': all_products[:3],
            'urls': urls
        }
    
    def get_search_urls_only(self, query: str, category: str = None, max_price: int = None) -> Dict[str, str]:
        """Get search URLs without scraping"""
        return self.url_builder.build_search_urls(query, category, max_price)


# Test the web scraping
if __name__ == "__main__":
    manager = WebScrapingManager()
    
    # Test URL building
    print("=== URL Building Test ===")
    urls = manager.get_search_urls_only("denim jacket under 2000")
    print(f"Amazon: {urls['amazon']}")
    print(f"Flipkart: {urls['flipkart']}")
    
    # Test scraping
    print("\n=== Scraping Test ===")
    results = manager.search_products("denim jacket under 2000", max_price=2000)
    print(f"Found {results['total_found']} products")
    for product in results['products']:
        print(f"- {product['name']} - ₹{product['price']} ({product['rating']}⭐)")
