#!/usr/bin/env python3
import json
import sys
import os
import re

def log_warning(file, line_num, cell_idx, cell_type, pattern, line_content):
    print(f"::warning file={file},line={line_num},title=Unfilled Placeholder::Cell {cell_idx} ({cell_type}) contains placeholder '{pattern}'")
    print(f"⚠️  {file}: Cell {cell_idx} ({cell_type}) line {line_num} contains placeholder '{pattern}': \"{line_content}\"")

def parse_md_to_cells(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cells = []
    current_cell_type = None  # 'code' or 'markdown'
    current_lines = []
    
    def save_cell():
        if not current_lines:
            return
        if current_cell_type == 'code':
            cells.append({
                "cell_type": "code",
                "source": list(current_lines)
            })
        else:
            source_str = "".join(current_lines).strip()
            if source_str:
                cells.append({
                    "cell_type": "markdown",
                    "source": list(current_lines)
                })
                
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```python"):
            if current_lines:
                current_cell_type = 'markdown'
                save_cell()
            current_cell_type = 'code'
            current_lines = []
        elif current_cell_type == 'code' and stripped == "```":
            save_cell()
            current_cell_type = None
            current_lines = []
        else:
            if current_cell_type == 'code':
                current_lines.append(line)
            else:
                is_header = False
                if re.match(r'^#{1,4}\s+', stripped):
                    is_header = True
                if is_header and current_lines:
                    current_cell_type = 'markdown'
                    save_cell()
                    current_lines = []
                current_lines.append(line)
    if current_lines:
        if current_cell_type is None:
            current_cell_type = 'markdown'
        save_cell()
    return cells

def check_todos(filepath):
    print(f"Scanning for placeholders in: {filepath}")
    filename = os.path.basename(filepath)
    
    cells = []
    if filename.endswith('.md'):
        cells = parse_md_to_cells(filepath)
    elif filename.endswith('.ipynb'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            cells = notebook.get('cells', [])
        except Exception as e:
            print(f"❌ Failed to parse JSON for {filepath}: {str(e)}")
            return 0
    else:
        print(f"❌ Unsupported file type: {filepath}")
        return 0
        
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
        
        for line_num, line in enumerate(source_lines, 1):
            for pattern in placeholders:
                if pattern in line:
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
