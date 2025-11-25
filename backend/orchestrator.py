#!/usr/bin/env python3
"""
InfraFlow AI - Data Aggregation Orchestrator
Coordinates the entire data aggregation and population pipeline.
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

RESEARCH_DATA_DIR = Path('/home/claude-user/ai-consults-platform/00-pivot/research_data')
BACKEND_DIR = Path('/home/claude-user/ai-consults-platform/00-pivot/backend')

def print_header(title):
    """Print formatted header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")

def run_command(command, description):
    """Run a command and return success status."""
    print(f"▶ {description}...")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✅ {description} completed")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Error: {e.stderr}")
        return False, e.stderr

def check_prerequisites():
    """Check if all prerequisites are met."""
    print_header("Checking Prerequisites")

    checks = []

    # Check Python version
    if sys.version_info >= (3, 8):
        print("✅ Python version: 3.8+")
        checks.append(True)
    else:
        print("❌ Python version too old. Need 3.8+")
        checks.append(False)

    # Check required directories
    if RESEARCH_DATA_DIR.exists():
        print(f"✅ Research data directory exists: {RESEARCH_DATA_DIR}")
        checks.append(True)
    else:
        print(f"⚠️  Research data directory not found, creating: {RESEARCH_DATA_DIR}")
        RESEARCH_DATA_DIR.mkdir(parents=True, exist_ok=True)
        checks.append(True)

    # Check required Python packages
    required_packages = ['psycopg2', 'openai', 'pinecone', 'dotenv']
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ Package installed: {package}")
            checks.append(True)
        except ImportError:
            print(f"❌ Package not installed: {package}")
            print(f"   Install with: pip install {package}")
            checks.append(False)

    return all(checks)

def test_connections():
    """Test database and API connections."""
    print_header("Testing Connections")

    success, output = run_command(
        f"python3 {BACKEND_DIR / 'test_connections.py'}",
        "Testing database and API connections"
    )

    return success

def check_research_status():
    """Check research data status."""
    print_header("Checking Research Data Status")

    success, output = run_command(
        f"python3 {BACKEND_DIR / 'check_research_status.py'}",
        "Checking research data files"
    )

    print(output)
    return success

def run_aggregation():
    """Run the main aggregation script."""
    print_header("Running Data Aggregation")

    print("Starting aggregation process...")
    print("This may take a while depending on the amount of data.\n")

    success, output = run_command(
        f"python3 {BACKEND_DIR / 'aggregate_and_populate.py'}",
        "Data aggregation and population"
    )

    if success:
        print("\n✨ Aggregation completed successfully!")
    else:
        print("\n❌ Aggregation failed. Check logs for details.")

    return success

def show_summary():
    """Display summary report."""
    print_header("Summary Report")

    report_path = RESEARCH_DATA_DIR / 'POPULATION_REPORT.md'

    if report_path.exists():
        print(f"📄 Full report available at: {report_path}\n")

        # Show first 50 lines of report
        with open(report_path, 'r') as f:
            lines = f.readlines()[:50]
            print(''.join(lines))

        if len(lines) >= 50:
            print("\n... (truncated)")
            print(f"\nView full report: cat {report_path}")
    else:
        print("⚠️  Summary report not found")

def main():
    """Main orchestrator function."""
    print("=" * 80)
    print("InfraFlow AI - Data Aggregation Orchestrator".center(80))
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Menu
    print("What would you like to do?\n")
    print("1. Run full pipeline (check → test → aggregate)")
    print("2. Check prerequisites only")
    print("3. Test connections only")
    print("4. Check research data status only")
    print("5. Run aggregation only (skip checks)")
    print("6. View summary report")
    print("7. Monitor aggregation (real-time)")
    print("0. Exit")

    choice = input("\nEnter choice [0-7]: ").strip()

    if choice == '0':
        print("Exiting...")
        return 0

    elif choice == '1':
        # Full pipeline
        if not check_prerequisites():
            print("\n❌ Prerequisites check failed. Fix issues and try again.")
            return 1

        if not test_connections():
            print("\n❌ Connection tests failed. Fix issues and try again.")
            return 1

        check_research_status()

        proceed = input("\nProceed with aggregation? [y/N]: ").strip().lower()
        if proceed != 'y':
            print("Aggregation cancelled.")
            return 0

        if run_aggregation():
            show_summary()
            return 0
        else:
            return 1

    elif choice == '2':
        check_prerequisites()

    elif choice == '3':
        test_connections()

    elif choice == '4':
        check_research_status()

    elif choice == '5':
        proceed = input("⚠️  This will skip all checks. Continue? [y/N]: ").strip().lower()
        if proceed == 'y':
            if run_aggregation():
                show_summary()
                return 0
            else:
                return 1
        else:
            print("Cancelled.")

    elif choice == '6':
        show_summary()

    elif choice == '7':
        print("\nStarting real-time monitoring...")
        subprocess.run([f"python3", f"{BACKEND_DIR / 'monitor_aggregation.py'}"])

    else:
        print("Invalid choice.")
        return 1

    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
