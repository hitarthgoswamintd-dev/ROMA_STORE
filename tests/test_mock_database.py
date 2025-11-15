"""
Unit tests for MockProductDatabase
"""

import pytest
from src.mock_database import MockProductDatabase


class TestMockDatabase:
    """Test suite for mock product database"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.db = MockProductDatabase()
    
    # Search tests
    def test_search_by_category(self):
        """Test searching products by category"""
        results = self.db.search_products(category='apparel')
        assert all(p['category'] == 'apparel' for p in results)
    
    def test_search_by_max_price(self):
        """Test searching products by max price"""
        results = self.db.search_products(max_price=3000)
        assert all(p['price'] <= 3000 for p in results)
    
    def test_search_by_query(self):
        """Test searching products by query keywords"""
        results = self.db.search_products(query='red shoes')
        assert len(results) > 0
    
    def test_search_by_brand(self):
        """Test searching products by brand"""
        results = self.db.search_products(brand='Nike')
        assert all('nike' in p['brand'].lower() for p in results)
    
    def test_search_by_color(self):
        """Test searching products by color"""
        results = self.db.search_products(color='red')
        assert all('red' in p['color'].lower() for p in results)
    
    def test_search_combined_filters(self):
        """Test searching with multiple filters"""
        results = self.db.search_products(
            category='apparel',
            max_price=3000,
            color='red'
        )
        assert all(p['category'] == 'apparel' and p['price'] <= 3000 for p in results)
    
    def test_search_no_results(self):
        """Test search returning no results"""
        results = self.db.search_products(max_price=100)
        assert len(results) == 0
    
    # Metadata tests
    def test_get_categories(self):
        """Test getting all categories"""
        categories = self.db.get_categories()
        assert 'apparel' in categories
        assert 'mobiles' in categories
        assert 'electronics' in categories
    
    def test_get_brands(self):
        """Test getting all brands"""
        brands = self.db.get_brands()
        assert len(brands) > 0
        assert isinstance(brands, list)
    
    def test_get_colors(self):
        """Test getting all colors"""
        colors = self.db.get_colors()
        assert len(colors) > 0
        assert isinstance(colors, list)
    
    def test_get_platforms(self):
        """Test getting all platforms"""
        platforms = self.db.get_platforms()
        assert len(platforms) > 0
        assert 'Amazon' in platforms or 'Flipkart' in platforms
    
    # Price range tests
    def test_get_price_range_all(self):
        """Test getting price range for all products"""
        price_range = self.db.get_price_range()
        assert isinstance(price_range, dict)
        assert 'min' in price_range
        assert 'max' in price_range
        assert price_range['min'] <= price_range['max']
    
    def test_get_price_range_by_category(self):
        """Test getting price range for specific category"""
        price_range = self.db.get_price_range(category='apparel')
        assert isinstance(price_range, dict)
        assert price_range['min'] >= 0
        assert price_range['max'] > 0
    
    def test_get_price_range_empty_category(self):
        """Test getting price range for non-existent category"""
        price_range = self.db.get_price_range(category='nonexistent')
        assert price_range['min'] == 0
        assert price_range['max'] == 0
    
    # Product retrieval tests
    def test_get_product_by_id(self):
        """Test getting product by ID"""
        product = self.db.get_product_by_id(0)
        assert product is not None
        assert 'name' in product
        assert 'price' in product
    
    def test_get_product_by_invalid_id(self):
        """Test getting product with invalid ID"""
        product = self.db.get_product_by_id(9999)
        assert product is None
    
    # Top rated tests
    def test_get_top_rated(self):
        """Test getting top rated products"""
        results = self.db.get_top_rated(limit=3)
        assert len(results) <= 3
        # Check if sorted by rating (descending)
        if len(results) > 1:
            assert results[0]['rating'] >= results[-1]['rating']
    
    def test_get_top_rated_by_category(self):
        """Test getting top rated products by category"""
        results = self.db.get_top_rated(category='apparel', limit=2)
        assert all(p['category'] == 'apparel' for p in results)
        assert len(results) <= 2
    
    # Brand exclusion tests
    def test_brand_exclusion_non_apple(self):
        """Test excluding Apple brand"""
        results = self.db.search_products(query='non-apple laptop')
        assert all('apple' not in p['brand'].lower() for p in results)
    
    # Add product test
    def test_add_product(self):
        """Test adding a new product"""
        initial_count = len(self.db.products)
        new_product = {
            'name': 'Test Product',
            'price': 5000,
            'rating': 4.5,
            'category': 'apparel',
            'brand': 'TestBrand',
            'color': 'blue',
            'platform': 'Amazon',
            'description': 'Test description',
            'buy_link': 'https://test.com'
        }
        self.db.add_product(new_product)
        assert len(self.db.products) == initial_count + 1
    
    # Edge cases
    def test_search_case_insensitivity(self):
        """Test that search is case insensitive"""
        results1 = self.db.search_products(query='RED')
        results2 = self.db.search_products(query='red')
        assert len(results1) == len(results2)
    
    def test_empty_database_operations(self):
        """Test operations on empty result set"""
        results = self.db.search_products(max_price=1)
        assert isinstance(results, list)
        assert len(results) == 0
