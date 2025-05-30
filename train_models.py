import os
import json
import joblib
import numpy as np
import re
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

MODEL_DIR = "model"
DATASET_PATH = "data/resumes_dataset.json"
ROLES_SKILLS_PATH = "data/roles_skills.json"

os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(os.path.dirname(ROLES_SKILLS_PATH), exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[\\/:"*?<>|]+', '_', name)

def load_dataset():
    with open(DATASET_PATH, "r") as f:
        return json.load(f)

def load_roles_skills():
    if os.path.exists(ROLES_SKILLS_PATH):
        with open(ROLES_SKILLS_PATH, "r") as f:
            return json.load(f)
    else:
        return {}

def save_roles_skills(roles_skills):
    with open(ROLES_SKILLS_PATH, "w") as f:
        json.dump(roles_skills, f, indent=4)

def train_models(selected_roles=None):
    data = load_dataset()
    role_data = defaultdict(list)
    for item in data:
        role = item["goal"]
        text = item["resume_text"]
        label = item["label"]
        role_data[role].append((text, label))

    if selected_roles is None:
        selected_roles = list(role_data.keys())
    else:
        selected_roles = [r for r in selected_roles if r in role_data]

    print(f"Training models for roles: {selected_roles}\n")

    for role in selected_roles:
        samples = role_data[role]
        texts, labels = zip(*samples)
        labels = np.array(labels)

        if len(set(labels)) < 2:
            print(f"Skipping '{role}' — not enough class variety.\n")
            continue

        print(f"Training and evaluating for role: '{role}'")
        print(f"Samples: {len(samples)}, Class distribution: {np.bincount(labels)}")

        X_train, X_test, y_train, y_test = train_test_split(
            texts, labels, test_size=0.3, stratify=labels, random_state=42)

        print(f"Training on {len(X_train)} samples, Testing on {len(X_test)} samples")

        pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)),
            ('clf', LogisticRegression(solver='liblinear', max_iter=1000))
        ])

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        print(f"Accuracy:  {acc:.3f}")
        print(f"Precision: {prec:.3f}")
        print(f"Recall:    {rec:.3f}")
        print(f"F1-Score:  {f1:.3f}")

        safe_role = sanitize_filename(role).replace(' ', '_')
        model_path = os.path.join(MODEL_DIR, f"{safe_role}_model.pkl")

        model_info = {
            'pipeline': pipeline,
            'vocab': pipeline.named_steps['tfidf'].vocabulary_
        }
        joblib.dump(model_info, model_path)

        print(f"Model saved to {model_path}\n")

    print("Training complete.\n")

if __name__ == "__main__":
    # Define roles and their key skills (can be extended or modified as needed)
    roles_skills = {
        "Frontend Developer": ["html", "css", "javascript", "react", "git"],
        "Backend Developer": ["python", "django", "rest apis", "sql", "docker"],
        "Data Scientist": ["python", "machine learning", "data analysis", "pandas", "numpy"],
        "Machine Learning Engineer": ["tensorflow", "keras", "python", "model training", "scikit-learn"],
        "Android Developer": ["java", "kotlin", "android sdk", "firebase", "xml"],
        "DevOps Engineer": ["docker", "kubernetes", "jenkins", "aws", "linux"],
        "Cloud Architect": ["aws", "gcp", "azure", "terraform", "cloud networking"],
        "Cybersecurity Analyst": ["network security", "firewalls", "ethical hacking", "siem", "encryption"],
        "Database Administrator": ["sql", "oracle", "performance tuning", "postgresql", "backups"],
        "QA Engineer": ["selenium", "test cases", "bug reports", "automation", "jira"],
        "Full Stack Developer": ["html", "css", "javascript", "node.js", "mongodb"],
        "NLP Engineer": ["nlp", "transformers", "spacy", "bert", "text classification"],
        "Blockchain Developer": ["solidity", "ethereum", "smart contracts", "web3", "cryptography"],
        "UI/UX Designer": ["figma", "sketch", "wireframing", "prototyping", "user research"],
        "System Administrator": ["linux", "docker", "kubernetes", "aws", "jenkins", "shell scripting", "troubleshooting", "monitoring"],
        "Game Developer": ["unity", "c#", "game physics", "level design", "animation"],
        "IoT Developer": ["arduino", "raspberry pi", "mqtt", "iot protocols", "c++"],
        "AI Researcher": ["deep learning", "pytorch", "mathematics", "publications", "algorithms"],
        "Robotics Engineer": ["ros", "control systems", "c++", "path planning", "mechanical design"],
        "Web Developer": ["html", "css", "javascript", "bootstrap", "php"]
    }

    # Save or update roles_skills json
    save_roles_skills(roles_skills)

    # Train models for all defined roles
    train_models(selected_roles=list(roles_skills.keys()))
