"""
Dual-Model Planning Orchestrator for SuperClaude Framework
Combines Claude and GPT-5 planning capabilities for enhanced results.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

# Import the OpenAI integration
try:
    from .openai_integration import GPT5Integration, GPT5Model, VerbosityLevel
except ImportError:
    # Fallback if module not found
    GPT5Integration = None
    GPT5Model = None
    VerbosityLevel = None

# Import the logger
try:
    from .gpt5_logger import get_logger, log_merge, log_fallback
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False


@dataclass
class PlanningContext:
    """Context for planning operations"""
    user_request: str
    project_info: Dict[str, Any]
    claude_plan: Optional[Dict] = None
    gpt5_plan: Optional[Dict] = None
    timestamp: str = ""
    session_id: str = ""
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class PlanningStrategy(Enum):
    """Planning strategy options"""
    CLAUDE_ONLY = "claude_only"
    GPT5_ONLY = "gpt5_only"
    DUAL_MODEL = "dual_model"
    CONSENSUS = "consensus"
    COMPLEMENTARY = "complementary"


class DualPlanner:
    """
    Orchestrates planning between Claude and GPT-5 models.
    Provides intelligent merging and conflict resolution.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the dual planner with configuration.
        
        Args:
            config_path: Path to configuration file (optional)
        """
        self.config = self._load_config(config_path)
        self.enabled = os.getenv("ENABLE_DUAL_PLANNING", "true").lower() == "true"
        self.strategy = PlanningStrategy(
            os.getenv("PLANNING_STRATEGY", "dual_model")
        )
        
        # Initialize logger if available
        self.logger = None
        if LOGGING_AVAILABLE:
            self.logger = get_logger()
            self.logger.info("🎨 Initializing Dual Planner")
            self.logger.info(f"Strategy: {self.strategy.value}")
            self.logger.info(f"Enabled: {self.enabled}")
        
        # Initialize GPT-5 integration if available
        self.gpt5 = None
        if GPT5Integration and self.enabled:
            try:
                self.gpt5 = GPT5Integration(
                    api_key=os.getenv("OPENAI_API_KEY"),
                    model=os.getenv("GPT5_MODEL", "gpt-5")
                )
                if self.logger:
                    self.logger.success("✅ GPT-5 Integration initialized in Dual Planner")
            except Exception as e:
                print(f"Warning: Could not initialize GPT-5 integration: {e}")
                if self.logger:
                    self.logger.error(f"GPT-5 integration failed: {e}")
                self.enabled = False
        
        # Planning metrics
        self.metrics = {
            'total_plans': 0,
            'dual_plans': 0,
            'consensus_achieved': 0,
            'fallback_used': 0,
            'average_confidence': 0.0
        }
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load configuration from file or defaults"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Default configuration
        return {
            'merge_strategy': 'intelligent',
            'confidence_threshold': 0.7,
            'consensus_weight': 0.8,
            'timeout': 30,
            'cache_enabled': True,
            'cache_ttl': 3600
        }
    
    async def create_enhanced_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """
        Create an enhanced plan using the configured strategy.
        
        Args:
            context: Planning context with request and project info
            
        Returns:
            Enhanced planning result with merged insights
        """
        self.metrics['total_plans'] += 1
        
        if self.logger:
            self.logger.log_with_banner(f"🎯 DUAL PLANNER ACTIVATED - Strategy: {self.strategy.value}")
            self.logger.info(f"Request: {context.user_request[:100]}...")
        
        # Check if dual planning is enabled
        if not self.enabled or not self.gpt5:
            if self.logger:
                reason = "Dual planning disabled" if not self.enabled else "No GPT-5 client"
                log_fallback(reason)
            return await self._claude_only_plan(context)
        
        # Log strategy selection
        if self.logger:
            self.logger.info(f"📍 Executing strategy: {self.strategy.value}")
        
        # Execute based on strategy
        if self.strategy == PlanningStrategy.CLAUDE_ONLY:
            return await self._claude_only_plan(context)
        elif self.strategy == PlanningStrategy.GPT5_ONLY:
            return await self._gpt5_only_plan(context)
        elif self.strategy == PlanningStrategy.DUAL_MODEL:
            return await self._dual_model_plan(context)
        elif self.strategy == PlanningStrategy.CONSENSUS:
            return await self._consensus_plan(context)
        elif self.strategy == PlanningStrategy.COMPLEMENTARY:
            return await self._complementary_plan(context)
        else:
            return await self._claude_only_plan(context)
    
    async def _claude_only_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """Claude-only planning (baseline)"""
        return {
            'strategy': 'claude_only',
            'plan': context.claude_plan or {},
            'confidence': 0.75,
            'timestamp': context.timestamp
        }
    
    async def _gpt5_only_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """GPT-5 only planning"""
        if not self.gpt5:
            self.metrics['fallback_used'] += 1
            return await self._claude_only_plan(context)
        
        try:
            gpt5_result = await self.gpt5.get_planning_insights(
                context.user_request,
                context.project_info
            )
            
            if gpt5_result.get('success'):
                return {
                    'strategy': 'gpt5_only',
                    'plan': gpt5_result,
                    'confidence': 0.8,
                    'timestamp': context.timestamp
                }
            else:
                self.metrics['fallback_used'] += 1
                return await self._claude_only_plan(context)
                
        except Exception as e:
            print(f"GPT-5 planning failed: {e}")
            self.metrics['fallback_used'] += 1
            return await self._claude_only_plan(context)
    
    async def _dual_model_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """Dual-model planning with intelligent merging"""
        self.metrics['dual_plans'] += 1
        
        # Get GPT-5 insights
        gpt5_result = None
        if self.gpt5:
            try:
                gpt5_result = await self.gpt5.get_planning_insights(
                    context.user_request,
                    {'claude_plan': context.claude_plan, **context.project_info}
                )
            except Exception as e:
                print(f"GPT-5 planning error: {e}")
                self.metrics['fallback_used'] += 1
        
        # Merge plans intelligently
        merged_plan = self._merge_plans(
            context.claude_plan or {},
            gpt5_result or {}
        )
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            context.claude_plan,
            gpt5_result
        )
        
        self.metrics['average_confidence'] = (
            (self.metrics['average_confidence'] * (self.metrics['dual_plans'] - 1) + confidence) /
            self.metrics['dual_plans']
        )
        
        return {
            'strategy': 'dual_model',
            'claude_plan': context.claude_plan,
            'gpt5_plan': gpt5_result,
            'merged_plan': merged_plan,
            'confidence': confidence,
            'consensus_points': self._find_consensus(context.claude_plan, gpt5_result),
            'timestamp': context.timestamp
        }
    
    async def _consensus_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """Planning that emphasizes consensus between models"""
        # Get dual model plan first
        dual_result = await self._dual_model_plan(context)
        
        # Extract and emphasize consensus points
        consensus_points = dual_result.get('consensus_points', [])
        
        if len(consensus_points) > 3:
            self.metrics['consensus_achieved'] += 1
        
        # Build consensus-focused plan
        consensus_plan = {
            'primary_actions': consensus_points,
            'claude_unique': self._get_unique_points(
                context.claude_plan,
                consensus_points
            ),
            'gpt5_unique': self._get_unique_points(
                dual_result.get('gpt5_plan', {}),
                consensus_points
            )
        }
        
        return {
            'strategy': 'consensus',
            'plan': consensus_plan,
            'consensus_strength': len(consensus_points),
            'confidence': min(0.9, 0.6 + len(consensus_points) * 0.05),
            'full_analysis': dual_result,
            'timestamp': context.timestamp
        }
    
    async def _complementary_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """Planning that leverages complementary strengths"""
        # Get dual model plan
        dual_result = await self._dual_model_plan(context)
        
        # Identify complementary aspects
        complementary = {
            'claude_strengths': {
                'context_awareness': context.claude_plan.get('context_analysis', {}),
                'safety_considerations': context.claude_plan.get('safety', {}),
                'user_alignment': context.claude_plan.get('user_focus', {})
            },
            'gpt5_strengths': {
                'code_generation': dual_result.get('gpt5_plan', {}).get('code_suggestions', {}),
                'performance_optimization': dual_result.get('gpt5_plan', {}).get('performance', {}),
                'tool_chaining': dual_result.get('gpt5_plan', {}).get('tool_sequence', {})
            }
        }
        
        # Combine complementary strengths
        combined_plan = self._combine_complementary(
            context.claude_plan,
            dual_result.get('gpt5_plan', {}),
            complementary
        )
        
        return {
            'strategy': 'complementary',
            'plan': combined_plan,
            'complementary_analysis': complementary,
            'confidence': dual_result.get('confidence', 0.75),
            'timestamp': context.timestamp
        }
    
    def _merge_plans(self, claude_plan: Dict, gpt5_plan: Dict) -> Dict[str, Any]:
        """
        Intelligently merge plans from both models.
        
        Args:
            claude_plan: Planning from Claude
            gpt5_plan: Planning from GPT-5
            
        Returns:
            Merged planning structure
        """
        merged = {
            'steps': [],
            'considerations': [],
            'risks': [],
            'alternatives': [],
            'tools_needed': [],
            'estimated_complexity': 'medium'
        }
        
        # Merge steps
        claude_steps = claude_plan.get('steps', [])
        gpt5_steps = gpt5_plan.get('insights', {}).get('structured', {}).get('steps', [])
        merged['steps'] = self._merge_lists(claude_steps, gpt5_steps)
        
        # Merge considerations
        claude_considerations = claude_plan.get('considerations', [])
        gpt5_considerations = gpt5_plan.get('insights', {}).get('structured', {}).get('considerations', [])
        merged['considerations'] = self._merge_lists(claude_considerations, gpt5_considerations)
        
        # Merge risks
        claude_risks = claude_plan.get('risks', [])
        gpt5_risks = gpt5_plan.get('insights', {}).get('structured', {}).get('challenges', [])
        merged['risks'] = self._merge_lists(claude_risks, gpt5_risks)
        
        # Merge alternatives
        claude_alts = claude_plan.get('alternatives', [])
        gpt5_alts = gpt5_plan.get('insights', {}).get('structured', {}).get('alternatives', [])
        merged['alternatives'] = self._merge_lists(claude_alts, gpt5_alts)
        
        # Estimate complexity based on both models
        merged['estimated_complexity'] = self._estimate_complexity(merged)
        
        return merged
    
    def _merge_lists(self, list1: List, list2: List) -> List:
        """Merge two lists, removing duplicates while preserving order"""
        seen = set()
        merged = []
        
        for item in list1 + list2:
            # Simple string comparison for deduplication
            item_str = str(item).lower().strip()
            if item_str not in seen:
                seen.add(item_str)
                merged.append(item)
        
        return merged
    
    def _find_consensus(self, claude_plan: Optional[Dict], gpt5_plan: Optional[Dict]) -> List[str]:
        """
        Find consensus points between both models.
        
        Args:
            claude_plan: Claude's planning
            gpt5_plan: GPT-5's planning
            
        Returns:
            List of consensus points
        """
        if not claude_plan or not gpt5_plan:
            return []
        
        consensus = []
        
        # Extract all points from both plans
        claude_points = self._extract_all_points(claude_plan)
        gpt5_points = self._extract_all_points(gpt5_plan)
        
        # Find similar points (simple similarity check)
        for c_point in claude_points:
            for g_point in gpt5_points:
                if self._are_similar(c_point, g_point):
                    consensus.append(f"Consensus: {c_point}")
                    break
        
        return consensus
    
    def _extract_all_points(self, plan: Dict) -> List[str]:
        """Extract all planning points from a plan structure"""
        points = []
        
        # Handle different plan structures
        if isinstance(plan, dict):
            for key, value in plan.items():
                if isinstance(value, list):
                    points.extend([str(v) for v in value])
                elif isinstance(value, dict):
                    points.extend(self._extract_all_points(value))
                elif isinstance(value, str) and len(value) > 10:
                    points.append(value)
        
        return points
    
    def _are_similar(self, text1: str, text2: str) -> bool:
        """
        Check if two text points are similar.
        Simple implementation - can be enhanced with NLP.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            True if texts are similar
        """
        # Convert to lowercase and split into words
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        # Calculate Jaccard similarity
        if not words1 or not words2:
            return False
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        similarity = len(intersection) / len(union)
        
        return similarity > 0.3  # 30% similarity threshold
    
    def _get_unique_points(self, plan: Dict, consensus_points: List[str]) -> List[str]:
        """Get points unique to a plan (not in consensus)"""
        all_points = self._extract_all_points(plan)
        consensus_text = ' '.join(consensus_points).lower()
        
        unique = []
        for point in all_points:
            if point.lower() not in consensus_text:
                unique.append(point)
        
        return unique[:5]  # Limit to top 5 unique points
    
    def _combine_complementary(self, claude_plan: Dict, gpt5_plan: Dict, complementary: Dict) -> Dict:
        """Combine plans based on complementary strengths"""
        combined = {
            'context_and_safety': complementary['claude_strengths'],
            'implementation_and_optimization': complementary['gpt5_strengths'],
            'unified_approach': {
                'planning': claude_plan.get('steps', []),
                'implementation': gpt5_plan.get('insights', {}).get('structured', {}).get('implementation_steps', []),
                'validation': self._create_validation_steps(claude_plan, gpt5_plan)
            }
        }
        
        return combined
    
    def _create_validation_steps(self, claude_plan: Dict, gpt5_plan: Dict) -> List[str]:
        """Create validation steps based on both plans"""
        validation = []
        
        # Add testing suggestions from both models
        if 'testing' in str(claude_plan):
            validation.append("Execute Claude's testing strategy")
        
        if gpt5_plan and 'test' in str(gpt5_plan).lower():
            validation.append("Apply GPT-5's testing recommendations")
        
        # Add standard validation steps
        validation.extend([
            "Verify implementation against requirements",
            "Run automated tests",
            "Check performance metrics",
            "Validate security considerations"
        ])
        
        return validation
    
    def _calculate_confidence(self, claude_plan: Optional[Dict], gpt5_plan: Optional[Dict]) -> float:
        """
        Calculate confidence score for the merged plan.
        
        Args:
            claude_plan: Claude's plan
            gpt5_plan: GPT-5's plan
            
        Returns:
            Confidence score between 0 and 1
        """
        base_confidence = 0.7
        
        # Increase if both models provided plans
        if claude_plan and gpt5_plan:
            base_confidence += 0.1
        
        # Increase based on GPT-5 success
        if gpt5_plan and gpt5_plan.get('success'):
            base_confidence += 0.1
        
        # Increase based on consensus
        consensus = self._find_consensus(claude_plan, gpt5_plan)
        if len(consensus) > 5:
            base_confidence += 0.1
        elif len(consensus) > 2:
            base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    def _estimate_complexity(self, merged_plan: Dict) -> str:
        """Estimate complexity based on merged plan"""
        total_items = (
            len(merged_plan.get('steps', [])) +
            len(merged_plan.get('considerations', [])) +
            len(merged_plan.get('risks', []))
        )
        
        if total_items > 20:
            return 'high'
        elif total_items > 10:
            return 'medium'
        else:
            return 'low'
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get planning metrics"""
        return {
            'total_plans': self.metrics['total_plans'],
            'dual_plans': self.metrics['dual_plans'],
            'consensus_rate': f"{(self.metrics['consensus_achieved'] / max(self.metrics['dual_plans'], 1)) * 100:.1f}%",
            'fallback_rate': f"{(self.metrics['fallback_used'] / max(self.metrics['total_plans'], 1)) * 100:.1f}%",
            'average_confidence': f"{self.metrics['average_confidence']:.2f}"
        }
    
    def reset_metrics(self):
        """Reset planning metrics"""
        self.metrics = {
            'total_plans': 0,
            'dual_plans': 0,
            'consensus_achieved': 0,
            'fallback_used': 0,
            'average_confidence': 0.0
        }


# Synchronous wrapper for easier integration
class DualPlannerSync:
    """Synchronous wrapper for DualPlanner"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.planner = DualPlanner(config_path)
    
    def create_enhanced_plan(self, context: PlanningContext) -> Dict[str, Any]:
        """Synchronous version of create_enhanced_plan"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.planner.create_enhanced_plan(context)
            )
        finally:
            loop.close()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get planning metrics"""
        return self.planner.get_metrics()
    
    def reset_metrics(self):
        """Reset planning metrics"""
        self.planner.reset_metrics()


# Export main classes
__all__ = ['DualPlanner', 'DualPlannerSync', 'PlanningContext', 'PlanningStrategy']