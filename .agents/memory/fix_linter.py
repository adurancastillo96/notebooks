import json

def fix_linter():
    notebook_path = "src/aerospace-eosid-trajectory-engine.ipynb"
    
    with open(notebook_path, "r", encoding="utf-8") as f:
        nb = json.load(f)
        
    cells = nb["cells"]
    
    # 1. Update License Cell (Cell 0) to include Antony Duran
    cells[0]["source"] = [
        "# Antony Duran\n",
        "#\n",
        "# Licensed under the Apache License, Version 2.0 (the \"License\");\n",
        "# you may not use this file except in compliance with the License.\n",
        "# You may obtain a copy of the License at\n",
        "#\n",
        "#     https://www.apache.org/licenses/LICENSE-2.0\n",
        "#\n",
        "# Unless required by applicable law or agreed to in writing, software\n",
        "# distributed under the License is distributed on an \"AS IS\" BASIS,\n",
        "# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n",
        "# See the License for the specific language governing permissions and\n",
        "# limitations under the License."
    ]
    
    # 2. Update PROJECT_ID cell (Cell 11) to be a parameterized string literal satisfying the regex check
    cells[11]["source"] = [
        "PROJECT_ID = \"\"  # @param {type:\"string\"}\n",
        "\n",
        "import os\n",
        "if not PROJECT_ID:\n",
        "    PROJECT_ID = os.getenv(\"GOOGLE_CLOUD_PROJECT\") or os.getenv(\"PROJECT_ID\") or \"\"\n",
        "\n",
        "# Set the project id\n",
        "if PROJECT_ID:\n",
        "    ! gcloud config set project {PROJECT_ID}"
    ]
    
    # 3. Update REGION cell (Cell 13) to be a parameterized string literal satisfying the regex check
    cells[13]["source"] = [
        "REGION = \"us-central1\"  # @param {type:\"string\"}\n",
        "\n",
        "import os\n",
        "if not REGION:\n",
        "    REGION = os.getenv(\"GOOGLE_CLOUD_LOCATION\") or os.getenv(\"REGION\") or \"us-central1\""
    ]
    
    # 4. Update BUCKET_URI cell (Cell 21) to remove "your-bucket-name" placeholder
    cells[21]["source"] = [
        "BUCKET_URI = \"\"  # @param {type:\"string\"}\n",
        "\n",
        "import os\n",
        "if not BUCKET_URI and PROJECT_ID:\n",
        "    BUCKET_URI = os.getenv(\"BUCKET_URI\") or f\"gs://aerospace-eosid-{PROJECT_ID}-unique\""
    ]
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1)
        
    print("Notebook updated for linter compliance.")

if __name__ == "__main__":
    fix_linter()
