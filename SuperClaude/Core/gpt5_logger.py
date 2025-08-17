"""
GPT-5 Integration Logger for SuperClaude Framework
Provides comprehensive logging for plan mode and GPT-5 API calls
"""

import os
import sys
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from enum import Enum


class LogLevel(Enum):
    """Log levels with color codes"""
    DEBUG = ("DEBUG", "\033[36m", "🔍")      # Cyan
    INFO = ("INFO", "\033[32m", "ℹ️")        # Green
    WARNING = ("WARNING", "\033[33m", "⚠️")  # Yellow
    ERROR = ("ERROR", "\033[31m", "❌")      # Red
    SUCCESS = ("SUCCESS", "\033[92m", "✅")  # Bright Green
    GPT5_CALL = ("GPT5", "\033[95m", "🤖")   # Magenta
    PLAN_MODE = ("PLAN", "\033[94m", "📋")   # Blue
    MERGE = ("MERGE", "\033[96m", "🔄")      # Bright Cyan


class GPT5Logger:
    """
    Specialized logger for GPT-5 integration with SuperClaude.
    Provides color-coded console output and file logging.
    """
    
    def __init__(self, name: str = "GPT5Integration", log_dir: Optional[str] = None):
        """
        Initialize the GPT-5 logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files (defaults to ~/.claude/logs/)
        """
        self.name = name
        self.enabled = os.getenv("GPT5_LOGGING", "true").lower() == "true"
        self.verbose = os.getenv("GPT5_VERBOSE_LOGGING", "false").lower() == "true"
        self.console_colors = os.getenv("GPT5_LOG_COLORS", "true").lower() == "true"
        
        # Set up log directory
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path.home() / ".claude" / "logs" / "gpt5"
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create log file with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"gpt5_integration_{timestamp}.log"
        
        # Initialize Python logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Remove existing handlers
        self.logger.handlers.clear()
        
        # File handler - always logs everything
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler - with colors
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        console_handler.setFormatter(self._ColorFormatter(self.console_colors))
        self.logger.addHandler(console_handler)
        
        # Statistics tracking
        self.stats = {
            'plan_mode_activations': 0,
            'gpt5_api_calls': 0,
            'successful_merges': 0,
            'fallbacks': 0,
            'errors': 0,
            'total_tokens': 0,
            'total_cost': 0.0
        }
        
        # Log initialization
        self.log_with_banner("GPT-5 Integration Logger Initialized", LogLevel.SUCCESS)
        self.info(f"Log file: {self.log_file}")
    
    class _ColorFormatter(logging.Formatter):
        """Custom formatter with color support"""
        
        def __init__(self, use_colors: bool = True):
            super().__init__()
            self.use_colors = use_colors
            self.reset = "\033[0m"
        
        def format(self, record):
            if self.use_colors and hasattr(record, 'color'):
                # Add color codes
                return f"{record.color}{record.emoji} {record.getMessage()}{self.reset}"
            else:
                # Plain text
                return f"{record.levelname}: {record.getMessage()}"
    
    def log_with_banner(self, message: str, level: LogLevel = LogLevel.INFO):
        """Log a message with a visual banner"""
        if not self.enabled:
            return
        
        banner = "=" * 60
        self._log(level, banner)
        self._log(level, message)
        self._log(level, banner)
    
    def plan_mode_detected(self, context: Dict[str, Any]):
        """Log plan mode detection"""
        if not self.enabled:
            return
        
        self.stats['plan_mode_activations'] += 1
        
        self._log(LogLevel.PLAN_MODE, "🎯 PLAN MODE DETECTED! 🎯")
        self._log(LogLevel.PLAN_MODE, f"Context: {json.dumps(context, indent=2)[:500]}...")
        self._log(LogLevel.PLAN_MODE, f"Activation #{self.stats['plan_mode_activations']}")
        
        # Log to file with full context
        self.logger.debug(f"Full plan mode context: {json.dumps(context)}")
    
    def gpt5_api_call(self, model: str, request_type: str, tokens: Optional[int] = None):
        """Log GPT-5 API call"""
        if not self.enabled:
            return
        
        self.stats['gpt5_api_calls'] += 1
        
        self._log(LogLevel.GPT5_CALL, f"🚀 GPT-5 API CALL #{self.stats['gpt5_api_calls']} 🚀")
        self._log(LogLevel.GPT5_CALL, f"Model: {model}")
        self._log(LogLevel.GPT5_CALL, f"Request Type: {request_type}")
        
        if tokens:
            self.stats['total_tokens'] += tokens
            self._log(LogLevel.GPT5_CALL, f"Tokens: {tokens} (Total: {self.stats['total_tokens']})")
    
    def gpt5_response(self, success: bool, response_time: float, tokens_used: Dict[str, int]):
        """Log GPT-5 API response"""
        if not self.enabled:
            return
        
        if success:
            self._log(LogLevel.SUCCESS, f"✨ GPT-5 Response Received ✨")
            self._log(LogLevel.SUCCESS, f"Response Time: {response_time:.2f}s")
            self._log(LogLevel.SUCCESS, f"Tokens: Input={tokens_used.get('input', 0)}, "
                                       f"Output={tokens_used.get('output', 0)}, "
                                       f"Total={tokens_used.get('total', 0)}")
            
            # Calculate cost
            cost = self._calculate_cost(tokens_used)
            self.stats['total_cost'] += cost
            self._log(LogLevel.SUCCESS, f"Cost: ${cost:.4f} (Total: ${self.stats['total_cost']:.4f})")
        else:
            self.stats['errors'] += 1
            self._log(LogLevel.ERROR, f"⚠️ GPT-5 API Call Failed (Error #{self.stats['errors']})")
    
    def plan_merge(self, strategy: str, consensus_points: int, confidence: float):
        """Log plan merging operation"""
        if not self.enabled:
            return
        
        self.stats['successful_merges'] += 1
        
        self._log(LogLevel.MERGE, f"🔀 Plan Merge Operation 🔀")
        self._log(LogLevel.MERGE, f"Strategy: {strategy}")
        self._log(LogLevel.MERGE, f"Consensus Points: {consensus_points}")
        self._log(LogLevel.MERGE, f"Confidence: {confidence:.2%}")
        self._log(LogLevel.MERGE, f"Total Merges: {self.stats['successful_merges']}")
    
    def fallback_triggered(self, reason: str):
        """Log fallback to Claude-only planning"""
        if not self.enabled:
            return
        
        self.stats['fallbacks'] += 1
        
        self._log(LogLevel.WARNING, f"⚡ Fallback to Claude-Only Planning ⚡")
        self._log(LogLevel.WARNING, f"Reason: {reason}")
        self._log(LogLevel.WARNING, f"Total Fallbacks: {self.stats['fallbacks']}")
    
    def error(self, message: str, exception: Optional[Exception] = None):
        """Log an error"""
        if not self.enabled:
            return
        
        self.stats['errors'] += 1
        
        self._log(LogLevel.ERROR, f"Error: {message}")
        if exception:
            self._log(LogLevel.ERROR, f"Exception: {str(exception)}")
            self.logger.exception("Full exception details:")
    
    def info(self, message: str):
        """Log an info message"""
        if not self.enabled:
            return
        
        self._log(LogLevel.INFO, message)
    
    def debug(self, message: str):
        """Log a debug message"""
        if not self.enabled or not self.verbose:
            return
        
        self._log(LogLevel.DEBUG, message)
    
    def success(self, message: str):
        """Log a success message"""
        if not self.enabled:
            return
        
        self._log(LogLevel.SUCCESS, message)
    
    def warning(self, message: str):
        """Log a warning message"""
        if not self.enabled:
            return
        
        self._log(LogLevel.WARNING, message)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get current statistics"""
        return {
            **self.stats,
            'success_rate': (
                (self.stats['gpt5_api_calls'] - self.stats['errors']) / 
                max(self.stats['gpt5_api_calls'], 1) * 100
            ),
            'fallback_rate': (
                self.stats['fallbacks'] / 
                max(self.stats['plan_mode_activations'], 1) * 100
            ),
            'average_cost_per_call': (
                self.stats['total_cost'] / 
                max(self.stats['gpt5_api_calls'], 1)
            )
        }
    
    def print_summary(self):
        """Print a summary of the session"""
        if not self.enabled:
            return
        
        stats = self.get_statistics()
        
        self.log_with_banner("GPT-5 Integration Session Summary", LogLevel.SUCCESS)
        self._log(LogLevel.INFO, f"Plan Mode Activations: {stats['plan_mode_activations']}")
        self._log(LogLevel.INFO, f"GPT-5 API Calls: {stats['gpt5_api_calls']}")
        self._log(LogLevel.INFO, f"Successful Merges: {stats['successful_merges']}")
        self._log(LogLevel.INFO, f"Fallbacks: {stats['fallbacks']} ({stats['fallback_rate']:.1f}%)")
        self._log(LogLevel.INFO, f"Errors: {stats['errors']}")
        self._log(LogLevel.INFO, f"Success Rate: {stats['success_rate']:.1f}%")
        self._log(LogLevel.INFO, f"Total Tokens: {stats['total_tokens']:,}")
        self._log(LogLevel.INFO, f"Total Cost: ${stats['total_cost']:.4f}")
        self._log(LogLevel.INFO, f"Average Cost/Call: ${stats['average_cost_per_call']:.4f}")
        self.log_with_banner("End of Summary", LogLevel.SUCCESS)
    
    def _log(self, level: LogLevel, message: str):
        """Internal logging method"""
        level_name, color, emoji = level.value
        
        # Create a log record
        record = self.logger.makeRecord(
            self.logger.name,
            getattr(logging, level_name, logging.INFO),
            __file__,
            0,
            message,
            None,
            None
        )
        
        # Add color and emoji attributes
        record.color = color if self.console_colors else ""
        record.emoji = emoji
        
        # Log it
        self.logger.handle(record)
    
    def _calculate_cost(self, tokens: Dict[str, int]) -> float:
        """Calculate cost based on GPT-5 pricing"""
        # GPT-5 pricing: $1.25/million input, $10/million output
        input_cost = (tokens.get('input', 0) / 1_000_000) * 1.25
        output_cost = (tokens.get('output', 0) / 1_000_000) * 10.0
        return input_cost + output_cost
    
    def enable_verbose(self):
        """Enable verbose logging"""
        self.verbose = True
        self.logger.setLevel(logging.DEBUG)
        for handler in self.logger.handlers:
            handler.setLevel(logging.DEBUG)
    
    def disable_verbose(self):
        """Disable verbose logging"""
        self.verbose = False
        self.logger.setLevel(logging.INFO)
        for handler in self.logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                handler.setLevel(logging.INFO)


# Singleton instance for easy access
_logger_instance = None

def get_logger() -> GPT5Logger:
    """Get or create the singleton logger instance"""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = GPT5Logger()
    return _logger_instance


# Convenience functions
def log_plan_mode(context: Dict[str, Any]):
    """Log plan mode detection"""
    get_logger().plan_mode_detected(context)

def log_gpt5_call(model: str, request_type: str, tokens: Optional[int] = None):
    """Log GPT-5 API call"""
    get_logger().gpt5_api_call(model, request_type, tokens)

def log_gpt5_response(success: bool, response_time: float, tokens_used: Dict[str, int]):
    """Log GPT-5 API response"""
    get_logger().gpt5_response(success, response_time, tokens_used)

def log_merge(strategy: str, consensus_points: int, confidence: float):
    """Log plan merge operation"""
    get_logger().plan_merge(strategy, consensus_points, confidence)

def log_fallback(reason: str):
    """Log fallback to Claude-only"""
    get_logger().fallback_triggered(reason)

def print_session_summary():
    """Print session summary"""
    get_logger().print_summary()


# Export all public functions and classes
__all__ = [
    'GPT5Logger',
    'LogLevel',
    'get_logger',
    'log_plan_mode',
    'log_gpt5_call',
    'log_gpt5_response',
    'log_merge',
    'log_fallback',
    'print_session_summary'
]