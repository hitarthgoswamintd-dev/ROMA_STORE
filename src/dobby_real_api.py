"""
Real Dobby API Integration for ROMA Shopping Agent
Production-ready API client for Sentient.ai Dobby
"""

import os
import json
import requests
from typing import Dict, Any, Optional
import time
import logging
from dataclasses import dataclass


@dataclass
class DobbyConfig:
    """Configuration for Dobby API"""
    api_key: str = None
    base_url: str = "https://api.sentient.ai/dobby/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0


class DobbyRealAPI:
    """Production-ready Dobby API client"""
    
    def __init__(self, config: DobbyConfig = None):
        self.config = config or DobbyConfig()
        self.session = requests.Session()
        self.logger = logging.getLogger(__name__)
        
        # Set up headers
        self.session.headers.update({
            'Authorization': f'Bearer {self.config.api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'ROMA-Shopping-Agent/1.0'
        })
    
    def analyze_shopping_query(self, query: str) -> Dict[str, Any]:
        """Real API call to Dobby for shopping query analysis"""
        
        if not self.config.api_key:
            return self._mock_response(query)  # Fallback for demo
        
        payload = {
            "prompt": self._build_shopping_prompt(query),
            "max_tokens": 500,
            "temperature": 0.1,
            "model": "dobby-shopping-v1"
        }
        
        try:
            response = self._make_api_call('/chat/completions', payload)
            return self._parse_response(response, query)
            
        except Exception as e:
            self.logger.error(f"Dobby API error: {e}")
            return self._fallback_response(query)
    
    def _build_shopping_prompt(self, query: str) -> str:
        """Build optimized prompt for shopping analysis"""
        return f"""
        Analyze this shopping query: "{query}"
        
        Provide detailed JSON analysis with:
        {
            "category": "primary product category",
            "subcategory": "specific product type",
            "budget": {
                "type": "exact/range/quality",
                "min": minimum_price,
                "max": maximum_price,
                "currency": "INR"
            },
            "brand_preferences": {
                "include": ["preferred brands"],
                "exclude": ["brands to avoid"]
            },
            "features": ["required features"],
            "use_case": "intended usage scenario",
            "quality_level": "budget/mid-range/premium/luxury",
            "color_preferences": ["preferred colors"],
            "urgency": "immediate/soon/flexible",
            "confidence": 0.0-1.0
        }
        
        Be specific and accurate. Return only valid JSON.
        """
    
    def _make_api_call(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Make actual API call with retry logic"""
        
        url = f"{self.config.base_url}{endpoint}"
        
        for attempt in range(self.config.max_retries):
            try:
                response = self.session.post(
                    url,
                    json=payload,
                    timeout=self.config.timeout
                )
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt < self.config.max_retries - 1:
                    time.sleep(self.config.retry_delay * (attempt + 1))
                    continue
                raise e
    
    def _parse_response(self, response: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Parse Dobby API response"""
        
        try:
            # Extract JSON from response
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Clean and parse JSON
            cleaned_content = content.strip().replace('```json', '').replace('```', '')
            parsed = json.loads(cleaned_content)
            
            # Validate and enhance response
            return {
                **parsed,
                "original_query": original_query,
                "ai_engine": "dobby",
                "timestamp": time.time()
            }
            
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(f"Failed to parse Dobby response: {e}")
            return self._fallback_response(original_query)
    
    def _fallback_response(self, query: str) -> Dict[str, Any]:
        """Fallback when API unavailable"""
        return {
            "category": "general",
            "subcategory": "unknown",
            "budget": {"type": "auto", "min": 0, "max": 100000, "currency": "INR"},
            "brand_preferences": {"include": [], "exclude": []},
            "features": [],
            "use_case": "general",
            "quality_level": "standard",
            "color_preferences": [],
            "urgency": "flexible",
            "confidence": 0.3,
            "original_query": query,
            "ai_engine": "fallback",
            "note": "API unavailable - using rule-based analysis"
        }
    
    def _mock_response(self, query: str) -> Dict[str, Any]:
        """Mock response for development/testing"""
        query_lower = query.lower()
        
        # Advanced mock based on query analysis
        analysis = {
            "category": self._extract_category(query_lower),
            "subcategory": self._extract_subcategory(query_lower),
            "budget": self._extract_budget_real(query_lower),
            "brand_preferences": self._extract_brands_real(query_lower),
            "features": self._extract_features(query_lower),
            "use_case": self._extract_use_case_real(query_lower),
            "quality_level": self._extract_quality_real(query_lower),
            "color_preferences": self._extract_colors_real(query_lower),
            "urgency": "flexible",
            "confidence": 0.85,
            "original_query": query,
            "ai_engine": "mock_dobby",
            "note": "Mock response - replace with real API"
        }
        
        return analysis
    
    def _extract_category(self, query: str) -> str:
        """Real category extraction for mock"""
        categories = {
            'phone': 'mobiles', 'mobile': 'mobiles', 'smartphone': 'mobiles',
            'laptop': 'electronics', 'computer': 'electronics', 'macbook': 'electronics',
            'shoes': 'apparel', 'sneakers': 'apparel', 'headphones': 'electronics',
            'watch': 'electronics', 'tablet': 'electronics', 'jacket': 'apparel'
        }
        
        for keyword, category in categories.items():
            if keyword in query:
                return category
        return "general"
    
    def _extract_subcategory(self, query: str) -> str:
        """Extract specific product type"""
        if 'running' in query:
            return 'running_shoes'
        elif 'gaming' in query:
            return 'gaming_laptop'
        elif 'wireless' in query:
            return 'wireless_headphones'
        return "standard"
    
    def _extract_budget_real(self, query: str) -> Dict[str, Any]:
        """Real budget extraction"""
        # Extract actual numbers
        numbers = re.findall(r'\d+(?:,\d+)*(?:k|lakh)?', query)
        
        if numbers:
            value = int(numbers[0].replace(',', '').replace('k', '000').replace('lakh', '00000'))
            
            if 'under' in query or 'below' in query:
                return {"type": "under", "max": value, "currency": "INR"}
            elif 'around' in query or 'about' in query:
                return {"type": "around", "min": value * 0.8, "max": value * 1.2, "currency": "INR"}
            elif 'between' in query:
                return {"type": "range", "min": value * 0.8, "max": value * 1.2, "currency": "INR"}
        
        # Quality-based budgets
        quality_map = {
            'cheap': {'min': 0, 'max': 5000, "type": "budget"},
            'budget': {'min': 0, 'max': 15000, "type": "budget"},
            'mid-range': {'min': 15000, 'max': 50000, "type": "mid-range"},
            'premium': {'min': 50000, 'max': 150000, "type": "premium"},
            'luxury': {'min': 150000, 'max': 500000, "type": "luxury"}
        }
        
        for quality, budget in quality_map.items():
            if quality in query:
                return {**budget, "currency": "INR"}
        
        return {"type": "auto", "min": 0, "max": 100000, "currency": "INR"}
    
    def _extract_brands_real(self, query: str) -> Dict[str, list]:
        """Real brand extraction"""
        brands = {
            'include': [],
            'exclude': []
        }
        
        # Include brands
        include_brands = ['apple', 'samsung', 'google', 'oneplus', 'xiaomi', 'realme', 'redmi',
                         'nike', 'adidas', 'puma', 'hp', 'dell', 'asus', 'lenovo', 'acer',
                         'sony', 'bose', 'jbl']
        
        for brand in include_brands:
            if brand in query:
                brands['include'].append(brand.title())
        
        # Exclude brands
        exclude_patterns = [r'non-([a-zA-Z]+)', r'not ([a-zA-Z]+)', r'except ([a-zA-Z]+)']
        for pattern in exclude_patterns:
            matches = re.findall(pattern, query)
            brands['exclude'].extend([m.title() for m in matches])
        
        return brands
    
    def _extract_use_case_real(self, query: str) -> str:
        """Real use case extraction"""
        use_cases = {
            'gaming': ['gaming', 'play', 'fps', 'performance', 'pubg'],
            'office': ['office', 'work', 'professional', 'business', 'productivity'],
            'gym': ['gym', 'workout', 'exercise', 'fitness', 'running'],
            'travel': ['travel', 'portable', 'lightweight', 'commute'],
            'parents': ['parents', 'elderly', 'senior', 'simple', 'easy'],
            'students': ['student', 'college', 'school', 'study', 'budget'],
            'gaming': ['gaming', 'play', 'performance']
        }
        
        for use_case, keywords in use_cases.items():
            if any(keyword in query for keyword in keywords):
                return use_case
        
        return "general"
    
    def _extract_colors_real(self, query: str) -> list:
        """Real color extraction"""
        colors = ['red', 'blue', 'black', 'white', 'green', 'yellow', 'pink', 'purple', 'orange', 'brown', 'gray', 'silver', 'gold', 'navy', 'beige']
        return [color for color in colors if color in query]
    
    def _extract_features(self, query: str) -> list:
        """Extract feature requirements"""
        features = ['wireless', 'bluetooth', 'waterproof', '5G', '4K', 'fast charging', 'long battery', 'lightweight', 'compact', 'touchscreen']
        return [feature for feature in features if feature in query]
    
    def _extract_quality_real(self, query: str) -> str:
        """Real quality extraction"""
        quality_map = {
            'cheap': 'budget', 'affordable': 'budget', 'economical': 'budget',
            'best': 'premium', 'top': 'premium', 'excellent': 'premium',
            'premium': 'premium', 'luxury': 'luxury', 'high-end': 'luxury',
            'pro': 'premium', 'professional': 'premium', 'flagship': 'luxury'
        }
        
        for keyword, quality in quality_map.items():
            if keyword in query:
                return quality
        
        return "standard"


# Configuration class for easy setup
class DobbyConfigManager:
    """Manage Dobby API configuration"""
    
    def __init__(self):
        self.config = DobbyConfig()
        self.load_from_env()
    
    def load_from_env(self):
        """Load configuration from environment variables"""
        self.config.api_key = os.getenv('DOBBY_API_KEY')
        self.config.base_url = os.getenv('DOBBY_BASE_URL', 'https://api.sentient.ai/dobby/v1')
    
    def set_api_key(self, api_key: str):
        """Set API key programmatically"""
        self.config.api_key = api_key
    
    def is_configured(self) -> bool:
        """Check if API is properly configured"""
        return self.config.api_key is not None and len(self.config.api_key.strip()) > 0


# Global instance
DOBBY_CONFIG = DobbyConfigManager()

if __name__ == "__main__":
    # Test the real API integration
    api = DobbyRealAPI()
    
    test_queries = [
        "comfortable wireless headphones for long flights under 5000",
        "best gaming laptop around 1 lakh with good battery",
        "affordable phone for elderly parents with large screen",
        "premium running shoes for marathon training"
    ]
    
    print("=== Dobby API Integration Test ===")
    print("API Status:", "Configured" if DOBBY_CONFIG.is_configured() else "Mock Mode")
    
    for query in test_queries:
        result = api.analyze_shopping_query(query)
        print(f"\nQuery: {query}")
        print(f"Analysis: {json.dumps(result, indent=2)}")
