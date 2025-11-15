"""
Centralized configuration for ROMA Shopping Agent
"""

# Category keywords for product classification
CATEGORY_KEYWORDS = {
    'apparel': [
        'shoes', 'clothes', 't-shirt', 'shirt', 'pants', 'trousers', 'jeans',
        'dress', 'jacket', 'coat', 'footwear', 'sneakers', 'boots', 'sandals',
        'sweater', 'hoodie', 'joggers', 'shorts', 'skirt', 'blouse'
    ],
    'mobiles': [
        'phone', 'smartphone', 'mobile', 'iphone', 'android', 'cellphone',
        'redmi', 'samsung', 'realme', 'vivo', 'oppo', 'oneplus', 'nokia',
        'moto', 'motorola', 'poco', 'nothing', 'google pixel'
    ],
    'electronics': [
        'laptop', 'computer', 'pc', 'notebook', 'macbook', 'thinkpad',
        'tv', 'television', 'smart tv', 'led tv', '4k tv',
        'camera', 'dslr', 'mirrorless', 'headphones', 'earphones',
        'speaker', 'soundbar', 'tablet', 'ipad', 'monitor', 'keyboard',
        'mouse', 'printer', 'scanner', 'projector', 'gaming console'
    ]
}

# Budget keywords for price tier detection
BUDGET_KEYWORDS = {
    'low': [
        'cheap', 'budget', 'affordable', 'low cost', 'economical', 'inexpensive',
        'under budget', 'low price', 'economy', 'basic', 'entry level'
    ],
    'medium': [
        'mid-range', 'reasonable', 'moderate', 'mid priced', 'standard',
        'average', 'decent', 'fair price', 'competitive', 'value'
    ],
    'high': [
        'premium', 'expensive', 'high-end', 'luxury', 'top', 'best',
        'flagship', 'professional', 'pro', 'ultimate', 'elite'
    ]
}

# Default budget ranges by category
BUDGET_RANGES = {
    'apparel': {'low': 3000, 'medium': 8000, 'high': 20000},
    'mobiles': {'low': 15000, 'medium': 35000, 'high': 70000},
    'electronics': {'low': 50000, 'medium': 100000, 'high': 250000}
}

# Color keywords for product matching
COLOR_KEYWORDS = [
    'red', 'blue', 'black', 'white', 'green', 'yellow', 'pink', 'purple',
    'orange', 'silver', 'gold', 'navy', 'beige', 'brown', 'gray', 'maroon',
    'cyan', 'magenta', 'violet', 'indigo', 'turquoise', 'khaki'
]

# Scoring weights for product ranking
SCORING_WEIGHTS = {
    'keyword_match': 2,
    'color_match': 3,
    'brand_match': 2,
    'price_relevance_under': 2,
    'price_relevance_over': -5,
    'rating_multiplier': 1.5,
    'category_match': 1
}

# Input validation constraints
INPUT_CONSTRAINTS = {
    'min_query_length': 2,
    'max_query_length': 500,
    'rate_limit_per_minute': 10,
    'rate_limit_per_hour': 50,
    'rate_limit_per_day': 200
}

# API configuration
API_CONFIG = {
    'default_results_limit': 3,
    'max_results_limit': 10,
    'timeout_seconds': 30
}
