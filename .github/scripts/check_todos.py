#!/usr/bin/env python3
import json
import sys
import os

def log_warning(file, line_num, cell_idx, cell_type, pattern, line_content):
    print(f"::warning file={file},line={line_num},title=Unfilled Placeholder::Cell {cell_idx} ({cell_type}) contains placeholder '{pattern}'")
    print(f"⚠️  {file}: Cell {cell_idx} ({cell_type}) line {line_num} contains placeholder '{pattern}': \"{line_content}\"")

def check_todos(filepath):
    print(f"Scanning for placeholders in: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse JSON for {filepath}: {str(e)}")
        return 0
        
    cells = notebook.get('cells', [])
    placeholders = [
        "{TODO:",
        "{TODO ",
        "[TODO]",
        "[your-project-id]",
        "your-bucket-name",
        "web-doc-title",
        "linkback-to-webdoc-page"
    ]
    
    found_count = 0
    
    for idx, cell in enumerate(cells):
        cell_type = cell.get('cell_type', 'unknown')
        source_lines = cell.get('source', [])
        
        # Skip the first cell since it contains the license header which could mention Apache License references,
        # but check for placeholders anyway, except we ignore Copyright date ranges.
        # Let's check all cells.
        for line_num, line in enumerate(source_lines, 1):
            for pattern in placeholders:
                if pattern in line:
                    # Ignore the template cell instructions themselves if checking the template file itself,
                    # but since this script is for authored notebooks in src/, we check everything.
                    line_truncated = line.strip()
                    if len(line_truncated) > 60:
                        line_truncated = line_truncated[:57] + "..."
                    log_warning(filepath, line_num, idx, cell_type, pattern, line_truncated)
                    found_count += 1
                    
    return found_count

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_todos.py <notebook_path1> <notebook_path2> ...")
        sys.exit(0)
        
    total_found = 0
    for filepath in sys.argv[1:]:
        total_found += check_todos(filepath)
        
    if total_found > 0:
        print(f"\n❌ Found {total_found} unfilled placeholder(s)/TODOs in notebooks.")
        sys.exit(1)
    else:
        print("\n✅ No placeholders or TODOs found.")
        sys.exit(0)
