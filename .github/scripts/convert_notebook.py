#!/usr/bin/env python3
import json
import sys
import os
import re

DEFAULT_METADATA = {
    "colab": {
        "collapsed_sections": [],
        "name": "notebook.ipynb",
        "toc_visible": True
    },
    "environment": {
        "kernel": "micromamba-base-py",
        "name": "workbench-notebooks.m20260701-2130-rc0",
        "type": "gcloud",
        "uri": "us-docker.pkg.dev/deeplearning-platform-release/gcr.io/workbench-notebooks:m20260701-2130-rc0"
    },
    "kernelspec": {
        "display_name": "Python 3 (Local) (Local)",
        "language": "python",
        "name": "micromamba-base-py"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.13"
    }
}

def ipynb_to_md(ipynb_path, md_path):
    with open(ipynb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
        
    cells = nb.get('cells', [])
    md_blocks = []
    
    for cell in cells:
        cell_type = cell.get('cell_type')
        source = cell.get('source', [])
        
        # Ensure source is a list of lines
        if isinstance(source, str):
            source = [source]
            
        content = "".join(source)
        if not content:
            continue
            
        if cell_type == 'code':
            # Wrap in ```python
            block = "```python\n" + content
            if not block.endswith('\n'):
                block += '\n'
            block += "```"
            md_blocks.append(block)
        elif cell_type == 'markdown':
            block = content
            if not block.endswith('\n'):
                block += '\n'
            md_blocks.append(block.rstrip('\n'))
        else:
            # Skip or treat as markdown
            block = content
            md_blocks.append(block)
            
    # Join the blocks with two newlines
    md_content = "\n\n".join(md_blocks) + "\n"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(md_path)), exist_ok=True)
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    print(f"Successfully converted {ipynb_path} -> {md_path}")

def md_to_ipynb(md_path, ipynb_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    cells = []
    current_cell_type = None  # 'code' or 'markdown'
    current_lines = []
    
    def save_cell():
        if not current_lines:
            return
            
        # Clean up trailing newlines inside the cell source list for neatness
        # but preserve structure. Jupyter lines usually end with \n.
        source = list(current_lines)
        
        # If it's all whitespace/empty, we can skip it unless it's a code cell (which we usually don't want empty anyway)
        if current_cell_type == 'code':
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": source
            })
        else:
            # Markdown cell
            # Check if source has only newlines, if so skip
            source_str = "".join(source).strip()
            if source_str:
                cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": source
                })
                
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith("```python"):
            # Start of code block
            # Save whatever markdown we accumulated
            if current_lines:
                # We were in markdown (or starting new)
                current_cell_type = 'markdown'
                save_cell()
            current_cell_type = 'code'
            current_lines = []
        elif current_cell_type == 'code' and stripped == "```":
            # End of code block
            save_cell()
            current_cell_type = None
            current_lines = []
        else:
            if current_cell_type == 'code':
                current_lines.append(line)
            else:
                # We are in markdown.
                # Split on H1/H2/H3/H4 headers to create clean separate markdown cells
                is_header = False
                if re.match(r'^#{1,4}\s+', stripped):
                    is_header = True
                    
                if is_header and current_lines:
                    # Save current accumulated markdown cell before starting the new one
                    current_cell_type = 'markdown'
                    save_cell()
                    current_lines = []
                    
                current_lines.append(line)
                
    # Save the last cell
    if current_lines:
        if current_cell_type is None:
            current_cell_type = 'markdown'
        save_cell()
        
    # Replicate default metadata, using the notebook filename
    filename = os.path.basename(ipynb_path)
    metadata = dict(DEFAULT_METADATA)
    metadata["colab"] = dict(metadata["colab"])
    metadata["colab"]["name"] = filename
    
    notebook = {
        "cells": cells,
        "metadata": metadata,
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(os.path.abspath(ipynb_path)), exist_ok=True)
    with open(ipynb_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=1, ensure_ascii=False)
        f.write('\n')
    print(f"Successfully converted {md_path} -> {ipynb_path}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage:")
        print("  python convert_notebook.py --to-md <input.ipynb> <output.md>")
        print("  python convert_notebook.py --to-ipynb <input.md> <output.ipynb>")
        sys.exit(1)
        
    mode = sys.argv[1]
    infile = sys.argv[2]
    outfile = sys.argv[3]
    
    if mode == '--to-md':
        ipynb_to_md(infile, outfile)
    elif mode == '--to-ipynb':
        md_to_ipynb(infile, outfile)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)
