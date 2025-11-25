#!/usr/bin/env python3
"""
Real-time monitoring script for data aggregation process.
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

RESEARCH_DATA_DIR = Path('/home/claude-user/ai-consults-platform/00-pivot/research_data')
LOG_FILE = RESEARCH_DATA_DIR / 'population.log'

def clear_screen():
    """Clear terminal screen."""
    os.system('clear' if os.name != 'nt' else 'cls')

def read_log_tail(lines=50):
    """Read last N lines from log file."""
    if not LOG_FILE.exists():
        return []

    try:
        with open(LOG_FILE, 'r') as f:
            return f.readlines()[-lines:]
    except:
        return []

def parse_log_stats(log_lines):
    """Parse statistics from log lines."""
    stats = {
        'projects_processed': 0,
        'embeddings_created': 0,
        'errors': 0,
        'warnings': 0,
        'last_project': 'N/A',
        'status': 'Unknown'
    }

    for line in log_lines:
        if 'Processing project' in line:
            try:
                # Extract project number and name
                parts = line.split('Processing project')[1].strip().split(':')
                if len(parts) >= 2:
                    count_part = parts[0].strip()
                    if '/' in count_part:
                        current = int(count_part.split('/')[0])
                        stats['projects_processed'] = current
                    stats['last_project'] = parts[1].strip()
            except:
                pass

        elif 'Stored document' in line:
            stats['embeddings_created'] += 1

        elif 'ERROR' in line:
            stats['errors'] += 1

        elif 'WARNING' in line or 'WARN' in line:
            stats['warnings'] += 1

        elif 'Database population completed successfully' in line:
            stats['status'] = 'Completed'

        elif 'Fatal error' in line:
            stats['status'] = 'Failed'

    if stats['projects_processed'] > 0:
        stats['status'] = 'Running'

    return stats

def monitor():
    """Monitor aggregation process in real-time."""
    print("Starting real-time monitoring...")
    print("Press Ctrl+C to exit")
    time.sleep(2)

    try:
        while True:
            clear_screen()

            # Header
            print("=" * 100)
            print("InfraFlow AI - Data Aggregation Monitor".center(100))
            print("=" * 100)
            print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(100))
            print("=" * 100)

            # Check if log file exists
            if not LOG_FILE.exists():
                print("\n⏳ Waiting for aggregation to start...")
                print(f"\nLog file not found: {LOG_FILE}")
                print("\nTo start aggregation, run:")
                print("   python aggregate_and_populate.py")
                time.sleep(5)
                continue

            # Read and parse log
            log_lines = read_log_tail(100)
            stats = parse_log_stats(log_lines)

            # Display statistics
            print("\n📊 STATISTICS")
            print("-" * 100)
            print(f"Status:             {stats['status']}")
            print(f"Projects Processed: {stats['projects_processed']}")
            print(f"Embeddings Created: {stats['embeddings_created']}")
            print(f"Warnings:           {stats['warnings']}")
            print(f"Errors:             {stats['errors']}")
            print(f"Last Project:       {stats['last_project']}")

            # Display recent log entries
            print("\n📝 RECENT LOG ENTRIES (Last 20 lines)")
            print("-" * 100)
            recent_lines = log_lines[-20:]
            for line in recent_lines:
                # Color code by level
                line = line.strip()
                if not line:
                    continue

                if 'ERROR' in line:
                    print(f"🔴 {line[:95]}")
                elif 'WARNING' in line or 'WARN' in line:
                    print(f"🟡 {line[:95]}")
                elif 'INFO' in line:
                    print(f"🔵 {line[:95]}")
                else:
                    print(f"   {line[:95]}")

            # Footer
            print("-" * 100)
            print("Press Ctrl+C to exit monitoring".center(100))
            print("=" * 100)

            # Check if completed
            if stats['status'] == 'Completed':
                print("\n✨ Aggregation completed successfully!")
                print("\nView full report at:")
                print(f"   {RESEARCH_DATA_DIR / 'POPULATION_REPORT.md'}")
                break

            elif stats['status'] == 'Failed':
                print("\n❌ Aggregation failed!")
                print("\nCheck log file for details:")
                print(f"   {LOG_FILE}")
                break

            # Refresh every 3 seconds
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(monitor())
