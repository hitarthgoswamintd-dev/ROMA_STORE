"""
ROMA Recursive Planning System
Implements recursive hierarchical planning for shopping queries
"""

import json
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Subtask:
    """Represents a subtask in the ROMA planning system"""
    id: str
    goal: str
    category: Optional[str] = None
    budget: Optional[int] = None
    constraints: List[str] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []


@dataclass
class ExecutionResult:
    """Result from executing a subtask"""
    subtask_id: str
    goal: str
    result: Any
    success: bool
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class ShoppingAtomizer:
    """Determines if query needs recursive planning"""
    
    def should_plan(self, query: str) -> bool:
        """Always plan for shopping queries"""
        return True
    
    def atomize(self, query: str) -> Dict[str, Any]:
        """Break down query into atomic components"""
        return {
            'needs_planning': True,
            'query_type': 'shopping',
            'complexity': self._assess_complexity(query)
        }
    
    def _assess_complexity(self, query: str) -> str:
        """Assess query complexity for planning"""
        query_lower = query.lower()
        
        # Count constraints
        constraints = 0
        constraint_keywords = [
            'under', 'below', 'cheap', 'budget', 'premium', 'expensive',
            'red', 'blue', 'black', 'white', 'green', 'yellow', 'pink',
            'nike', 'adidas', 'apple', 'samsung', 'hp', 'dell',
            'non-apple', 'not apple', 'excluding'
        ]
        
        for keyword in constraint_keywords:
            if keyword in query_lower:
                constraints += 1
        
        if constraints >= 3:
            return 'complex'
        elif constraints >= 1:
            return 'moderate'
        else:
            return 'simple'


class ShoppingPlanner:
    """Creates recursive plan for shopping queries"""
    
    def __init__(self):
        self.subtask_counter = 0
    
    def plan(self, original_query: str) -> List[Subtask]:
        """Generate subtasks for shopping query"""
        self.subtask_counter = 0
        return self._create_plan(original_query)
    
    def _create_plan(self, query: str) -> List[Subtask]:
        """Create hierarchical plan"""
        subtasks = []
        
        # Step 1: Analyze query
        subtasks.append(Subtask(
            id=self._next_id(),
            goal=f"Analyze shopping query: {query}",
            category="analysis"
        ))
        
        # Step 2: Extract constraints
        subtasks.append(Subtask(
            id=self._next_id(),
            goal="Extract product category and constraints from query",
            category="extraction"
        ))
        
        # Step 3: Determine budget range
        subtasks.append(Subtask(
            id=self._next_id(),
            goal="Determine appropriate budget range",
            category="budgeting"
        ))
        
        # Step 4: Search products
        subtasks.append(Subtask(
            id=self._next_id(),
            goal="Search for products matching criteria",
            category="search"
        ))
        
        # Step 5: Filter and rank
        subtasks.append(Subtask(
            id=self._next_id(),
            goal="Filter and rank products by relevance",
            category="ranking"
        ))
        
        # Step 6: Format results
        subtasks.append(Subtask(
            id=self._next_id(),
            goal="Format top 3 products for presentation",
            category="formatting"
        ))
        
        return subtasks
    
    def _next_id(self) -> str:
        self.subtask_counter += 1
        return f"ST{self.subtask_counter:02d}"


class ShoppingExecutor:
    """Executes subtasks using built-in logic"""
    
    def __init__(self):
        self.budget_analyzer = BudgetAnalyzer()
        self.product_db = self._create_product_db()
    
    def execute(self, subtask: Subtask) -> ExecutionResult:
        """Execute a specific subtask"""
        try:
            if subtask.category == "analysis":
                return self._execute_analysis(subtask)
            elif subtask.category == "extraction":
                return self._execute_extraction(subtask)
            elif subtask.category == "budgeting":
                return self._execute_budgeting(subtask)
            elif subtask.category == "search":
                return self._execute_search(subtask)
            elif subtask.category == "ranking":
                return self._execute_ranking(subtask)
            elif subtask.category == "formatting":
                return self._execute_formatting(subtask)
            else:
                return ExecutionResult(
                    subtask_id=subtask.id,
                    goal=subtask.goal,
                    result=None,
                    success=False,
                    metadata={'error': 'Unknown subtask category'}
                )
        except Exception as e:
            return ExecutionResult(
                subtask_id=subtask.id,
                goal=subtask.goal,
                result=None,
                success=False,
                metadata={'error': str(e)}
            )
    
    def _execute_analysis(self, subtask: Subtask) -> ExecutionResult:
        query = subtask.goal.replace("Analyze shopping query: ", "")
        analysis = self.budget_analyzer.analyze_budget(query)
        
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result=analysis,
            success=True,
            metadata={'analysis_complete': True}
        )
    
    def _execute_extraction(self, subtask: Subtask) -> ExecutionResult:
        # This would be handled by the main query processing
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result={'category': 'extracted', 'constraints': 'identified'},
            success=True
        )
    
    def _execute_budgeting(self, subtask: Subtask) -> ExecutionResult:
        # Budget determination handled by analyzer
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result={'budget_range': 'determined'},
            success=True
        )
    
    def _execute_search(self, subtask: Subtask) -> ExecutionResult:
        # Search would use the product database
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result={'search_complete': True, 'products_found': len(self.product_db)},
            success=True
        )
    
    def _execute_ranking(self, subtask: Subtask) -> ExecutionResult:
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result={'ranking_complete': True},
            success=True
        )
    
    def _execute_formatting(self, subtask: Subtask) -> ExecutionResult:
        return ExecutionResult(
            subtask_id=subtask.id,
            goal=subtask.goal,
            result={'formatting_complete': True},
            success=True
        )
    
    def _create_product_db(self):
        """Create embedded product database"""
        return [
            {
                "name": "Red Nike Air Max 270",
                "price": 2499,
                "rating": 4.5,
                "category": "apparel",
                "brand": "Nike",
                "color": "red"
            },
            {
                "name": "HP Pavilion 15",
                "price": 45999,
                "rating": 4.3,
                "category": "electronics",
                "brand": "HP",
                "color": "silver"
            },
            {
                "name": "Redmi Note 12 Pro",
                "price": 14999,
                "rating": 4.2,
                "category": "mobiles",
                "brand": "Redmi",
                "color": "blue"
            }
        ]


class ShoppingAggregator:
    """Aggregates results from subtask executions"""
    
    def aggregate(self, original_query: str, execution_results: List[ExecutionResult]) -> Dict[str, Any]:
        """Aggregate all subtask results into final response"""
        
        # Extract relevant results
        analysis_result = next((r for r in execution_results if r.goal.startswith("Analyze")), None)
        search_result = next((r for r in execution_results if r.goal.startswith("Search")), None)
        
        if not analysis_result or not search_result:
            return {
                'success': False,
                'error': 'Missing required execution results',
                'products': []
            }
        
        # Get analysis data
        analysis = analysis_result.result
        
        # Filter products based on analysis
        products = self._filter_products(analysis)
        
        return {
            'success': True,
            'query': original_query,
            'analysis': analysis,
            'products': products[:3],
            'total_found': len(products),
            'planning_complete': True
        }
    
    def _filter_products(self, analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter products based on analysis"""
        # This would use the actual product database
        # For now, return sample filtered products
        products = [
            {
                "name": "Red Nike Air Max 270",
                "price": 2499,
                "rating": 4.5,
                "image_url": "https://via.placeholder.com/300x200/ff0000/ffffff?text=Nike+Red",
                "description": "Comfortable running shoes with Air Max cushioning",
                "buy_link": "https://amazon.in/nike-red",
                "category": "apparel",
                "brand": "Nike",
                "color": "red",
                "platform": "Amazon"
            }
        ]
        
        # Filter based on analysis
        filtered = []
        for product in products:
            if analysis['category'] and product['category'] != analysis['category']:
                continue
            if analysis['max_budget'] and product['price'] > analysis['max_budget']:
                continue
            filtered.append(product)
        
        return filtered


class ROMAShoppingAgent:
    """Main ROMA agent that orchestrates the recursive planning"""
    
    def __init__(self):
        self.atomizer = ShoppingAtomizer()
        self.planner = ShoppingPlanner()
        self.executor = ShoppingExecutor()
        self.aggregator = ShoppingAggregator()
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """Process query through complete ROMA pipeline"""
        
        try:
            # Step 1: Atomize query
            atomization = self.atomizer.atomize(user_query)
            
            if not atomization['needs_planning']:
                return self._simple_search(user_query)
            
            # Step 2: Plan subtasks
            subtasks = self.planner.plan(user_query)
            
            # Step 3: Execute subtasks
            execution_results = []
            for subtask in subtasks:
                result = self.executor.execute(subtask)
                execution_results.append(result)
            
            # Step 4: Aggregate results
            final_result = self.aggregator.aggregate(user_query, execution_results)
            
            return final_result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'products': [],
                'planning_error': True
            }
    
    def _simple_search(self, query: str) -> Dict[str, Any]:
        """Fallback for simple queries"""
        return {
            'success': True,
            'query': query,
            'products': [],
            'total_found': 0,
            'planning_complete': False,
            'note': 'Used simple search instead of planning'
        }
