import json
import os

# Define path to roles.json relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROLES_JSON_PATH = os.path.join(BASE_DIR, "..", "data", "roles.json")

# Load roles data from JSON once at import
with open(ROLES_JSON_PATH, "r") as f:
    roles_data = json.load(f)

# Extract the dictionaries for easy access
role_model_paths = {role: info["model_path"] for role, info in roles_data.items()}
role_skill_map = {role: info["skills"] for role, info in roles_data.items()}
role_qualification_map = {role: info["qualifications"] for role, info in roles_data.items()}
