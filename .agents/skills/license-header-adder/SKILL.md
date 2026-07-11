---
name: license-header-adder
description: >
  Adds the standard corporate Apache 2.0 license header to the first cell of new notebooks.
tools: [Read, Write]
---

# Skill: License Header Adder

Prepend standard Apache 2.0 license headers to notebook source files.

## Steps

1. **Read Template**
   - Read the license content from `resources/HEADER.txt`.

2. **Apply to Notebook**
   - Parse the target notebook JSON.
   - Insert a code cell containing the license lines at the very beginning of the cells array.
   - The cell should have `"execution_count": null`, `"outputs": []`, and `"source"` populated with the license comment lines.

3. **Verify**
   - Verify the license code cell is the first cell in the array.
