"""
Unit tests for ShoppingQueryProcessor
"""

import pytest
from src.shopping_processor import ShoppingQueryProcessor


class TestShoppingProcessor:
    """Test suite for shopping query processor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.processor = ShoppingQueryProcessor()
    
    # Query processing tests
    def test_process_query_success(self):
        """Test successful query processing"""
        result = self.processor.process_query("red shoes under 3000")
        assert result['success'] is True
        assert 'products' in result
        assert 'analysis' in result
        assert 'total_found' in result
    
    def test_process_query_returns_top_3(self):
        """Test that processor returns top 3 results"""
        result = self.processor.process_query("shoes")
        assert len(result['products']) <= 3
    
    def test_process_query_with_budget(self):
        """Test query processing with budget constraint"""
        result = self.processor.process_query("laptop under 50000")
        assert result['success'] is True
        assert result['max_budget'] == 50000
        # All returned products should be under budget
        for product in result['products']:
            assert product['price'] <= 50000
    
    def test_process_query_with_category(self):
        """Test query processing with category detection"""
        result = self.processor.process_query("running shoes")
        assert result['success'] is True
        assert result['category'] == 'apparel'
    
    def test_process_query_with_color(self):
        """Test query processing with color preference"""
        result = self.processor.process_query("red shoes")
        assert result['success'] is True
        # At least one result should have red color if available
        if result['products']:
            colors = [p['color'].lower() for p in result['products']]
            assert any('red' in color for color in colors)
    
    def test_process_query_with_brand_exclusion(self):
        """Test query processing with brand exclusion"""
        result = self.processor.process_query("non-Apple laptop")
        assert result['success'] is True
        # All results should not contain Apple
        for product in result['products']:
            assert 'apple' not in product['brand'].lower()
    
    def test_process_query_empty(self):
        """Test processing empty query"""
        result = self.processor.process_query("")
        # Should handle gracefully
        assert 'success' in result
    
    def test_process_query_special_characters(self):
        """Test processing query with special characters"""
        result = self.processor.process_query("@#$%^&*()")
        # Should handle gracefully
        assert 'success' in result
    
    # Suggestions tests
    def test_get_suggestions_with_category(self):
        """Test getting suggestions for query with category"""
        suggestions = self.processor.get_suggestions("laptop")
        assert 'price_range' in suggestions
        assert suggestions['price_range'] is not None
    
    def test_get_suggestions_without_category(self):
        """Test getting suggestions for ambiguous query"""
        suggestions = self.processor.get_suggestions("something")
        assert 'categories' in suggestions or 'price_range' in suggestions
    
    def test_get_suggestions_returns_brands(self):
        """Test that suggestions include popular brands"""
        suggestions = self.processor.get_suggestions("shoes")
        if suggestions.get('popular_brands'):
            assert isinstance(suggestions['popular_brands'], list)
    
    def test_get_suggestions_returns_samples(self):
        """Test that suggestions include sample products"""
        suggestions = self.processor.get_suggestions("shoes")
        if suggestions.get('sample_products'):
            assert isinstance(suggestions['sample_products'], list)
    
    # Metadata tests
    def test_get_categories(self):
        """Test getting available categories"""
        categories = self.processor.get_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0
    
    def test_get_brands(self):
        """Test getting available brands"""
        brands = self.processor.get_brands()
        assert isinstance(brands, list)
        assert len(brands) > 0
    
    # Ranking tests
    def test_ranking_by_relevance(self):
        """Test that results are ranked by relevance"""
        result = self.processor.process_query("red shoes")
        products = result['products']
        if len(products) > 1:
            # First product should be more relevant than others
            first_name = products[0]['name'].lower()
            assert 'red' in first_name or 'shoe' in first_name
    
    def test_ranking_by_rating(self):
        """Test that higher rated products are ranked higher"""
        result = self.processor.process_query("shoes")
        products = result['products']
        if len(products) > 1:
            # Check if products are sorted by rating (descending)
            ratings = [p['rating'] for p in products]
            assert ratings == sorted(ratings, reverse=True)
    
    # Error handling tests
    def test_process_query_with_very_long_query(self):
        """Test processing very long query"""
        long_query = "a" * 1000
        result = self.processor.process_query(long_query)
        # Should handle gracefully
        assert 'success' in result
    
    def test_process_query_with_unicode(self):
        """Test processing query with unicode characters"""
        result = self.processor.process_query("जूते shoes")
        # Should handle gracefully
        assert 'success' in result
    
    # Integration tests
    def test_full_flow_budget_category_color(self):
        """Test full flow with budget, category, and color"""
        result = self.processor.process_query("red running shoes under 3000")
        assert result['success'] is True
        assert result['category'] == 'apparel'
        assert result['max_budget'] == 3000
        # All products should be apparel and under budget
        for product in result['products']:
            assert product['category'] == 'apparel'
            assert product['price'] <= 3000
    
    def test_full_flow_electronics_premium(self):
        """Test full flow for premium electronics"""
        result = self.processor.process_query("premium laptop")
        assert result['success'] is True
        assert result['category'] == 'electronics'
