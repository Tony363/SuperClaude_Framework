"""
Plan Mode Hook - Integrates GPT-5 for enhanced planning in Claude Code
"""

import os
import json
import asyncio
import time
from typing import Dict, Optional, List, Any
from datetime import datetime

# Import the logger
try:
    from ..Core.gpt5_logger import (
        get_logger, log_plan_mode, log_gpt5_call, 
        log_gpt5_response, log_merge, log_fallback
    )
    LOGGING_AVAILABLE = True
except ImportError:
    LOGGING_AVAILABLE = False
    print("Warning: GPT-5 logger not available")


class PlanModeHook:
    """
    Hook to intercept Claude Code's plan mode and enhance it with GPT-5 insights.
    This hook activates when plan mode is detected and provides dual-model planning.
    """
    
    def __init__(self):
        """Initialize the plan mode hook with configuration"""
        self.enabled = os.getenv("ENABLE_DUAL_PLANNING", "true").lower() == "true"
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("GPT5_MODEL", "gpt-5")
        self.verbosity = os.getenv("GPT5_VERBOSITY", "medium")
        self.client = None
        
        # Initialize logger if available
        if LOGGING_AVAILABLE:
            self.logger = get_logger()
            self.logger.info("🚀 Initializing Plan Mode Hook for GPT-5 Integration")
            self.logger.info(f"Model: {self.model}, Verbosity: {self.verbosity}")
        else:
            self.logger = None
        
        if self.enabled and self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
                if self.logger:
                    self.logger.success("✅ OpenAI client initialized successfully")
                    self.logger.info(f"API Key: ...{self.api_key[-8:]}")
            except ImportError:
                error_msg = "OpenAI package not installed. Run: pip install openai"
                print(f"Warning: {error_msg}")
                if self.logger:
                    self.logger.error(error_msg)
                self.enabled = False
            except Exception as e:
                error_msg = f"Could not initialize OpenAI client: {e}"
                print(f"Warning: {error_msg}")
                if self.logger:
                    self.logger.error(error_msg, e)
                self.enabled = False
        else:
            if self.logger:
                if not self.enabled:
                    self.logger.warning("Dual planning is disabled")
                if not self.api_key:
                    self.logger.warning("No OpenAI API key found")
    
    def on_plan_mode_enter(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Called when Claude Code enters plan mode.
        Enhances the planning process with GPT-5 insights.
        
        Args:
            context: Current planning context including user request and initial analysis
            
        Returns:
            Enhanced context with GPT-5 insights merged
        """
        # Log plan mode detection
        if self.logger and LOGGING_AVAILABLE:
            log_plan_mode(context)
            self.logger.log_with_banner("🎯 PLAN MODE ACTIVATED - GPT-5 ENHANCEMENT STARTING 🎯")
        
        if not self.enabled or not self.client:
            if self.logger:
                reason = "Dual planning disabled" if not self.enabled else "No OpenAI client"
                log_fallback(reason)
            return context
        
        try:
            # Extract key information from context
            user_request = context.get('user_request', '')
            initial_plan = context.get('initial_plan', {})
            project_context = context.get('project_context', {})
            
            # Get GPT-5's planning insights
            gpt5_insights = self.get_gpt5_insights(
                user_request, 
                initial_plan, 
                project_context
            )
            
            # Merge GPT-5 insights with Claude's plan
            enhanced_context = self.merge_plans(context, gpt5_insights)
            
            # Add metadata about the enhancement
            enhanced_context['planning_metadata'] = {
                'dual_model': True,
                'gpt5_model': self.model,
                'timestamp': datetime.now().isoformat(),
                'confidence_score': self.calculate_confidence(context, gpt5_insights)
            }
            
            return enhanced_context
            
        except Exception as e:
            # On error, return original context with error info
            context['gpt5_error'] = str(e)
            return context
    
    def get_gpt5_insights(self, request: str, initial_plan: Dict, project_context: Dict) -> Dict[str, Any]:
        """
        Get planning insights from GPT-5.
        
        Args:
            request: User's original request
            initial_plan: Claude's initial planning
            project_context: Current project information
            
        Returns:
            GPT-5's planning insights and suggestions
        """
        if not self.client:
            return {}
        
        try:
            # Build the prompt for GPT-5
            system_prompt = """You are GPT-5, an advanced AI assistant specializing in code planning and architecture.
You are enhancing Claude Code's planning capabilities. Provide detailed, actionable planning insights that:
1. Identify potential challenges and edge cases
2. Suggest optimal implementation strategies
3. Recommend best practices and design patterns
4. Consider performance and scalability
5. Highlight security considerations"""
            
            user_prompt = f"""Task: {request}

Initial Planning Context:
{json.dumps(initial_plan, indent=2)}

Project Context:
{json.dumps(project_context, indent=2)}

Please provide enhanced planning insights, alternative approaches, and critical considerations."""
            
            # Log API call
            if self.logger and LOGGING_AVAILABLE:
                log_gpt5_call(self.model, "planning_insights")
                self.logger.info(f"Request length: {len(user_prompt)} characters")
            
            # Track timing
            start_time = time.time()
            
            # Call GPT-5 API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Parse and structure the response
            gpt5_content = response.choices[0].message.content
            
            # Log successful response
            if self.logger and LOGGING_AVAILABLE:
                tokens_used = {
                    'input': response.usage.prompt_tokens,
                    'output': response.usage.completion_tokens,
                    'total': response.usage.total_tokens
                }
                log_gpt5_response(True, response_time, tokens_used)
                self.logger.success(f"✨ GPT-5 responded in {response_time:.2f}s")
                self.logger.info(f"Response length: {len(gpt5_content)} characters")
            
            return {
                'raw_insights': gpt5_content,
                'model_used': self.model,
                'usage': {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'structured_insights': self.parse_gpt5_response(gpt5_content)
            }
            
        except Exception as e:
            # Log error
            if self.logger and LOGGING_AVAILABLE:
                log_gpt5_response(False, 0, {})
                self.logger.error(f"GPT-5 API call failed: {str(e)}", e)
                log_fallback(f"GPT-5 API error: {str(e)}")
            
            return {
                'error': str(e),
                'fallback': True
            }
    
    def parse_gpt5_response(self, content: str) -> Dict[str, Any]:
        """
        Parse GPT-5's response into structured insights.
        
        Args:
            content: Raw response from GPT-5
            
        Returns:
            Structured insights dictionary
        """
        # Basic parsing - can be enhanced with more sophisticated NLP
        insights = {
            'key_considerations': [],
            'implementation_steps': [],
            'potential_issues': [],
            'best_practices': [],
            'alternative_approaches': []
        }
        
        # Simple keyword-based extraction (can be improved)
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if 'consideration' in line.lower() or 'consider' in line.lower():
                current_section = 'key_considerations'
            elif 'implementation' in line.lower() or 'step' in line.lower():
                current_section = 'implementation_steps'
            elif 'issue' in line.lower() or 'challenge' in line.lower():
                current_section = 'potential_issues'
            elif 'best practice' in line.lower() or 'recommend' in line.lower():
                current_section = 'best_practices'
            elif 'alternative' in line.lower() or 'approach' in line.lower():
                current_section = 'alternative_approaches'
            elif current_section and line.startswith(('-', '*', '•', '1', '2', '3')):
                # Add bullet points to current section
                insights[current_section].append(line.lstrip('-*•123456789. '))
        
        return insights
    
    def merge_plans(self, claude_context: Dict, gpt5_insights: Dict) -> Dict[str, Any]:
        """
        Intelligently merge Claude's plan with GPT-5's insights.
        
        Args:
            claude_context: Original context from Claude
            gpt5_insights: Insights from GPT-5
            
        Returns:
            Merged and enhanced context
        """
        if self.logger and LOGGING_AVAILABLE:
            self.logger.info("🔀 Starting plan merge operation...")
        
        enhanced_context = claude_context.copy()
        
        # Add GPT-5 insights as a separate section
        enhanced_context['gpt5_enhancement'] = gpt5_insights
        
        # If both models agree on certain points, highlight them
        consensus_points = []
        if 'structured_insights' in gpt5_insights:
            consensus_points = self.find_consensus(
                claude_context.get('plan_points', []),
                gpt5_insights['structured_insights']
            )
            enhanced_context['consensus_points'] = consensus_points
        
        # Create a combined action plan
        enhanced_context['combined_plan'] = self.create_combined_plan(
            claude_context,
            gpt5_insights
        )
        
        # Log merge results
        if self.logger and LOGGING_AVAILABLE:
            confidence = self.calculate_confidence(claude_context, gpt5_insights)
            log_merge("dual_model", len(consensus_points), confidence)
            self.logger.success(f"✅ Plan merge completed with {len(consensus_points)} consensus points")
        
        return enhanced_context
    
    def find_consensus(self, claude_points: List, gpt5_insights: Dict) -> List[str]:
        """
        Find points where both models agree.
        
        Args:
            claude_points: Planning points from Claude
            gpt5_insights: Structured insights from GPT-5
            
        Returns:
            List of consensus points
        """
        consensus = []
        
        # Flatten GPT-5 insights
        gpt5_points = []
        for category, points in gpt5_insights.items():
            if isinstance(points, list):
                gpt5_points.extend(points)
        
        # Simple similarity check (can be enhanced with NLP)
        for claude_point in claude_points:
            for gpt5_point in gpt5_points:
                if any(word in gpt5_point.lower() for word in claude_point.lower().split()):
                    consensus.append(f"Both models agree: {claude_point}")
                    break
        
        return consensus
    
    def create_combined_plan(self, claude_context: Dict, gpt5_insights: Dict) -> Dict[str, Any]:
        """
        Create a unified plan combining both models' insights.
        
        Args:
            claude_context: Original context from Claude
            gpt5_insights: Insights from GPT-5
            
        Returns:
            Combined planning structure
        """
        combined = {
            'primary_steps': claude_context.get('steps', []),
            'gpt5_enhancements': [],
            'additional_considerations': [],
            'risk_mitigation': []
        }
        
        if 'structured_insights' in gpt5_insights:
            insights = gpt5_insights['structured_insights']
            
            # Add GPT-5's unique contributions
            if insights.get('implementation_steps'):
                combined['gpt5_enhancements'] = insights['implementation_steps']
            
            if insights.get('potential_issues'):
                combined['risk_mitigation'] = insights['potential_issues']
            
            if insights.get('best_practices'):
                combined['additional_considerations'] = insights['best_practices']
        
        return combined
    
    def calculate_confidence(self, claude_context: Dict, gpt5_insights: Dict) -> float:
        """
        Calculate confidence score based on model agreement.
        
        Args:
            claude_context: Original context from Claude
            gpt5_insights: Insights from GPT-5
            
        Returns:
            Confidence score between 0 and 1
        """
        if gpt5_insights.get('error') or gpt5_insights.get('fallback'):
            # If GPT-5 failed, return lower confidence
            return 0.6
        
        # Base confidence
        confidence = 0.7
        
        # Increase confidence if GPT-5 provided structured insights
        if gpt5_insights.get('structured_insights'):
            confidence += 0.1
        
        # Increase confidence based on consensus points
        consensus_points = claude_context.get('consensus_points', [])
        if len(consensus_points) > 3:
            confidence += 0.2
        elif len(consensus_points) > 0:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def on_plan_mode_exit(self, context: Dict[str, Any]) -> None:
        """
        Called when exiting plan mode.
        Can be used for cleanup or logging.
        
        Args:
            context: Final planning context
        """
        if self.enabled:
            # Log planning session if needed
            if context.get('planning_metadata', {}).get('dual_model'):
                usage = context.get('gpt5_enhancement', {}).get('usage', {})
                if usage:
                    print(f"GPT-5 Planning Session - Tokens used: {usage.get('total_tokens', 0)}")


# Export the hook class
__all__ = ['PlanModeHook']