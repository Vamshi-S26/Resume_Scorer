import re
import os
from parser.file_reader import read_file
from parser.extractor import extract_skills, extract_certifications, extract_education, extract_experience, extract_contact_info

def parse_resume(file_path):
    text = read_file(file_path)

    skills = extract_skills(text)
    education = extract_education(text)
    certifications = extract_certifications(text)
    experience = extract_experience(text)
    contact_info = extract_contact_info(text)

    return {
        "full_text": text,
        "skills": skills,
        "education": education,
        "certifications": certifications,
        "experience": experience,
        "contact_info": contact_info
    }
