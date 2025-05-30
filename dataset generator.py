import json
import random
from faker import Faker
import os

fake = Faker()
random.seed(42)

# Define 20 roles and their top skills
role_skill_map = {
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
    "System Administrator": ["linux", "shell scripting", "monitoring", "troubleshooting", "backups"],
    "Game Developer": ["unity", "c#", "game physics", "level design", "animation"],
    "IoT Developer": ["arduino", "raspberry pi", "mqtt", "iot protocols", "c++"],
    "AI Researcher": ["deep learning", "pytorch", "mathematics", "publications", "algorithms"],
    "Robotics Engineer": ["ros", "control systems", "c++", "path planning", "mechanical design"],
    "Web Developer": ["html", "css", "javascript", "bootstrap", "php"]
}

samples_per_role = 250
positive_ratio = 0.6
dataset = []

def generate_resume(role, is_selected, skills):
    if is_selected:
        selected_skills = random.sample(skills, random.randint(3, 5))
    else:
        selected_skills = [fake.word() for _ in range(5)]

    extra_skills = [fake.word() for _ in range(2)]
    all_skills = selected_skills + extra_skills

    qualifications = f"B.Tech in {fake.word().capitalize()} from {fake.company()}"
    latest_project = fake.sentence(nb_words=6)
    latest_internship = f"{fake.company()} - {fake.job()} internship"

    resume_text = (
        f"{fake.name()}\n"
        f"Email: {fake.email()}\n"
        f"Phone: {fake.phone_number()}\n"
        f"Skills: {', '.join(all_skills)}\n"
        f"Strengths: {fake.word()}, {fake.word()}\n"
        f"Experience: {fake.sentence(nb_words=10)}\n"
        f"Latest Project: {latest_project}\n"
        f"Internship: {latest_internship}\n"
        f"Certifications: {fake.word()} Certification\n"
        f"Education: {qualifications}"
    )

    return {
        "goal": role,
        "label": 1 if is_selected else 0,
        "resume_text": resume_text,
        "skills": selected_skills,
        "qualifications": qualifications,
        "latest_project": latest_project,
        "latest_internship": latest_internship
    }

# Generate data
for role, skills in role_skill_map.items():
    num_positive = int(samples_per_role * positive_ratio)
    num_negative = samples_per_role - num_positive

    for _ in range(num_positive):
        dataset.append(generate_resume(role, True, skills))

    for _ in range(num_negative):
        dataset.append(generate_resume(role, False, skills))

# Shuffle dataset
random.shuffle(dataset)

# Save to file
os.makedirs("data", exist_ok=True)
with open("data/resumes_dataset.json", "w") as f:
    json.dump(dataset, f, indent=2)

print(f"Generated {len(dataset)} samples for 20 roles with structured fields in 'data/resumes_dataset.json'")
