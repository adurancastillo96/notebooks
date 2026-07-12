---
name: license-header-adder
description: >
  Adds the standard corporate Apache 2.0 license header to the first cell of new notebooks.
tools: [Read, Write]
---

# Skill: License Header Adder

Prepend standard Apache 2.0 license headers to markdown source files.

## Steps

1. **Read Template**
   - Read the license content from `resources/HEADER.txt`.

2. **Apply to Notebook**
   - Read the target notebook markdown file.
   - Insert a python code block containing the license lines at the very beginning of the file.
   - The block should be wrapped with ` ```python ` and ` ``` `.

3. **Verify**
   - Verify the license code block is the first content in the file.
