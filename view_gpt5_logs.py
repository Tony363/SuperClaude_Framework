#!/usr/bin/env python3
"""
GPT-5 Log Viewer Utility
Interactive tool to view and analyze GPT-5 integration logs
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import argparse


class LogViewer:
    """View and analyze GPT-5 integration logs"""
    
    def __init__(self, log_dir: Optional[Path] = None):
        """Initialize the log viewer"""
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path.home() / ".claude" / "logs" / "gpt5"
        
        self.current_file = None
        self.logs = []
    
    def list_log_files(self) -> List[Path]:
        """List all available log files"""
        if not self.log_dir.exists():
            print(f"❌ Log directory does not exist: {self.log_dir}")
            return []
        
        log_files = sorted(self.log_dir.glob("*.log"), key=lambda x: x.stat().st_mtime, reverse=True)
        return log_files
    
    def display_file_list(self):
        """Display list of log files"""
        files = self.list_log_files()
        
        if not files:
            print("No log files found.")
            return
        
        print("\n📁 Available Log Files:")
        print("=" * 60)
        
        for i, file in enumerate(files, 1):
            stat = file.stat()
            mod_time = datetime.fromtimestamp(stat.st_mtime)
            size_kb = stat.st_size / 1024
            
            print(f"{i:2}. {file.name}")
            print(f"    Modified: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"    Size: {size_kb:.2f} KB")
            print()
    
    def load_log_file(self, file_path: Path) -> bool:
        """Load a log file for analysis"""
        try:
            with open(file_path, 'r') as f:
                self.logs = f.readlines()
            self.current_file = file_path
            return True
        except Exception as e:
            print(f"❌ Error loading file: {e}")
            return False
    
    def display_summary(self):
        """Display summary of current log file"""
        if not self.logs:
            print("No log file loaded.")
            return
        
        print(f"\n📊 Log Summary for: {self.current_file.name}")
        print("=" * 60)
        
        # Count different log levels
        levels = {
            'INFO': 0,
            'DEBUG': 0,
            'WARNING': 0,
            'ERROR': 0,
            'SUCCESS': 0,
            'GPT5': 0,
            'PLAN': 0,
            'MERGE': 0
        }
        
        api_calls = 0
        plan_mode_activations = 0
        errors = 0
        
        for line in self.logs:
            for level in levels:
                if f"- {level} -" in line:
                    levels[level] += 1
            
            if "GPT-5 API CALL" in line:
                api_calls += 1
            if "PLAN MODE DETECTED" in line:
                plan_mode_activations += 1
            if "ERROR" in line:
                errors += 1
        
        print(f"Total Lines: {len(self.logs)}")
        print(f"Plan Mode Activations: {plan_mode_activations}")
        print(f"GPT-5 API Calls: {api_calls}")
        print(f"Errors: {errors}")
        print("\nLog Levels:")
        for level, count in levels.items():
            if count > 0:
                print(f"  {level}: {count}")
    
    def display_recent_entries(self, n: int = 20):
        """Display recent log entries"""
        if not self.logs:
            print("No log file loaded.")
            return
        
        print(f"\n📜 Last {n} Log Entries:")
        print("=" * 60)
        
        # Remove ANSI color codes for cleaner display
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        
        for line in self.logs[-n:]:
            clean_line = ansi_escape.sub('', line).strip()
            
            # Highlight important entries
            if "PLAN MODE DETECTED" in clean_line:
                print(f"🎯 {clean_line}")
            elif "GPT-5 API CALL" in clean_line:
                print(f"🤖 {clean_line}")
            elif "ERROR" in clean_line:
                print(f"❌ {clean_line}")
            elif "SUCCESS" in clean_line:
                print(f"✅ {clean_line}")
            elif "MERGE" in clean_line:
                print(f"🔀 {clean_line}")
            else:
                print(f"   {clean_line[:120]}...")
    
    def search_logs(self, pattern: str):
        """Search logs for a pattern"""
        if not self.logs:
            print("No log file loaded.")
            return
        
        print(f"\n🔍 Search Results for: '{pattern}'")
        print("=" * 60)
        
        matches = []
        for i, line in enumerate(self.logs):
            if pattern.lower() in line.lower():
                matches.append((i + 1, line.strip()))
        
        if matches:
            print(f"Found {len(matches)} matches:")
            for line_num, line in matches[:20]:  # Show first 20 matches
                print(f"  Line {line_num}: {line[:100]}...")
        else:
            print("No matches found.")
    
    def extract_statistics(self):
        """Extract and display statistics from logs"""
        if not self.logs:
            print("No log file loaded.")
            return
        
        print("\n📈 Statistics:")
        print("=" * 60)
        
        # Extract token usage
        total_tokens = 0
        total_cost = 0.0
        response_times = []
        
        for line in self.logs:
            # Look for token counts
            if "Total Tokens:" in line:
                match = re.search(r'Total Tokens: ([\d,]+)', line)
                if match:
                    tokens = int(match.group(1).replace(',', ''))
                    total_tokens += tokens
            
            # Look for costs
            if "Total Cost:" in line:
                match = re.search(r'Total Cost: \$([\d.]+)', line)
                if match:
                    cost = float(match.group(1))
                    total_cost = cost  # This is usually cumulative
            
            # Look for response times
            if "responded in" in line:
                match = re.search(r'responded in ([\d.]+)s', line)
                if match:
                    response_times.append(float(match.group(1)))
        
        if total_tokens:
            print(f"Total Tokens Used: {total_tokens:,}")
        
        if total_cost:
            print(f"Total Cost: ${total_cost:.4f}")
        
        if response_times:
            avg_response = sum(response_times) / len(response_times)
            print(f"Average Response Time: {avg_response:.2f}s")
            print(f"Min Response Time: {min(response_times):.2f}s")
            print(f"Max Response Time: {max(response_times):.2f}s")
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("\n🔬 GPT-5 Log Viewer - Interactive Mode")
        print("=" * 60)
        
        while True:
            print("\nOptions:")
            print("1. List log files")
            print("2. Load most recent log")
            print("3. Show summary")
            print("4. Show recent entries")
            print("5. Search logs")
            print("6. Show statistics")
            print("7. Exit")
            
            choice = input("\nSelect option (1-7): ").strip()
            
            if choice == '1':
                self.display_file_list()
            
            elif choice == '2':
                files = self.list_log_files()
                if files:
                    if self.load_log_file(files[0]):
                        print(f"✅ Loaded: {files[0].name}")
                    else:
                        print("❌ Failed to load file")
                else:
                    print("No log files available")
            
            elif choice == '3':
                self.display_summary()
            
            elif choice == '4':
                n = input("How many entries? (default: 20): ").strip()
                n = int(n) if n.isdigit() else 20
                self.display_recent_entries(n)
            
            elif choice == '5':
                pattern = input("Enter search pattern: ").strip()
                if pattern:
                    self.search_logs(pattern)
            
            elif choice == '6':
                self.extract_statistics()
            
            elif choice == '7':
                print("👋 Goodbye!")
                break
            
            else:
                print("Invalid option. Please try again.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="View and analyze GPT-5 integration logs")
    parser.add_argument('--dir', type=str, help='Log directory path')
    parser.add_argument('--latest', action='store_true', help='Show latest log entries')
    parser.add_argument('--summary', action='store_true', help='Show summary of latest log')
    parser.add_argument('--search', type=str, help='Search for pattern in logs')
    parser.add_argument('--stats', action='store_true', help='Show statistics')
    
    args = parser.parse_args()
    
    viewer = LogViewer(args.dir if args.dir else None)
    
    if args.latest or args.summary or args.search or args.stats:
        # Command-line mode
        files = viewer.list_log_files()
        if files:
            viewer.load_log_file(files[0])
            
            if args.summary:
                viewer.display_summary()
            
            if args.latest:
                viewer.display_recent_entries()
            
            if args.search:
                viewer.search_logs(args.search)
            
            if args.stats:
                viewer.extract_statistics()
        else:
            print("No log files found")
    else:
        # Interactive mode
        viewer.interactive_mode()


if __name__ == "__main__":
    main()