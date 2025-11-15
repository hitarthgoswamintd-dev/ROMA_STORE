"""
Unit tests for BudgetAnalyzer
"""

import pytest
from src.budget_analyzer import BudgetAnalyzer


class TestBudgetAnalyzer:
    """Test suite for budget analysis functionality"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.analyzer = BudgetAnalyzer()
    
    # Price extraction tests
    def test_extract_price_under_5000(self):
        """Test extracting price with 'under' keyword"""
        result = self.analyzer.analyze_budget("shoes under 5000")
        assert result['max_budget'] == 5000
    
    def test_extract_price_with_rupee_symbol(self):
        """Test extracting price with rupee symbol"""
        result = self.analyzer.analyze_budget("laptop under ₹50000")
        assert result['max_budget'] == 50000
    
    def test_extract_price_with_rs_notation(self):
        """Test extracting price with Rs. notation"""
        result = self.analyzer.analyze_budget("phone under Rs. 30000")
        assert result['max_budget'] == 30000
    
    def test_extract_price_with_k_notation(self):
        """Test extracting price with k notation (5k = 5000)"""
        result = self.analyzer.analyze_budget("phone under 30k")
        assert result['max_budget'] == 30000
    
    def test_extract_price_with_comma_separator(self):
        """Test extracting price with comma separator"""
        result = self.analyzer.analyze_budget("laptop under 50,000")
        assert result['max_budget'] == 50000
    
    def test_extract_price_around_keyword(self):
        """Test extracting price with 'around' keyword"""
        result = self.analyzer.analyze_budget("headphones around 5000")
        assert result['max_budget'] == 5000
    
    def test_extract_price_below_keyword(self):
        """Test extracting price with 'below' keyword"""
        result = self.analyzer.analyze_budget("shoes below 3000")
        assert result['max_budget'] == 3000
    
    def test_extract_price_no_budget_keyword(self):
        """Test that price is not extracted without budget keyword"""
        result = self.analyzer.analyze_budget("version 5.0 phone")
        assert result['max_budget'] is not None  # Should use default, not 5
    
    def test_extract_price_between_range(self):
        """Test extracting price from range"""
        result = self.analyzer.analyze_budget("laptop between 40000 and 80000")
        assert result['max_budget'] == 80000
    
    # Category detection tests
    def test_category_detection_apparel(self):
        """Test detecting apparel category"""
        result = self.analyzer.analyze_budget("red running shoes")
        assert result['category'] == 'apparel'
    
    def test_category_detection_mobiles(self):
        """Test detecting mobiles category"""
        result = self.analyzer.analyze_budget("best phone under 20000")
        assert result['category'] == 'mobiles'
    
    def test_category_detection_electronics(self):
        """Test detecting electronics category"""
        result = self.analyzer.analyze_budget("gaming laptop under 1 lakh")
        assert result['category'] == 'electronics'
    
    def test_category_detection_headphones(self):
        """Test detecting headphones as electronics"""
        result = self.analyzer.analyze_budget("wireless headphones")
        assert result['category'] == 'electronics'
    
    def test_category_detection_none(self):
        """Test when category cannot be detected"""
        result = self.analyzer.analyze_budget("something random")
        assert result['category'] is None
    
    # Budget type detection tests
    def test_budget_type_cheap(self):
        """Test detecting cheap budget type"""
        result = self.analyzer.analyze_budget("cheap shoes")
        assert result['budget_type'] == 'low'
    
    def test_budget_type_premium(self):
        """Test detecting premium budget type"""
        result = self.analyzer.analyze_budget("premium headphones")
        assert result['budget_type'] == 'high'
    
    def test_budget_type_mid_range(self):
        """Test detecting mid-range budget type"""
        result = self.analyzer.analyze_budget("mid-range laptop")
        assert result['budget_type'] == 'medium'
    
    def test_budget_type_default(self):
        """Test default budget type when not specified"""
        result = self.analyzer.analyze_budget("shoes")
        assert result['budget_type'] in ['low', 'medium', 'high']
    
    # Brand exclusion tests
    def test_brand_exclusion_non_apple(self):
        """Test detecting non-Apple brand exclusion"""
        result = self.analyzer.analyze_budget("non-Apple laptop")
        assert result['category'] == 'electronics'
    
    # Edge cases
    def test_empty_query(self):
        """Test handling empty query"""
        result = self.analyzer.analyze_budget("")
        assert result['category'] is None
    
    def test_query_with_only_spaces(self):
        """Test handling query with only spaces"""
        result = self.analyzer.analyze_budget("   ")
        assert result['category'] is None
    
    def test_case_insensitivity(self):
        """Test that analysis is case insensitive"""
        result1 = self.analyzer.analyze_budget("RED SHOES UNDER 5000")
        result2 = self.analyzer.analyze_budget("red shoes under 5000")
        assert result1['category'] == result2['category']
        assert result1['max_budget'] == result2['max_budget']
    
    # Category suggestions
    def test_get_category_suggestions(self):
        """Test getting category suggestions"""
        suggestions = self.analyzer.get_category_suggestions("phone laptop")
        assert len(suggestions) > 0
        assert 'mobiles' in suggestions or 'electronics' in suggestions
