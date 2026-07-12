import json
import os

def rename_in_file(filepath, replacements):
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} (does not exist)")
        return
        
    print(f"Processing replacements in: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for target, replacement in replacements:
        content = content.replace(target, replacement)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # Define replacements for general text and markdown files
    general_replacements = [
        ("PROJECT_ID", "GOOGLE_CLOUD_PROJECT"),
        ("REGION", "GOOGLE_CLOUD_LOCATION"),
        ("[your-project-id]", "[your-google-cloud-project]"),
        ("your-gcp-project-id", "your-google-cloud-project-id"),
        ("project-id", "google-cloud-project"),
        ("region", "google-cloud-location")
    ]
    
    # Files to update
    files = [
        "spec/requirements.md",
        "spec/acceptance.md",
        "spec/plan.md",
        "spec/tasks/T001.md",
        "spec/tasks/T002.md",
        "spec/tasks/T003.md",
        ".agents/rules/notebook.md",
        ".agents/rules/security.md",
        ".agents/skills/create-notebook/SKILL.md",
        ".agents/skills/notebook-lint/SKILL.md",
        ".agents/memory/PICKUP.md",
        ".agents/memory/learnings.md"
    ]
    
    for filepath in files:
        rename_in_file(filepath, general_replacements)
        
    # Special replacements for linter script
    linter_replacements = [
        ("PROJECT_ID", "GOOGLE_CLOUD_PROJECT"),
        ("REGION", "GOOGLE_CLOUD_LOCATION"),
        ("has_project_id", "has_google_cloud_project"),
        ("has_region", "has_google_cloud_location")
    ]
    rename_in_file(".github/scripts/check_notebook_structure.py", linter_replacements)
    
    # Special replacements for notebook_template.ipynb
    notebook_template_replacements = [
        ("PROJECT_ID", "GOOGLE_CLOUD_PROJECT"),
        ("REGION", "GOOGLE_CLOUD_LOCATION")
    ]
    rename_in_file("notebook_template.ipynb", notebook_template_replacements)
    
    # Special replacements for src/aerospace-eosid-trajectory-engine.ipynb
    rename_in_file("src/aerospace-eosid-trajectory-engine.ipynb", notebook_template_replacements)
    
    print("Variable rename completed successfully across the whole project.")

if __name__ == "__main__":
    main()
