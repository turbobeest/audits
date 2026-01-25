#!/usr/bin/env python3
"""Regenerate audits.json for the audit browser."""

import json
import yaml
from pathlib import Path
from datetime import datetime

AUDITS_DIR = Path("/mnt/walnut-drive/dev/audits/audits")
OUTPUT_PATH = Path("/mnt/walnut-drive/dev/audits/audit-browser/static/data/audits.json")

def main():
    print("=== Regenerating audits.json for browser ===")

    audits = []
    categories = {}

    for yaml_file in sorted(AUDITS_DIR.rglob("*.yaml")):
        try:
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f.read())

            if not data or 'audit' not in data:
                continue

            audit = data.get('audit', {})
            execution = data.get('execution', {})
            description = data.get('description', {})

            # Extract category info
            cat_num = str(audit.get('category_number', '')).zfill(2)
            cat_name = audit.get('category', '')

            if cat_num not in categories:
                # Find category directory name
                rel_path = yaml_file.relative_to(AUDITS_DIR)
                cat_dir = str(rel_path).split('/')[0]
                categories[cat_num] = {
                    "number": cat_num,
                    "name": cat_name,
                    "directory": cat_dir,
                    "audit_count": 0
                }
            categories[cat_num]["audit_count"] += 1

            audit_entry = {
                "id": audit.get('id', ''),
                "name": audit.get('name', ''),
                "category": cat_name,
                "category_number": cat_num,
                "subcategory": audit.get('subcategory', ''),
                "tier": audit.get('tier', ''),
                "status": audit.get('status', 'active'),
                "automatable": execution.get('automatable', ''),
                "severity": execution.get('severity', ''),
                "estimated_duration": str(audit.get('estimated_duration', '')),
                "description": description.get('what', '')[:500] if description.get('what') else '',
                "why_it_matters": description.get('why_it_matters', '')[:500] if description.get('why_it_matters') else '',
                "file_path": str(yaml_file.relative_to(AUDITS_DIR.parent)),
                "requires_runtime": audit.get('requires_runtime', False),
                "requires_physical_access": 'requires_physical_access' in str(data),
                "requires_interviews": 'requires_interviews' in str(data),
            }

            audits.append(audit_entry)

        except Exception as e:
            print(f"  Error: {yaml_file.name}: {e}")

    # Build output structure
    output = {
        "generated": datetime.now().isoformat(),
        "total_audits": len(audits),
        "total_categories": len(categories),
        "categories": list(categories.values()),
        "audits": audits
    }

    # Write JSON
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"  Generated: {OUTPUT_PATH}")
    print(f"  Audits: {len(audits)}")
    print(f"  Categories: {len(categories)}")

    # Also copy to build directory if it exists
    build_path = OUTPUT_PATH.parent.parent / "build" / "data" / "audits.json"
    if build_path.parent.exists():
        with open(build_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        print(f"  Also updated: {build_path}")

if __name__ == "__main__":
    main()
