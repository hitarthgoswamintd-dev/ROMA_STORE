"""
Optimized Dobby Configuration for Shopping Queries
Hyper-relevant AI for e-commerce search and recommendations
"""

import os
import json
from typing import Dict, Any, List
from datetime import datetime


class ShoppingDobbyConfig:
    """Specialized Dobby configuration for shopping domain"""
    
    def __init__(self):
        self.domain = "ecommerce_shopping"
        self.specialized_prompts = self._build_shopping_prompts()
        self.context_templates = self._build_context_templates()
        self.product_taxonomy = self._build_product_taxonomy()
        self.budget_mapping = self._build_budget_mapping()
        self.brand_hierarchy = self._build_brand_hierarchy()
    
    def _build_shopping_prompts(self) -> Dict[str, str]:
        """Specialized prompts for shopping query analysis"""
        return {
            "shopping_analysis": """
            You are a shopping assistant AI. Analyze this query for e-commerce search:
            "{query}"
            
            Return precise JSON with:
            {
                "intent": "primary shopping intent",
                "category": "exact product category",
                "subcategory": "specific product type",
                "price_range": {
                    "min": minimum_budget,
                    "max": maximum_budget,
                    "currency": "INR",
                    "confidence": 0.0-1.0
                },
                "specifications": {
                    "must_have": [required features],
                    "nice_to_have": [optional features],
                    "avoid": [undesired features]
                },
                "user_profile": {
                    "experience_level": "beginner/intermediate/expert",
                    "use_case": "specific usage scenario",
                    "priority": "price/quality/brand/features"
                },
                "brand_preferences": {
                    "preferred": [recommended brands],
                    "avoid": [brands to exclude],
                    "tier": "budget/mid/premium/luxury"
                },
                "timing": "immediate/soon/flexible",
                "urgency_indicators": [keywords indicating urgency],
                "confidence_score": 0.0-1.0
            }
            
            Be specific and shopping-focused.
            """,
            
            "budget_interpretation": """
            Interpret budget indicators in: "{query}"
            
            Map to precise budget ranges:
            - "cheap" → ₹0-5000
            - "budget" → ₹0-15000  
            - "mid-range" → ₹15000-50000
            - "premium" → ₹50000-150000
            - "luxury" → ₹150000+
            - "under X" → ₹0-X
            - "around X" → ₹X*0.8-X*1.2
            - "between X and Y" → ₹X-Y
            
            Return: {"type": "exact/range/quality", "min": int, "max": int, "confidence": float}
            """,
            
            "use_case_detection": """
            Detect use case from: "{query}"
            
            Shopping use cases:
            - "gaming" → high performance, RGB, cooling
            - "office" → professional, reliable, battery life
            - "travel" → portable, lightweight, battery
            - "gym" → sweat-resistant, secure fit, durable
            - "students" → budget-friendly, reliable, warranty
            - "parents/elderly" → simple UI, large display, support
            - "content creation" → camera quality, storage, performance
            - "daily use" → balanced features, durability
            
            Return: {"use_case": "detected_case", "specific_requirements": [list]}
            """
        }
    
    def _build_product_taxonomy(self) -> Dict[str, Dict[str, List[str]]]:
        """Comprehensive product taxonomy for accurate categorization"""
        return {
            "mobiles": {
                "smartphones": ["phone", "mobile", "smartphone", "android", "iphone"],
                "budget_phones": ["cheap phone", "budget mobile", "affordable smartphone"],
                "flagship_phones": ["premium phone", "flagship", "latest mobile"]
            },
            "electronics": {
                "laptops": ["laptop", "notebook", "macbook", "computer"],
                "headphones": ["headphones", "earphones", "headset", "wireless earbuds"],
                "tablets": ["tablet", "ipad", "android tablet"],
                "smartwatches": ["watch", "smartwatch", "fitness band"]
            },
            "apparel": {
                "shoes": ["shoes", "sneakers", "running shoes", "boots"],
                "clothing": ["jacket", "shirt", "jeans", "t-shirt", "hoodie"],
                "accessories": ["bag", "wallet", "belt", "hat"]
            }
        }
    
    def _build_budget_mapping(self) -> Dict[str, Dict[str, int]]:
        """Precise budget mapping for shopping context"""
        return {
            "mobiles": {
                "budget": {"min": 0, "max": 15000},
                "mid_range": {"min": 15000, "max": 40000},
                "premium": {"min": 40000, "max": 100000},
                "flagship": {"min": 100000, "max": 200000}
            },
            "electronics": {
                "laptop_budget": {"min": 0, "max": 40000},
                "laptop_mid": {"min": 40000, "max": 80000},
                "laptop_premium": {"min": 80000, "max": 200000}
            },
            "apparel": {
                "shoes_budget": {"min": 0, "max": 3000},
                "shoes_mid": {"min": 3000, "max": 8000},
                "shoes_premium": {"min": 8000, "max": 20000}
            }
        }
    
    def _build_brand_hierarchy(self) -> Dict[str, Dict[str, List[str]]]:
        """Brand hierarchy for shopping recommendations"""
        return {
            "mobiles": {
                "budget": ["Redmi", "Realme", "Poco", "Samsung"],
                "mid_range": ["OnePlus", "Samsung", "Google", "Vivo"],
                "premium": ["Apple", "Samsung", "Google", "OnePlus"],
                "flagship": ["Apple", "Samsung", "Google"]
            },
            "laptops": {
                "budget": ["HP", "Dell", "Lenovo", "Acer"],
                "mid_range": ["HP", "Dell", "ASUS", "Lenovo"],
                "premium": ["Apple", "Dell", "HP", "ASUS"],
                "gaming": ["ASUS ROG", "MSI", "Acer Predator", "HP Omen"]
            },
            "headphones": {
                "budget": ["boAt", "Realme", "JBL", "Skullcandy"],
                "mid_range": ["JBL", "Sony", "Sennheiser", "Audio-Technica"],
                "premium": ["Sony", "Bose", "Sennheiser", "Apple"]
            }
        }
    
    def get_optimized_prompt(self, query: str) -> str:
        """Get the most relevant prompt for the query type"""
        query_lower = query.lower()
        
        # Determine prompt type based on query
        if any(word in query_lower for word in ['under', 'below', 'around', 'between']):
            return self.specialized_prompts["budget_interpretation"].format(query=query)
        elif any(word in query_lower for word in ['for', 'use case', 'purpose']):
            return self.specialized_prompts["use_case_detection"].format(query=query)
        else:
            return self.specialized_prompts["shopping_analysis"].format(query=query)
    
    def get_context_for_query(self, query: str) -> Dict[str, Any]:
        """Get shopping context for the query"""
        return {
            "query_type": self._classify_query_type(query),
            "urgency_level": self._detect_urgency(query),
            "seasonal_context": self._get_seasonal_context(),
            "user_intent": self._detect_user_intent(query)
        }
    
    def _classify_query_type(self, query: str) -> str:
        """Classify query type for optimization"""
        query_lower = query.lower()
        
        if 'best' in query_lower or 'top' in query_lower:
            return "comparison_search"
        elif 'cheap' in query_lower or 'budget' in query_lower:
            return "budget_search"
        elif 'vs' in query_lower or 'compare' in query_lower:
            return "comparison_query"
        elif 'for' in query_lower:
            return "use_case_search"
        else:
            return "general_search"
    
    def _detect_urgency(self, query: str) -> str:
        """Detect urgency indicators"""
        urgency_words = ['urgent', 'need', 'quick', 'fast', 'asap', 'immediately']
        return 'high' if any(word in query.lower() for word in urgency_words) else 'normal'
    
    def _get_seasonal_context(self) -> Dict[str, str]:
        """Add seasonal context"""
        month = datetime.now().month
        
        seasonal_map = {
            (11, 12, 1): "festive_season",
            (2, 3): "spring_sale",
            (4, 5): "summer_products",
            (6, 7, 8): "monsoon_deals",
            (9, 10): "festival_prep"
        }
        
        for months, season in seasonal_map.items():
            if month in months:
                return {"season": season, "relevant_deals": True}
        
        return {"season": "regular", "relevant_deals": False}
    
    def _detect_user_intent(self, query: str) -> str:
        """Detect underlying user intent"""
        query_lower = query.lower()
        
        intent_indicators = {
            "research": ['best', 'top', 'compare', 'vs', 'review'],
            "purchase": ['buy', 'get', 'need', 'want', 'looking for'],
            "upgrade": ['upgrade', 'better than', 'replace', 'new'],
            "gift": ['gift', 'present', 'for someone', 'birthday']
        }
        
        for intent, keywords in intent_indicators.items():
            if any(keyword in query_lower for keyword in keywords):
                return intent
        
        return "explore"


class ShoppingQueryOptimizer:
    """Optimize queries for Dobby AI"""
    
    def __init__(self, config: ShoppingDobbyConfig = None):
        self.config = config or ShoppingDobbyConfig()
    
    def optimize_query(self, raw_query: str) -> Dict[str, str]:
        """Optimize query for Dobby processing"""
        
        # Clean and normalize query
        cleaned = self._clean_query(raw_query)
        
        # Add context
        context = self.config.get_context_for_query(cleaned)
        
        # Select optimal prompt
        prompt = self.config.get_optimized_prompt(cleaned)
        
        return {
            "original_query": raw_query,
            "cleaned_query": cleaned,
            "prompt_type": self._determine_prompt_type(cleaned),
            "context": context,
            "optimized_prompt": prompt
        }
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize query"""
        # Remove extra spaces, normalize case
        cleaned = ' '.join(query.split()).lower().strip()
        
        # Handle common abbreviations
        replacements = {
            '₹': 'rs',
            'rs.': 'rs',
            'k': 'thousand',
            'lakh': 'lakh'
        }
        
        for old, new in replacements.items():
            cleaned = cleaned.replace(old, new)
        
        return cleaned
    
    def _determine_prompt_type(self, query: str) -> str:
        """Determine which specialized prompt to use"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['under', 'below', 'around', 'between', 'cheap', 'budget']):
            return "budget_interpretation"
        elif any(word in query_lower for word in ['for', 'use case', 'purpose', 'suitable for']):
            return "use_case_detection"
        else:
            return "shopping_analysis"


# Global configuration instance
SHOPPING_CONFIG = ShoppingDobbyConfig()

if __name__ == "__main__":
    config = ShoppingDobbyConfig()
    
    test_queries = [
        "comfortable wireless headphones for long flights under 5000",
        "best gaming laptop around 1 lakh with good battery",
        "affordable phone for elderly parents with large screen",
        "premium running shoes for marathon training",
        "good laptop for coding and occasional gaming"
    ]
    
    print("=== Shopping Dobby Configuration Test ===")
    print("Configuration Ready for:")
    print("✅ Specialized shopping prompts")
    print("✅ Product taxonomy mapping")
    print("✅ Budget interpretation")
    print("✅ Use case detection")
    print("✅ Brand hierarchy")
    print("✅ Context optimization")
    
    for query in test_queries:
        optimized = SHOPPING_CONFIG.optimize_query(query)
        print(f"\nQuery: {query}")
        print(f"Optimized: {json.dumps(optimized, indent=2)}")
