#!/usr/bin/env python3
import json
import sys
import os
import re

def log_error(file, check, message):
    print(f"::error file={file},title={check}::{message}")
    print(f"❌ FAIL [{check}]: {message}")

def log_pass(check, message):
    print(f"✅ PASS [{check}]: {message}")

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

def check_file(filepath):
    print(f"\nChecking notebook: {filepath}")
    filename = os.path.basename(filepath)
    
    # Check naming convention and parse structure
    if filename.endswith('.md'):
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*\.md$', filename):
            log_error(filepath, "File Naming", "Filename must be kebab-case (lowercase, numbers, and hyphens only, e.g., category-name.md)")
            return False
        cells = parse_md_to_cells(filepath)
    elif filename.endswith('.ipynb'):
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*\.ipynb$', filename):
            log_error(filepath, "File Naming", "Filename must be kebab-case (lowercase, numbers, and hyphens only, e.g., category-name.ipynb)")
            return False
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            cells = notebook.get('cells', [])
        except Exception as e:
            log_error(filepath, "JSON Parsing", f"Failed to parse notebook JSON: {str(e)}")
            return False
    else:
        log_error(filepath, "File Type", "Unsupported file type (must be .md or .ipynb)")
        return False
        
    if not cells:
        log_error(filepath, "Empty Notebook", "Notebook contains no cells")
        return False
        
    passed = True
    
    # 1. License cell check (first cell must be code cell with Apache 2.0)
    first_cell = cells[0]
    if first_cell.get('cell_type') != 'code':
        log_error(filepath, "License Header", "First cell must be a code cell containing the Apache 2.0 license header")
        passed = False
    else:
        source_text = "".join(first_cell.get('source', []))
        if "Duran" not in source_text or "Apache License" not in source_text:
            log_error(filepath, "License Header", "First code cell does not contain a valid Apache 2.0 license header")
            passed = False
        else:
            log_pass("License Header", "First code cell contains Apache 2.0 license header")
            
    # 2. H1 Title check (second cell must be markdown with H1 title, not a TODO)
    if len(cells) < 2:
        log_error(filepath, "Notebook Length", "Notebook is too short (must contain at least structure header cells)")
        return False
        
    second_cell = cells[1]
    if second_cell.get('cell_type') != 'markdown':
        log_error(filepath, "H1 Title", "Second cell must be a markdown cell containing the H1 title heading")
        passed = False
    else:
        source_text = "".join(second_cell.get('source', []))
        if not source_text.startswith('# '):
            log_error(filepath, "H1 Title", "Second cell markdown must start with a single H1 header '# '")
            passed = False
        elif "[TODO]" in source_text or "TODO" in source_text:
            log_error(filepath, "H1 Title", "H1 title heading contains [TODO] or placeholder text")
            passed = False
        else:
            log_pass("H1 Title", f"Valid H1 heading found: {source_text.strip()}")
            
    # Required sections must appear in the template order, not merely exist somewhere.
    # Required subsections: Objective, Dataset, Costs
    required_h2 = {
        "Overview": False,
        "Installation": False,
        "Before you begin": False,
        "Cleaning up": False
    }
    required_h3 = {
        "Objective": False,
        "Dataset": False,
        "Costs": False
    }
    
    headings = []
    for cell in cells:
        if cell.get('cell_type') == 'markdown':
            source_lines = cell.get('source', [])
            for line in source_lines:
                line_clean = line.strip()
                # Check H2
                if line_clean.startswith('## '):
                    header_text = line_clean[3:].strip()
                    for h2 in required_h2:
                        if h2.lower() in header_text.lower():
                            required_h2[h2] = True
                            headings.append(("h2", h2))
                # Check H3
                elif line_clean.startswith('### '):
                    header_text = line_clean[4:].strip()
                    for h3 in required_h3:
                        if h3.lower() in header_text.lower():
                            required_h3[h3] = True
                            headings.append(("h3", h3))
                            
    for h2, found in required_h2.items():
        if not found:
            log_error(filepath, "Required Section", f"Missing required section header '## {h2}'")
            passed = False
        else:
            log_pass("Required Section", f"Found section '## {h2}'")
            
    for h3, found in required_h3.items():
        if not found:
            log_error(filepath, "Required Subsection", f"Missing required subsection header '### {h3}'")
            passed = False
        else:
            log_pass("Required Subsection", f"Found subsection '### {h3}'")

    expected_heading_order = [
        ("h2", "Overview"),
        ("h3", "Objective"),
        ("h3", "Dataset"),
        ("h3", "Costs"),
        ("h2", "Installation"),
        ("h2", "Before you begin"),
        ("h2", "Cleaning up"),
    ]
    heading_positions = {heading: index for index, heading in enumerate(headings)}
    observed_positions = [heading_positions.get(heading, -1) for heading in expected_heading_order]
    if any(position < 0 for position in observed_positions) or observed_positions != sorted(observed_positions):
        log_error(filepath, "Section Order", "Required template sections are missing or out of order")
        passed = False
    else:
        log_pass("Section Order", "Required template sections follow the template order")
            
    # 5 & 6. Project ID and Region cells check
    has_google_cloud_project = False
    has_google_cloud_location = False
    
    for cell in cells:
        if cell.get('cell_type') == 'code':
            source_text = "".join(cell.get('source', []))
            # Match GOOGLE_CLOUD_PROJECT = ... (ignoring comments)
            if re.search(r'^\s*(?:GOOGLE_CLOUD_PROJECT|PROJECT_ID)\s*=\s*["\'].*@param', source_text, re.MULTILINE):
                has_google_cloud_project = True
            if re.search(r'^\s*(?:GOOGLE_CLOUD_LOCATION|REGION)\s*=\s*["\'].*@param', source_text, re.MULTILINE):
                has_google_cloud_location = True
                
    if not has_google_cloud_project:
        log_error(filepath, "Parameterization", "Missing GOOGLE_CLOUD_PROJECT (or PROJECT_ID) variable assignment in code cells")
        passed = False
    else:
        log_pass("Parameterization", "Found GOOGLE_CLOUD_PROJECT parameterization")
        
    if not has_google_cloud_location:
        log_error(filepath, "Parameterization", "Missing GOOGLE_CLOUD_LOCATION (or REGION) variable assignment in code cells")
        passed = False
    else:
        log_pass("Parameterization", "Found GOOGLE_CLOUD_LOCATION parameterization")
        
    return passed

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: check_notebook_structure.py <notebook_path1> <notebook_path2> ...")
        sys.exit(0)
        
    files_failed = 0
    for filepath in sys.argv[1:]:
        if not check_file(filepath):
            files_failed += 1
            
    if files_failed > 0:
        print(f"\n❌ Lint failed: {files_failed} notebook(s) did not meet standard structure requirements.")
        sys.exit(1)
    else:
        print("\n✅ Lint passed: All notebooks conform to the standard structure requirements.")
        sys.exit(0)
