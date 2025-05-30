from parser.resume_parser import parse_resume
from predict.new_predict import clean_text, predict_for_multiple_roles
from predict.model_paths import role_model_paths, role_skill_map, role_qualification_map
from visualize import plot_grouped_bar_chart, plot_lollipop_chart

if __name__ == "__main__":
    file_path = "data/resume2.pdf"
    result = parse_resume(file_path)

    # Extract structured parts
    resume_skills = result.get('skills', [])
    resume_experience = result.get('experience', [])
    resume_certifications = result.get('certifications', [])
    resume_projects = result.get('projects', [])
    resume_internships = result.get('internships', [])
    resume_qualification = result.get('qualification', 'Unknown')
    raw_text = result.get('full_text', '')

    print("Contact Info:", result.get('contact_info', {}))
    print("Skills:", resume_skills)
    print("Education:", result.get('education', []))
    print("Experience:", resume_experience)
    print("Certifications:", resume_certifications)
    print("Projects:", resume_projects)
    print("Internships:", resume_internships)
    print("Qualification:", resume_qualification)

    # Clean the full text
    cleaned_text = clean_text(raw_text)

    selected_roles = list(role_model_paths.keys())

    prediction_results = predict_for_multiple_roles(
        resume_skills,
        resume_experience,
        resume_certifications,
        cleaned_text,
        resume_qualification,
        resume_projects,
        resume_internships,
        selected_roles,
        role_model_paths,
        role_skill_map,
        role_qualification_map
    )

    for res in prediction_results:
        print(f"\nRole: {res['role']}")
        print(f"Match Score: {res['match_score']}%")
        print(f"Prediction: {res['prediction']}")
        print(f"Matched Skills: {res['matched_skills']}")
        print(f"Missing Skills: {res['missing_skills']}")
        print(f"Suggestions: {res['suggestions']}")
        print(f"Required Qualification: {res['qualification_required']}")
        print(f"Candidate Qualification: {res['candidate_qualification']}")
        print(f"Has Projects/Internships: {'Yes' if res.get('has_projects_or_internships') else 'No'}")
        print("-" * 40)

    # Optional visualizations
    plot_grouped_bar_chart(prediction_results)
    plot_lollipop_chart(prediction_results)
