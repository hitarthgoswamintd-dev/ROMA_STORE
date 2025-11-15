"""
Fireworks AI Integration for ROMA Shopping Agent
Qwen3-8B for natural language query simplification
"""

import os
import json
import time
import requests
from typing import Dict, Any, Optional
from datetime import datetime


class FireworksAIClient:
    """Production-ready Fireworks AI client for ROMA"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('FIREWORKS_API_KEY')
        if not self.api_key:
            raise ValueError("FIREWORKS_API_KEY environment variable not set. Please set it in .env file.")
        self.base_url = "https://api.fireworks.ai/inference/v1/chat/completions"
        self.model = "accounts/fireworks/models/qwen3-8b"
        self.rate_limiter = RateLimiter(max_requests=10, window_seconds=60)
        
        # Shopping-specific system prompt
        self.system_prompt = """
        You are ROMA's AI shopping assistant. Your job is to take complex natural language shopping queries and convert them into precise, structured data that ROMA can process.
        
        INPUT: Natural language shopping query from user
        OUTPUT: JSON with exact shopping parameters
        
        RULES:
        1. Always return valid JSON
        2. Be specific about categories and budgets
        3. Include brand preferences when mentioned
        4. Extract use cases from context
        5. Handle negations properly
        6. Convert vague terms to specific values
        
        EXAMPLE:
        Input: "comfortable wireless headphones for long flights under 5000"
        Output: {
            "category": "electronics",
            "subcategory": "wireless_headphones",
            "budget": {"min": 0, "max": 5000, "currency": "INR"},
            "specifications": ["wireless", "comfortable", "long_battery"],
            "use_case": "travel",
            "brand_preferences": {"include": [], "exclude": []},
            "quality_level": "mid_range",
            "confidence": 0.9
        }
        """
    
    def simplify_shopping_query(self, query: str) -> Dict[str, Any]:
        """Convert natural language query to structured shopping data"""
        
        # Check rate limit
        if not self.rate_limiter.allow_request():
            return self._rate_limit_response()
        
        # Build optimized prompt
        prompt = self._build_shopping_prompt(query)
        
        # Make API call
        return self._call_fireworks_api(prompt, query)
    
    def _build_shopping_prompt(self, query: str) -> str:
        """Build shopping-optimized prompt"""
        return f"""
        Convert this shopping query to structured data:
        "{query}"
        
        Return JSON with these exact fields:
        {{
            "category": "main product category",
            "subcategory": "specific product type",
            "budget": {{
                "min": minimum_price,
                "max": maximum_price,
                "currency": "INR"
            }},
            "specifications": [list of required features],
            "use_case": "intended usage scenario",
            "brand_preferences": {{
                "include": [preferred brands],
                "exclude": [brands to avoid]
            }},
            "quality_level": "budget/mid_range/premium/luxury",
            "color_preferences": [preferred colors],
            "urgency": "immediate/soon/flexible",
            "confidence": 0.0-1.0
        }}
        """
    
    def _call_fireworks_api(self, prompt: str, original_query: str) -> Dict[str, Any]:
        """Make actual API call to Fireworks"""
        
        payload = {
            "model": self.model,
            "max_tokens": 512,
            "top_p": 1,
            "top_k": 40,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            return self._parse_fireworks_response(response.json(), original_query)
            
        except Exception as e:
            return self._fallback_response(original_query, str(e))
    
    def _parse_fireworks_response(self, response: Dict[str, Any], original_query: str) -> Dict[str, Any]:
        """Parse Fireworks response into structured data"""
        try:
            content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
            
            # Clean and parse JSON
            cleaned = content.strip()
            if cleaned.startswith('```json'):
                cleaned = cleaned[7:]
            if cleaned.endswith('```'):
                cleaned = cleaned[:-3]
            
            parsed = json.loads(cleaned)
            
            # Ensure all required fields
            return {
                **parsed,
                "original_query": original_query,
                "ai_engine": "fireworks_qwen3",
                "timestamp": datetime.now().isoformat(),
                "success": True
            }
            
        except json.JSONDecodeError:
            return self._fallback_response(original_query, "Invalid JSON response")
    
    def _fallback_response(self, query: str, error: str = None) -> Dict[str, Any]:
        """Fallback when API fails"""
        return {
            "category": "general",
            "subcategory": "unknown",
            "budget": {"min": 0, "max": 100000, "currency": "INR"},
            "specifications": [],
            "use_case": "general",
            "brand_preferences": {"include": [], "exclude": []},
            "quality_level": "standard",
            "color_preferences": [],
            "urgency": "flexible",
            "confidence": 0.3,
            "original_query": query,
            "ai_engine": "fallback",
            "error": error or "API unavailable",
            "success": False
        }
    
    def _rate_limit_response(self) -> Dict[str, Any]:
        """Rate limit response"""
        return {
            "error": "Rate limit exceeded",
            "retry_after": self.rate_limiter.get_retry_after(),
            "success": False
        }


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = []
    
    def allow_request(self) -> bool:
        """Check if request is allowed"""
        now = time.time()
        
        # Remove old requests
        self.requests = [req_time for req_time in self.requests if now - req_time < self.window_seconds]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        
        return False
    
    def get_retry_after(self) -> int:
        """Get retry after time in seconds"""
        if not self.requests:
            return 0
        
        oldest_request = min(self.requests)
        return max(0, int(self.window_seconds - (time.time() - oldest_request)))


# Production-ready client
class ROMAFireworksClient:
    """Production client for ROMA + Fireworks AI"""
    
    def __init__(self):
        self.fireworks = FireworksAIClient()
    
    def process_shopping_query(self, query: str) -> Dict[str, Any]:
        """Main entry point for query processing"""
        return self.fireworks.simplify_shopping_query(query)
    
    def test_connection(self) -> bool:
        """Test API connection"""
        try:
            result = self.process_shopping_query("test query")
            return result.get("success", False)
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False


# Usage example
if __name__ == "__main__":
    client = ROMAFireworksClient()
    
    test_queries = [
        "comfortable wireless headphones for long flights under 5000",
        "best gaming laptop around 1 lakh with good battery",
        "affordable phone for elderly parents with large screen",
        "premium running shoes for marathon training",
        "good laptop for coding and occasional gaming"
    ]
    
    print("=== Fireworks AI Shopping Query Processing ===")
    
    for query in test_queries:
        result = client.process_shopping_query(query)
        print(f"\n🎯 Query: {query}")
        print(f"📊 Analysis: {json.dumps(result, indent=2, ensure_ascii=False)}")
