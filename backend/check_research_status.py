#!/usr/bin/env python3
"""
Check the status of research data files.
"""

import json
from pathlib import Path
from datetime import datetime

RESEARCH_DATA_DIR = Path('/home/claude-user/ai-consults-platform/00-pivot/research_data')

EXPECTED_FILES = [
    'ebrd_projects.json',
    'eib_projects.json',
    'ifc_projects.json',
    'worldbank_projects.json',
    'adb_projects.json',
    'afdb_projects.json',
    'compliance_standards.json',
    'renewable_energy_projects.json',
    'water_infrastructure_projects.json',
    'hydrogen_projects.json'
]

def check_file_status():
    """Check which research files are available."""
    print("=" * 80)
    print("InfraFlow AI - Research Data Status Check")
    print("=" * 80)
    print(f"Check Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    if not RESEARCH_DATA_DIR.exists():
        print(f"❌ Research directory not found: {RESEARCH_DATA_DIR}")
        return

    # Find all JSON files
    all_json_files = list(RESEARCH_DATA_DIR.glob('*.json'))

    found_files = []
    missing_files = []
    file_stats = []

    # Check expected files
    for filename in EXPECTED_FILES:
        filepath = RESEARCH_DATA_DIR / filename
        if filepath.exists():
            found_files.append(filename)

    # Check all JSON files
    for filepath in all_json_files:
        filename = filepath.name

        # Get file info
        stat = filepath.stat()
        size_kb = stat.st_size / 1024
        modified = datetime.fromtimestamp(stat.st_mtime)

        # Try to read and count records
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if 'projects' in data:
                    record_count = len(data['projects'])
                    record_type = 'projects'
                elif 'green_hydrogen_projects' in data:
                    record_count = len(data['green_hydrogen_projects'])
                    record_type = 'hydrogen projects'
                elif 'compliance_standards' in data:
                    record_count = len(data['compliance_standards'])
                    record_type = 'standards'
                elif 'standards' in data:
                    record_count = len(data['standards'])
                    record_type = 'standards'
                elif 'companies' in data:
                    record_count = len(data['companies'])
                    record_type = 'companies'
                elif 'government_policies' in data:
                    record_count = len(data['government_policies'])
                    record_type = 'policies'
                elif 'carbon_markets' in data:
                    record_count = len(data['carbon_markets'])
                    record_type = 'markets'
                else:
                    record_count = len(data) if isinstance(data, list) else 1
                    record_type = 'records'
        except:
            record_count = 0
            record_type = 'unknown'

        file_stats.append({
            'name': filename,
            'size_kb': size_kb,
            'modified': modified,
            'records': record_count,
            'type': record_type
        })

    # Identify missing expected files
    for filename in EXPECTED_FILES:
        if filename not in [f['name'] for f in file_stats]:
            missing_files.append(filename)

    # Print results
    print(f"📊 Status: {len(found_files)}/{len(EXPECTED_FILES)} expected files | {len(file_stats)} total files\n")

    if file_stats:
        print("✅ Available Files:")
        print("-" * 80)
        for stat in file_stats:
            print(f"  • {stat['name']:<40} {stat['size_kb']:>8.1f} KB  {stat['records']:>5} {stat['type']}")
        print()

    if missing_files:
        print("❌ Missing Files:")
        print("-" * 80)
        for filename in missing_files:
            print(f"  • {filename}")
        print()

    # Calculate total records
    total_records = sum(s['records'] for s in file_stats)
    print(f"📈 Total Records: {total_records}")

    # Estimate completion
    completion_percent = (len(found_files) / len(EXPECTED_FILES)) * 100
    print(f"📊 Completion: {completion_percent:.1f}%")

    if completion_percent == 100:
        print("\n✨ All research files are ready! You can now run the aggregation script.")
        print("\n💡 Next step:")
        print("   python aggregate_and_populate.py")
    else:
        print(f"\n⏳ Waiting for {len(missing_files)} more files...")

    print("=" * 80)

if __name__ == '__main__':
    check_file_status()
