import re
from typing import Dict, Optional
from .config import CATEGORY_KEYWORDS, BUDGET_KEYWORDS, BUDGET_RANGES


class BudgetAnalyzer:
    """Analyzes budget constraints from user shopping queries"""
    
    BUDGET_RANGES = BUDGET_RANGES
    CATEGORY_KEYWORDS = CATEGORY_KEYWORDS
    BUDGET_KEYWORDS = BUDGET_KEYWORDS
    
    def __init__(self):
        self.budget_patterns = [
            (re.compile(r'(?:under|below|less than|upto)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', re.IGNORECASE), 'under'),
            (re.compile(r'(?:around|about)\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*(?:\.\d+)?)', re.IGNORECASE), 'around'),
            (re.compile(r'between\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*)\s+and\s+(?:rs\.?|₹)?\s*(\d+(?:,\d+)*)', re.IGNORECASE), 'range'),
        ]
    
    def analyze_budget(self, query: str) -> Dict[str, Optional[int]]:
        """Extract budget and category from user query"""
        
        query_lower = query.lower().strip()
        
        category = self._detect_category(query_lower)
        budget_type = self._detect_budget_type(query_lower)
        specific_budget = self._extract_price(query_lower)
        
        if specific_budget:
            max_budget = specific_budget
        else:
            max_budget = self.BUDGET_RANGES.get(category, {}).get(budget_type, 50000)
        
        return {
            'category': category,
            'max_budget': max_budget,
            'budget_type': budget_type,
            'specific_budget': specific_budget,
            'original_query': query
        }
    
    def _detect_category(self, query: str) -> Optional[str]:
        """Detect product category from query using keyword matching"""
        
        if any(exclude in query for exclude in ['non-apple', 'not apple', 'excluding apple']):
            if any(keyword in query for keyword in ['laptop', 'computer', 'macbook']):
                return 'electronics'
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            if any(keyword in query for keyword in keywords):
                return category
        
        return None
    
    def _detect_budget_type(self, query: str) -> str:
        """Detect budget type from query keywords"""
        
        if self._extract_price(query):
            return 'specific'
        
        for budget_key, keywords in self.BUDGET_KEYWORDS.items():
            if any(keyword in query for keyword in keywords):
                return budget_key
        
        if any(term in query for term in ['cheap', 'budget', 'under']):
            return 'low'
        
        return 'low'
    
    def _extract_price(self, query: str) -> Optional[int]:
        """Extract specific price mentions from query with budget keywords"""
        
        budget_keywords = ['under', 'below', 'less than', 'upto', 'around', 'about', 'between', 'max', 'maximum']
        has_budget_keyword = any(kw in query.lower() for kw in budget_keywords)
        
        if not has_budget_keyword:
            return None
        
        for pattern, pattern_type in self.budget_patterns:
            match = pattern.search(query)
            if match:
                if pattern_type == 'range':
                    price_str = match.group(2).replace(',', '')
                else:
                    price_str = match.group(1).replace(',', '')
                
                try:
                    price = float(price_str)
                    
                    if 'k' in query.lower() and price < 100:
                        price *= 1000
                    
                    return int(price)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def get_category_suggestions(self, query: str) -> list:
        """Get category suggestions for ambiguous queries"""
        
        query_lower = query.lower()
        suggestions = []
        
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                suggestions.append((category, score))
        
        # Sort by relevance score
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [cat for cat, score in suggestions]


if __name__ == "__main__":
    analyzer = BudgetAnalyzer()
    
    test_queries = [
        "red running shoes under budget",
        "non-Apple laptops under 50000",
        "cheap mobile phones",
        "premium headphones",
        "blue denim jacket under 2000"
    ]
    
    for query in test_queries:
        result = analyzer.analyze_budget(query)
        print(f"Query: {query}")
        print(f"Analysis: {result}")
        print("-" * 50)
