#!/usr/bin/env python3
"""
Test script to demonstrate GPT-5 logging during plan mode
This simulates plan mode activation to show the logging in action
"""

import os
import sys
import json
from pathlib import Path

# Add SuperClaude to path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for testing
os.environ["ENABLE_DUAL_PLANNING"] = "true"
os.environ["GPT5_LOGGING"] = "true"
os.environ["GPT5_VERBOSE_LOGGING"] = "true"
os.environ["GPT5_LOG_COLORS"] = "true"
os.environ["GPT5_MODEL"] = "gpt-5"
os.environ["GPT5_VERBOSITY"] = "medium"

# You need to set this to your actual API key for real testing
# os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"

def test_plan_mode_detection():
    """Test plan mode detection and logging"""
    print("\n" + "="*60)
    print("TESTING GPT-5 LOGGING IN PLAN MODE")
    print("="*60 + "\n")
    
    try:
        # Import the modules
        from SuperClaude.Hooks.plan_mode_hook import PlanModeHook
        from SuperClaude.Core.gpt5_logger import get_logger, print_session_summary
        
        # Initialize the logger
        logger = get_logger()
        logger.log_with_banner("🧪 TEST MODE - Simulating Plan Mode Activation 🧪")
        
        # Create a test context
        test_context = {
            'user_request': 'Create a REST API for user management with authentication',
            'initial_plan': {
                'steps': [
                    'Design API endpoints',
                    'Implement authentication',
                    'Create user CRUD operations'
                ],
                'considerations': [
                    'Security best practices',
                    'Rate limiting',
                    'Input validation'
                ]
            },
            'project_context': {
                'framework': 'FastAPI',
                'database': 'PostgreSQL',
                'auth_method': 'JWT'
            }
        }
        
        # Initialize the plan mode hook
        print("\n📋 Initializing Plan Mode Hook...")
        hook = PlanModeHook()
        
        # Simulate plan mode entry
        print("\n🚀 Simulating Plan Mode Entry...")
        
        # This will trigger all the logging
        enhanced_context = hook.on_plan_mode_enter(test_context)
        
        # Show results
        print("\n📊 Enhanced Context Results:")
        print("-" * 40)
        
        if enhanced_context.get('gpt5_enhancement'):
            print("✅ GPT-5 Enhancement Added")
            if 'error' in enhanced_context['gpt5_enhancement']:
                print(f"⚠️ Error: {enhanced_context['gpt5_enhancement']['error']}")
        else:
            print("❌ No GPT-5 Enhancement (API key may be missing)")
        
        if enhanced_context.get('consensus_points'):
            print(f"🤝 Consensus Points: {len(enhanced_context['consensus_points'])}")
        
        if enhanced_context.get('combined_plan'):
            print("📝 Combined Plan Created")
        
        # Print session summary
        print("\n")
        print_session_summary()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure you're running this from the SuperClaude_Framework directory")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def test_dual_planner():
    """Test the dual planner with logging"""
    print("\n" + "="*60)
    print("TESTING DUAL PLANNER WITH LOGGING")
    print("="*60 + "\n")
    
    try:
        from SuperClaude.Core.dual_planner import DualPlannerSync, PlanningContext
        from SuperClaude.Core.gpt5_logger import get_logger
        
        # Create planning context
        context = PlanningContext(
            user_request="Implement a caching system for our API",
            project_info={
                'language': 'Python',
                'framework': 'FastAPI',
                'requirements': ['Redis support', 'TTL management', 'Cache invalidation']
            },
            claude_plan={
                'steps': ['Setup Redis', 'Create cache decorator', 'Implement TTL']
            }
        )
        
        # Create dual planner
        planner = DualPlannerSync()
        
        # Execute planning
        print("🎯 Executing Dual Planning...")
        result = planner.create_enhanced_plan(context)
        
        print("\n📊 Planning Results:")
        print(f"Strategy Used: {result.get('strategy', 'unknown')}")
        print(f"Confidence: {result.get('confidence', 0):.2%}")
        
        # Get metrics
        metrics = planner.get_metrics()
        print("\n📈 Planner Metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

def check_log_files():
    """Check if log files are being created"""
    print("\n" + "="*60)
    print("CHECKING LOG FILES")
    print("="*60 + "\n")
    
    log_dir = Path.home() / ".claude" / "logs" / "gpt5"
    
    if log_dir.exists():
        log_files = list(log_dir.glob("*.log"))
        if log_files:
            print(f"✅ Found {len(log_files)} log file(s):")
            for log_file in log_files[-3:]:  # Show last 3 files
                print(f"  📄 {log_file.name}")
                print(f"     Size: {log_file.stat().st_size:,} bytes")
                
                # Show last few lines
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        print("     Last entry:")
                        print(f"     {lines[-1].strip()[:100]}...")
        else:
            print("❌ No log files found")
    else:
        print(f"❌ Log directory does not exist: {log_dir}")
        print("   It will be created when the logger is first used")

def main():
    """Main test function"""
    print("\n" + "🔬" * 30)
    print("GPT-5 INTEGRATION LOGGING TEST")
    print("🔬" * 30)
    
    # Check if API key is set
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key or api_key == "sk-your-api-key-here":
        print("\n⚠️  WARNING: No OpenAI API key detected!")
        print("   The logging will work but GPT-5 calls will fail.")
        print("   Set OPENAI_API_KEY environment variable for full testing.")
        print("   Example: export OPENAI_API_KEY=sk-your-actual-key")
    else:
        print(f"\n✅ API Key detected: ...{api_key[-8:]}")
    
    # Run tests
    test_plan_mode_detection()
    test_dual_planner()
    check_log_files()
    
    print("\n" + "="*60)
    print("✨ TEST COMPLETE ✨")
    print("="*60)
    print("\nThe logging system is now integrated and will track:")
    print("  🎯 Plan mode activations")
    print("  🤖 GPT-5 API calls")
    print("  🔀 Plan merging operations")
    print("  ⚡ Fallback events")
    print("  📊 Usage statistics and costs")
    print("\nLogs are saved to: ~/.claude/logs/gpt5/")

if __name__ == "__main__":
    main()