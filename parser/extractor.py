import re
import spacy

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")

# Skills and keyword databases
SKILLS_DB = [
    'Python', 'Java', 'C++', 'JavaScript', 'SQL', 'AWS', 'Azure', 'Docker',
    'Kubernetes', 'React', 'Node.js', 'Machine Learning', 'Deep Learning',
    'TensorFlow', 'PyTorch', 'Data Analysis', 'Git', 'Linux', 'HTML', 'CSS',
    'Django', 'Flask', 'REST API', 'NoSQL', 'MongoDB'
]

EDU_KEYWORDS = ['bachelor', 'master', 'b.tech', 'm.tech', 'phd', 'bs', 'ms', 'bsc', 'msc', 'engineering', 'university', 'college']
EXP_KEYWORDS = ['experience', 'internship', 'project', 'worked', 'developed', 'engineer', 'developer']
CERT_KEYWORDS = ['certification', 'certificate', 'certified', 'course', 'training']

# ----------------------------
# ✅ Contact Info Extractor
# ----------------------------
def extract_contact_info(text):
    # Email
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    email = emails[0] if emails else None

    # Phone - non-capturing group to get full number
    phone_pattern = r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, text)
    phone = phones[0] if phones else None

    # Name (first line or NLP-based)
    name = None
    lines = text.strip().split('\n')
    if lines and len(lines[0].split()) <= 5 and lines[0].strip().lower() not in ['resume', 'curriculum vitae', 'cv']:
        name = lines[0].strip()

        # Clean 'Name:', 'Name :', or similar prefix from the extracted name
        name = re.sub(r'^[Nn]ame\s*:?\s*', '', name)

    if not name:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                name = ent.text.strip()
                break

    return {'name': name, 'email': email, 'phone': phone}

# ----------------------------
# ✅ Skill Extractor
# ----------------------------
def extract_skills(text):
    found_skills = set()
    text_lower = text.lower()
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(skill)
    return list(found_skills)

# ----------------------------
# ✅ Education Extractor
# ----------------------------
def extract_education(text):
    education_lines = []
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in EDU_KEYWORDS):
            education_lines.append(line.strip())
    return education_lines

# ----------------------------
# ✅ Experience Extractor
# ----------------------------
def extract_experience(text):
    experience_lines = []
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in EXP_KEYWORDS):
            experience_lines.append(line.strip())
    return experience_lines

# ----------------------------
# ✅ Certification Extractor
# ----------------------------
def extract_certifications(text):
    cert_lines = []
    lines = text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if any(keyword in line_lower for keyword in CERT_KEYWORDS):
            cert_lines.append(line.strip())
    return cert_lines
