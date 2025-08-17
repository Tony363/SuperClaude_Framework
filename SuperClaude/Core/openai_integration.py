"""
OpenAI GPT-5 Integration for SuperClaude Framework
Advanced integration with OpenAI's GPT-5 models for enhanced planning and code generation.
"""

import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class GPT5Model(Enum):
    """Available GPT-5 model variants"""
    FULL = "gpt-5"
    MINI = "gpt-5-mini"
    NANO = "gpt-5-nano"
    CHAT = "gpt-5-chat"


class VerbosityLevel(Enum):
    """GPT-5 verbosity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MINIMAL = "minimal"  # New in GPT-5 for minimal reasoning


class GPT5Integration:
    """
    Main integration class for OpenAI GPT-5 models.
    Provides async and sync interfaces for planning, code generation, and analysis.
    """
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-5"):
        """
        Initialize GPT-5 integration.
        
        Args:
            api_key: OpenAI API key (defaults to env var OPENAI_API_KEY)
            model: GPT-5 model variant to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.organization = os.getenv("OPENAI_ORG_ID")
        self.verbosity = VerbosityLevel(os.getenv("GPT5_VERBOSITY", "medium"))
        
        # Initialize clients
        self.client = None
        self.async_client = None
        self._initialize_clients()
        
        # Configuration
        self.max_retries = 3
        self.timeout = 30
        self.temperature = 0.7
        self.max_tokens = 4000
        
        # Usage tracking
        self.usage_stats = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'errors': 0
        }
    
    def _initialize_clients(self):
        """Initialize OpenAI clients with error handling"""
        if not self.api_key:
            print("Warning: No OpenAI API key found. GPT-5 integration disabled.")
            return
        
        try:
            from openai import OpenAI, AsyncOpenAI
            
            # Initialize synchronous client
            self.client = OpenAI(
                api_key=self.api_key,
                organization=self.organization
            )
            
            # Initialize async client
            self.async_client = AsyncOpenAI(
                api_key=self.api_key,
                organization=self.organization
            )
            
        except ImportError:
            print("Error: OpenAI package not installed. Run: pip install openai>=1.40.0")
        except Exception as e:
            print(f"Error initializing OpenAI clients: {e}")
    
    async def get_planning_insights(self, 
                                   request: str, 
                                   context: Dict[str, Any],
                                   verbosity: Optional[VerbosityLevel] = None) -> Dict[str, Any]:
        """
        Get asynchronous planning insights from GPT-5.
        
        Args:
            request: User's planning request
            context: Current context and project information
            verbosity: Override default verbosity level
            
        Returns:
            Dictionary containing GPT-5's planning insights
        """
        if not self.async_client:
            return self._error_response("OpenAI client not initialized")
        
        verbosity = verbosity or self.verbosity
        
        try:
            # Build messages for GPT-5
            messages = self._build_planning_messages(request, context)
            
            # Call GPT-5 API with special parameters
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                # GPT-5 specific parameters
                extra_body={
                    "verbosity": verbosity.value
                }
            )
            
            # Process and structure the response
            return self._process_planning_response(response, request)
            
        except Exception as e:
            self.usage_stats['errors'] += 1
            return self._error_response(str(e))
    
    def get_planning_insights_sync(self, 
                                  request: str, 
                                  context: Dict[str, Any],
                                  verbosity: Optional[VerbosityLevel] = None) -> Dict[str, Any]:
        """
        Synchronous version of get_planning_insights.
        
        Args:
            request: User's planning request
            context: Current context and project information
            verbosity: Override default verbosity level
            
        Returns:
            Dictionary containing GPT-5's planning insights
        """
        if not self.client:
            return self._error_response("OpenAI client not initialized")
        
        verbosity = verbosity or self.verbosity
        
        try:
            messages = self._build_planning_messages(request, context)
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                extra_body={
                    "verbosity": verbosity.value
                }
            )
            
            return self._process_planning_response(response, request)
            
        except Exception as e:
            self.usage_stats['errors'] += 1
            return self._error_response(str(e))
    
    async def analyze_code(self, 
                          code: str, 
                          analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze code using GPT-5's advanced capabilities.
        
        Args:
            code: Code to analyze
            analysis_type: Type of analysis (comprehensive, security, performance, quality)
            
        Returns:
            Detailed code analysis from GPT-5
        """
        if not self.async_client:
            return self._error_response("OpenAI client not initialized")
        
        try:
            system_prompt = self._get_analysis_prompt(analysis_type)
            
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Analyze this code:\n\n```\n{code}\n```"}
                ],
                temperature=0.3,  # Lower temperature for analysis
                max_tokens=3000
            )
            
            return self._process_analysis_response(response, analysis_type)
            
        except Exception as e:
            self.usage_stats['errors'] += 1
            return self._error_response(str(e))
    
    async def generate_code(self, 
                           specification: str, 
                           language: str = "python",
                           style_guide: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Generate code using GPT-5's superior coding capabilities.
        
        Args:
            specification: Code specification or requirements
            language: Programming language
            style_guide: Optional style guidelines
            
        Returns:
            Generated code with explanations
        """
        if not self.async_client:
            return self._error_response("OpenAI client not initialized")
        
        try:
            prompt = self._build_code_generation_prompt(specification, language, style_guide)
            
            response = await self.async_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are GPT-5, expert at generating high-quality, production-ready code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=4000,
                extra_body={
                    "verbosity": "high"  # Detailed code generation
                }
            )
            
            return self._process_code_response(response, language)
            
        except Exception as e:
            self.usage_stats['errors'] += 1
            return self._error_response(str(e))
    
    def _build_planning_messages(self, request: str, context: Dict) -> List[Dict[str, str]]:
        """Build message array for planning requests"""
        system_prompt = """You are GPT-5, the most advanced AI for code planning and architecture.
Your strengths:
- 74.9% accuracy on SWE-bench Verified
- 88% on Aider polyglot
- Superior tool calling and chaining capabilities
- Advanced reasoning with minimal hallucination

Provide comprehensive planning that includes:
1. Step-by-step implementation strategy
2. Potential challenges and solutions
3. Performance and scalability considerations
4. Security best practices
5. Testing strategy
6. Alternative approaches with trade-offs"""
        
        user_prompt = f"""Planning Request: {request}

Context:
{json.dumps(context, indent=2)}

Please provide detailed planning insights with your advanced capabilities."""
        
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    
    def _get_analysis_prompt(self, analysis_type: str) -> str:
        """Get appropriate system prompt for code analysis"""
        prompts = {
            "comprehensive": """Perform comprehensive code analysis covering:
- Code quality and maintainability
- Performance characteristics
- Security vulnerabilities
- Best practices compliance
- Potential bugs and issues
- Improvement suggestions""",
            
            "security": """Focus on security analysis:
- Vulnerability detection (OWASP Top 10)
- Input validation issues
- Authentication/authorization flaws
- Data exposure risks
- Injection vulnerabilities
- Cryptographic weaknesses""",
            
            "performance": """Analyze performance characteristics:
- Time complexity analysis
- Space complexity
- Bottlenecks and inefficiencies
- Caching opportunities
- Database query optimization
- Scaling considerations""",
            
            "quality": """Evaluate code quality:
- Clean code principles
- SOLID principles compliance
- Design pattern usage
- Code duplication
- Readability and maintainability
- Testing coverage suggestions"""
        }
        
        return prompts.get(analysis_type, prompts["comprehensive"])
    
    def _build_code_generation_prompt(self, spec: str, language: str, style_guide: Optional[Dict]) -> str:
        """Build prompt for code generation"""
        prompt = f"""Generate {language} code for the following specification:

{spec}

Requirements:
- Production-ready code with error handling
- Well-commented and documented
- Following best practices for {language}
- Include necessary imports/dependencies
- Add basic unit tests if applicable"""
        
        if style_guide:
            prompt += f"\n\nStyle Guidelines:\n{json.dumps(style_guide, indent=2)}"
        
        return prompt
    
    def _process_planning_response(self, response: Any, request: str) -> Dict[str, Any]:
        """Process and structure planning response from GPT-5"""
        try:
            content = response.choices[0].message.content
            
            # Update usage statistics
            self._update_usage_stats(response.usage)
            
            return {
                'success': True,
                'request': request,
                'model': self.model,
                'timestamp': datetime.now().isoformat(),
                'insights': {
                    'raw': content,
                    'structured': self._parse_planning_content(content)
                },
                'usage': {
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens,
                    'estimated_cost': self._calculate_cost(response.usage)
                },
                'metadata': {
                    'verbosity': self.verbosity.value,
                    'temperature': self.temperature,
                    'model_version': 'gpt-5-2025-08'
                }
            }
        except Exception as e:
            return self._error_response(f"Error processing response: {e}")
    
    def _process_analysis_response(self, response: Any, analysis_type: str) -> Dict[str, Any]:
        """Process code analysis response"""
        try:
            content = response.choices[0].message.content
            self._update_usage_stats(response.usage)
            
            return {
                'success': True,
                'analysis_type': analysis_type,
                'timestamp': datetime.now().isoformat(),
                'analysis': self._parse_analysis_content(content),
                'raw_output': content,
                'usage': {
                    'tokens': response.usage.total_tokens,
                    'cost': self._calculate_cost(response.usage)
                }
            }
        except Exception as e:
            return self._error_response(f"Error processing analysis: {e}")
    
    def _process_code_response(self, response: Any, language: str) -> Dict[str, Any]:
        """Process code generation response"""
        try:
            content = response.choices[0].message.content
            self._update_usage_stats(response.usage)
            
            # Extract code blocks
            code_blocks = self._extract_code_blocks(content)
            
            return {
                'success': True,
                'language': language,
                'timestamp': datetime.now().isoformat(),
                'code': code_blocks,
                'explanation': self._extract_explanation(content),
                'usage': {
                    'tokens': response.usage.total_tokens,
                    'cost': self._calculate_cost(response.usage)
                }
            }
        except Exception as e:
            return self._error_response(f"Error processing code: {e}")
    
    def _parse_planning_content(self, content: str) -> Dict[str, List[str]]:
        """Parse planning content into structured format"""
        structured = {
            'steps': [],
            'challenges': [],
            'best_practices': [],
            'alternatives': [],
            'considerations': []
        }
        
        lines = content.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            lower_line = line.lower()
            if any(word in lower_line for word in ['step', 'implementation', 'process']):
                current_section = 'steps'
            elif any(word in lower_line for word in ['challenge', 'issue', 'problem']):
                current_section = 'challenges'
            elif any(word in lower_line for word in ['best practice', 'recommendation']):
                current_section = 'best_practices'
            elif any(word in lower_line for word in ['alternative', 'option', 'approach']):
                current_section = 'alternatives'
            elif any(word in lower_line for word in ['consideration', 'note', 'important']):
                current_section = 'considerations'
            
            # Add content to current section
            if current_section and line.startswith(('-', '*', '•', '1', '2', '3')):
                structured[current_section].append(line.lstrip('-*•1234567890. '))
        
        return structured
    
    def _parse_analysis_content(self, content: str) -> Dict[str, Any]:
        """Parse analysis content into categories"""
        return {
            'summary': self._extract_summary(content),
            'issues': self._extract_issues(content),
            'suggestions': self._extract_suggestions(content),
            'metrics': self._extract_metrics(content)
        }
    
    def _extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks from content"""
        import re
        code_blocks = []
        
        # Find all code blocks with optional language specification
        pattern = r'```(\w+)?\n(.*?)\n```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        for lang, code in matches:
            code_blocks.append({
                'language': lang or 'plain',
                'code': code.strip()
            })
        
        return code_blocks
    
    def _extract_explanation(self, content: str) -> str:
        """Extract explanation text excluding code blocks"""
        import re
        # Remove code blocks
        cleaned = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        return cleaned.strip()
    
    def _extract_summary(self, content: str) -> str:
        """Extract summary from analysis content"""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if 'summary' in line.lower():
                # Return next few lines as summary
                return ' '.join(lines[i+1:min(i+4, len(lines))])
        return lines[0] if lines else ""
    
    def _extract_issues(self, content: str) -> List[str]:
        """Extract issues from analysis content"""
        issues = []
        lines = content.split('\n')
        
        for line in lines:
            if any(word in line.lower() for word in ['issue', 'problem', 'error', 'bug', 'vulnerability']):
                issues.append(line.strip())
        
        return issues
    
    def _extract_suggestions(self, content: str) -> List[str]:
        """Extract suggestions from analysis content"""
        suggestions = []
        lines = content.split('\n')
        
        for line in lines:
            if any(word in line.lower() for word in ['suggest', 'recommend', 'consider', 'should', 'could']):
                suggestions.append(line.strip())
        
        return suggestions
    
    def _extract_metrics(self, content: str) -> Dict[str, Any]:
        """Extract metrics from analysis content"""
        import re
        metrics = {}
        
        # Look for common metrics patterns
        patterns = {
            'complexity': r'complexity[:\s]+(\d+)',
            'lines': r'lines[:\s]+(\d+)',
            'functions': r'functions[:\s]+(\d+)',
            'coverage': r'coverage[:\s]+([\d.]+)%'
        }
        
        for metric, pattern in patterns.items():
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                metrics[metric] = match.group(1)
        
        return metrics
    
    def _update_usage_stats(self, usage: Any):
        """Update internal usage statistics"""
        self.usage_stats['total_requests'] += 1
        self.usage_stats['total_tokens'] += usage.total_tokens
        self.usage_stats['total_cost'] += self._calculate_cost(usage)
    
    def _calculate_cost(self, usage: Any) -> float:
        """
        Calculate cost based on GPT-5 pricing.
        Pricing: $1.25/million input tokens, $10/million output tokens
        """
        input_cost = (usage.prompt_tokens / 1_000_000) * 1.25
        output_cost = (usage.completion_tokens / 1_000_000) * 10.0
        return round(input_cost + output_cost, 4)
    
    def _error_response(self, error_message: str) -> Dict[str, Any]:
        """Generate standardized error response"""
        return {
            'success': False,
            'error': error_message,
            'timestamp': datetime.now().isoformat(),
            'fallback': True,
            'model': self.model
        }
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Get usage statistics report"""
        return {
            'total_requests': self.usage_stats['total_requests'],
            'total_tokens': self.usage_stats['total_tokens'],
            'total_cost': f"${self.usage_stats['total_cost']:.2f}",
            'error_rate': f"{(self.usage_stats['errors'] / max(self.usage_stats['total_requests'], 1)) * 100:.1f}%",
            'average_tokens_per_request': self.usage_stats['total_tokens'] // max(self.usage_stats['total_requests'], 1)
        }
    
    def switch_model(self, model: Union[str, GPT5Model]):
        """
        Switch to a different GPT-5 model variant.
        
        Args:
            model: Model name or GPT5Model enum
        """
        if isinstance(model, GPT5Model):
            self.model = model.value
        else:
            self.model = model
    
    def set_verbosity(self, level: Union[str, VerbosityLevel]):
        """
        Set verbosity level for GPT-5 responses.
        
        Args:
            level: Verbosity level
        """
        if isinstance(level, VerbosityLevel):
            self.verbosity = level
        else:
            self.verbosity = VerbosityLevel(level)


# Export main class and enums
__all__ = ['GPT5Integration', 'GPT5Model', 'VerbosityLevel']