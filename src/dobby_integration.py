"""
Dobby AI Integration for ROMA Shopping Agent
Advanced natural language understanding with Dobby by Sentient
"""

import os
import json
import requests
from typing import Dict, Any, Optional
import re


class DobbyNLP:
    """Dobby AI integration for semantic query understanding"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('DOBBY_API_KEY')
        if not self.api_key:
            # Use mock mode if no API key provided
            self.api_key = None
        self.base_url = "https://api.sentient.ai/dobby/v1"
        
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Use Dobby to understand shopping queries semantically"""
        
        # Dobby API payload for shopping query analysis
        payload = {
            "prompt": f"""
            Analyze this shopping query: "{query}"
            
            Extract:
            1. Product category
            2. Budget range (if mentioned)
            3. Brand preferences (include/exclude)
            4. Color preferences
            5. Use case/intent
            6. Quality indicators (premium, cheap, best)
            7. Any other constraints
            
            Return as JSON with confidence scores.
            """,
            "max_tokens": 300,
            "temperature": 0.1
        }
        
        try:
            # Mock Dobby response (in production, this would be actual API call)
            return self._mock_dobby_response(query)
        except Exception as e:
            return self._fallback_analysis(query)
    
    def _mock_dobby_response(self, query: str) -> Dict[str, Any]:
        """Mock Dobby response for demonstration"""
        query_lower = query.lower()
        
        # Advanced semantic analysis
        analysis = {
            "category": self._extract_category(query_lower),
            "budget": self._extract_budget(query_lower),
            "brand_preferences": self._extract_brands(query_lower),
            "color_preferences": self._extract_colors(query_lower),
            "use_case": self._extract_use_case(query_lower),
            "quality_indicator": self._extract_quality(query_lower),
            "constraints": self._extract_constraints(query_lower),
            "confidence": 0.85
        }
        
        return analysis
    
    def _extract_category(self, query: str) -> str:
        """Semantic category extraction"""
        category_map = {
            'phone': 'mobiles', 'mobile': 'mobiles', 'smartphone': 'mobiles',
            'laptop': 'electronics', 'computer': 'electronics', 'macbook': 'electronics',
            'shoes': 'apparel', 'sneakers': 'apparel', 'running shoes': 'apparel',
            'headphones': 'electronics', 'earphones': 'electronics', 'headset': 'electronics',
            'jacket': 'apparel', 'denim': 'apparel', 'coat': 'apparel',
            'watch': 'electronics', 'smartwatch': 'electronics', 'fitness band': 'electronics',
            'tablet': 'electronics', 'ipad': 'electronics'
        }
        
        for keyword, category in category_map.items():
            if keyword in query:
                return category
        return "general"
    
    def _extract_budget(self, query: str) -> Dict[str, Any]:
        """Advanced budget extraction with context"""
        budget_patterns = [
            (r'under\s+(\d+(?:,\d+)*)', 'under'),
            (r'below\s+(\d+(?:,\d+)*)', 'under'),
            (r'less than\s+(\d+(?:,\d+)*)', 'under'),
            (r'upto\s+(\d+(?:,\d+)*)', 'under'),
            (r'around\s+(\d+(?:,\d+)*)', 'around'),
            (r'between\s+(\d+(?:,\d+)*)\s+and\s+(\d+(?:,\d+)*)', 'range')
        ]
        
        quality_budgets = {
            'cheap': 5000,
            'budget': 10000,
            'mid-range': 30000,
            'premium': 80000,
            'luxury': 150000
        }
        
        # Check for explicit numbers
        for pattern, type in budget_patterns:
            match = re.search(pattern, query)
            if match:
                if type == 'range':
                    return {
                        'type': 'range',
                        'min': int(match.group(1).replace(',', '')),
                        'max': int(match.group(2).replace(',', ''))
                    }
                else:
                    return {
                        'type': type,
                        'value': int(match.group(1).replace(',', ''))
                    }
        
        # Check for quality indicators
        for quality, budget in quality_budgets.items():
            if quality in query:
                return {
                    'type': 'quality_based',
                    'value': budget,
                    'quality': quality
                }
        
        return {'type': 'auto', 'value': None}
    
    def _extract_brands(self, query: str) -> Dict[str, list]:
        """Brand preference extraction"""
        brands = {
            'include': [],
            'exclude': []
        }
        
        brand_list = [
            'apple', 'samsung', 'google', 'oneplus', 'xiaomi', 'realme', 'redmi',
            'nike', 'adidas', 'puma', 'reebok', 'new balance', 'asics',
            'hp', 'dell', 'asus', 'lenovo', 'acer', 'msi',
            'sony', 'bose', 'jbl', 'sennheiser', 'skullcandy'
        ]
        
        # Extract brands to include
        for brand in brand_list:
            if brand in query:
                brands['include'].append(brand)
        
        # Extract brands to exclude
        exclude_patterns = [
            r'non-([a-zA-Z]+)',
            r'not ([a-zA-Z]+)',
            r'except ([a-zA-Z]+)',
            r'excluding ([a-zA-Z]+)'
        ]
        
        for pattern in exclude_patterns:
            matches = re.findall(pattern, query)
            brands['exclude'].extend(matches)
        
        return brands
    
    def _extract_colors(self, query: str) -> list:
        """Color preference extraction"""
        colors = ['red', 'blue', 'black', 'white', 'green', 'yellow', 'pink', 'purple', 'orange', 'brown', 'gray', 'silver', 'gold']
        return [color for color in colors if color in query]
    
    def _extract_use_case(self, query: str) -> str:
        """Understand the intended use"""
        use_cases = {
            'gaming': ['gaming', 'play', 'fps', 'performance'],
            'office': ['office', 'work', 'professional', 'business'],
            'gym': ['gym', 'workout', 'exercise', 'fitness'],
            'travel': ['travel', 'portable', 'lightweight'],
            'parents': ['parents', 'elderly', 'senior', 'simple'],
            'students': ['student', 'college', 'school', 'study']
        }
        
        for use_case, keywords in use_cases.items():
            if any(keyword in query for keyword in keywords):
                return use_case
        
        return "general"
    
    def _extract_quality(self, query: str) -> str:
        """Quality indicator extraction"""
        quality_map = {
            'cheap': 'budget',
            'affordable': 'budget',
            'best': 'premium',
            'top': 'premium',
            'premium': 'premium',
            'luxury': 'luxury',
            'pro': 'premium',
            'professional': 'premium'
        }
        
        for keyword, quality in quality_map.items():
            if keyword in query:
                return quality
        
        return "standard"
    
    def _extract_constraints(self, query: str) -> list:
        """Extract additional constraints"""
        constraints = []
        
        # Size constraints
        size_words = ['large', 'small', 'compact', 'portable', 'lightweight']
        constraints.extend([word for word in size_words if word in query])
        
        # Feature constraints
        feature_words = ['wireless', 'bluetooth', 'waterproof', 'fast charging', '5G', '4K']
        constraints.extend([word for word in feature_words if word in query])
        
        return constraints
    
    def _fallback_analysis(self, query: str) -> Dict[str, Any]:
        """Fallback to rule-based analysis if Dobby unavailable"""
        return {
            "category": "general",
            "budget": {"type": "auto", "value": None},
            "brand_preferences": {"include": [], "exclude": []},
            "color_preferences": [],
            "use_case": "general",
            "quality_indicator": "standard",
            "constraints": [],
            "confidence": 0.5
        }


class DobbyEnhancedProcessor:
    """Enhanced processor using Dobby AI"""
    
    def __init__(self):
        self.dobby = DobbyNLP()
        self.url_builder = None  # Will be set from web_scraper
    
    def process_with_dobby(self, query: str) -> Dict[str, Any]:
        """Process query using Dobby AI understanding"""
        
        # Get Dobby's semantic analysis
        analysis = self.dobby.analyze_query(query)
        
        # Build enhanced search parameters
        search_params = {
            "query": query,
            "category": analysis["category"],
            "budget": analysis["budget"],
            "brands": analysis["brand_preferences"],
            "colors": analysis["color_preferences"],
            "use_case": analysis["use_case"],
            "quality": analysis["quality_indicator"],
            "constraints": analysis["constraints"],
            "confidence": analysis["confidence"]
        }
        
        return search_params
    
    def generate_natural_response(self, query: str, products: list) -> str:
        """Generate human-like response using Dobby"""
        
        # Mock Dobby response generation
        count = len(products)
        if count == 0:
            return f"I couldn't find any products matching '{query}'. Try adjusting your criteria."
        
        avg_price = sum(p['price'] for p in products) / count
        
        response = f"Based on your search for '{query}', I found {count} great options. "
        
        if avg_price < 10000:
            response += "These are all excellent budget-friendly choices."
        elif avg_price < 50000:
            response += "These offer great value in the mid-range segment."
        else:
            response += "These are premium options with top-tier features."
        
        return response


# Test Dobby integration
if __name__ == "__main__":
    dobby = DobbyNLP()
    
    test_queries = [
        "red running shoes under 3000 for gym",
        "best non-Apple phone under 50000",
        "comfortable wireless headphones for long flights",
        "premium gaming laptop around 1 lakh",
        "cheap but good phone for elderly parents"
    ]
    
    print("=== Dobby NLP Analysis ===")
    for query in test_queries:
        result = dobby.analyze_query(query)
        print(f"\nQuery: {query}")
        print(f"Analysis: {json.dumps(result, indent=2)}")
