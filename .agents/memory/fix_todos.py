import json

def fix():
    notebook_path = "src/aerospace-eosid-trajectory-engine.ipynb"
    
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            source = cell["source"]
            new_source = []
            for line in source:
                # Fix installation cell
                if "{TODO: Suggest using the latest major GA version of each package; i.e., --upgrade}" in line:
                    line = line.replace("{TODO: Suggest using the latest major GA version of each package; i.e., --upgrade}", "We recommend using the latest major version of each package (i.e. --upgrade).")
                # Fix before you begin cell
                if " {TODO: Update the APIs needed for your tutorial. Edit the API names, and update the link to append the API IDs, separating each one with a comma. For example, container.googleapis.com,cloudbuild.googleapis.com}" in line:
                    line = line.replace(" {TODO: Update the APIs needed for your tutorial. Edit the API names, and update the link to append the API IDs, separating each one with a comma. For example, container.googleapis.com,cloudbuild.googleapis.com}", "")
                # Fix cleaning up cell
                if "{TODO: Include commands to delete individual resources below}" in line:
                    line = line.replace("{TODO: Include commands to delete individual resources below}", "In this tutorial, no persistent endpoints or models were deployed. Only temporary Cloud Storage objects may have been created, which can be deleted below.")
                new_source.append(line)
            cell["source"] = new_source
            
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
        
    print("Notebook placeholders successfully completed.")

if __name__ == "__main__":
    fix()
