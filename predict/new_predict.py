import joblib
import re

def clean_text(text):
    """Lowercase, remove non-alphanumeric chars except spaces, and normalize spaces."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def match_skills(resume_skills, role_skills, enriched_text=""):
    """
    Match skills between resume and role.
    Checks if role skill appears in resume skills list or in enriched text.
    Returns two lists: matched skills and missing skills.
    """
    resume_skills_lower = [skill.lower() for skill in resume_skills]
    enriched_text = enriched_text.lower()

    matched = []
    missing = []

    for skill in role_skills:
        skill_lower = skill.lower()
        if skill_lower in resume_skills_lower or skill_lower in enriched_text:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing

def normalize_qualification(text):
    """
    Normalize qualification text to standardized levels.
    Returns 'btech', 'mtech', 'phd', 'diploma', 'intermediate', or 'unknown'.
    """
    text = text.lower()

    if any(keyword in text for keyword in ['bachelor', 'b.tech', 'btech', 'b.e', 'b.sc']):
        return 'btech'
    elif any(keyword in text for keyword in ['master', 'm.tech', 'mtech', 'm.e', 'm.sc']):
        return 'mtech'
    elif 'phd' in text or 'doctor' in text:
        return 'phd'
    elif 'diploma' in text:
        return 'diploma'
    elif 'high school' in text or '12th' in text or 'intermediate' in text:
        return 'intermediate'
    else:
        return 'unknown'

def predict_for_multiple_roles(
    resume_skills,
    resume_experience,
    resume_certifications,
    resume_qualification,
    resume_projects,
    resume_internships,
    resume_text,
    selected_roles,
    role_model_paths,
    role_skill_map,
    role_qualification_map
):
    """
    For each selected role, predicts candidate suitability based on skills, qualifications, and ML model.
    Returns a list of dict results per role with match score, decision, matched/missing skills, and suggestions.
    """

    results = []

    # Compose fallback text for qualification normalization if initial is unknown
    fallback_text = " ".join(resume_experience + resume_certifications + resume_projects + resume_internships + [resume_text])
    normalized_qual = normalize_qualification(resume_qualification)
    if normalized_qual == "unknown":
        normalized_qual = normalize_qualification(fallback_text)

    # Create enriched combined text from all candidate data for ML prediction and skill matching
    enriched_text = (
        "Skills: " + ' '.join(resume_skills) + " " +
        "Experience: " + ' '.join(resume_experience) + " " +
        "Certifications: " + ' '.join(resume_certifications) + " " +
        "Projects: " + ' '.join(resume_projects) + " " +
        "Internships: " + ' '.join(resume_internships) + " " +
        resume_text
    )
    enriched_text = clean_text(enriched_text)

    for role in selected_roles:
        # Check role info presence
        if role not in role_model_paths or role not in role_skill_map or role not in role_qualification_map:
            print(f"[WARN] Missing model/skills/qualification info for role: {role}")
            continue

        # Qualification mismatch immediate rejection
        if normalized_qual not in role_qualification_map[role]:
            results.append({
                "role": role,
                "match_score": 0.0,
                "prediction": "Rejected",
                "matched_skills": [],
                "missing_skills": role_skill_map[role],
                "suggestions": [f"Learn {skill}" for skill in role_skill_map[role]],
                "qualification_required": role_qualification_map[role],
                "candidate_qualification": normalized_qual,
                "has_projects_or_internships": bool(resume_projects or resume_internships)
            })
            continue

        # Load model pipeline
        try:
            model_info = joblib.load(role_model_paths[role])
            pipeline = model_info['pipeline']
        except Exception as e:
            print(f"[ERROR] Failed to load model for {role}: {e}")
            continue

        # Predict suitability using ML model
        prediction = pipeline.predict([enriched_text])[0]
        proba = pipeline.predict_proba([enriched_text])[0][1]  # Probability of positive class
        match_score = round(proba * 100, 2)

        # Skill matching for additional analysis
        matched, missing = match_skills(resume_skills, role_skill_map[role], enriched_text)
        has_projects_or_internships = bool(resume_projects or resume_internships)

        # Decision logic: require minimum matched skills or boosted by projects/internships
        enough_skills = len(matched) >= 3
        boosted_by_projects = len(matched) >= 2 and has_projects_or_internships

        if prediction == 1 and (enough_skills or boosted_by_projects):
            final_decision = "Selected"
        else:
            final_decision = "Rejected"

        results.append({
            "role": role,
            "match_score": match_score,
            "prediction": final_decision,
            "matched_skills": matched,
            "missing_skills": missing,
            "suggestions": [f"Learn {skill}" for skill in missing] if missing else [],
            "qualification_required": role_qualification_map[role],
            "candidate_qualification": normalized_qual,
            "has_projects_or_internships": has_projects_or_internships
        })

    return results
