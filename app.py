from flask import Flask, render_template, request, redirect, url_for
import os
from parser.resume_parser import parse_resume
from predict.new_predict import clean_text, predict_for_multiple_roles
from predict.model_paths import role_model_paths, role_skill_map, role_qualification_map

app = Flask(__name__)

# Folder to save uploaded resumes temporarily
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Start with roles from the existing model paths and allow dynamic changes during runtime
dynamic_roles = list(role_model_paths.keys())

# Helper to add a new role with empty placeholders if missing from model_paths etc.
def add_new_role_placeholder(role_name):
    if role_name not in role_model_paths:
        role_model_paths[role_name] = None  # You can later set the actual model file path
    if role_name not in role_skill_map:
        role_skill_map[role_name] = []
    if role_name not in role_qualification_map:
        role_qualification_map[role_name] = []

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        files = request.files.getlist('resumes')
        selected_roles = request.form.getlist('roles')

        # Input validations
        if not selected_roles:
            return "Please select at least one role."

        if not files or all(f.filename == '' for f in files):
            return "Please upload at least one resume."

        all_results = []
        saved_file_paths = []

        # Ensure roles in dynamic_roles have model/skill/qualification entries
        for role in selected_roles:
            add_new_role_placeholder(role)

        for file in files:
            if file and file.filename:
                filename = file.filename
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                # Save uploaded resume temporarily
                file.save(file_path)
                saved_file_paths.append(file_path)

                try:
                    # Parse resume and extract text + info
                    result = parse_resume(file_path)
                    raw_text = result.get('full_text', '')
                    cleaned_text = clean_text(raw_text)

                    contact_info = result.get('contact_info', {})
                    name = contact_info.get('name', "Name not found")
                    phone = contact_info.get('phone', "Phone not found")
                    email = contact_info.get('email', "Email not found")

                    # Combine education list into string
                    education_list = result.get('education', [])
                    qualification_text = " ".join(education_list) if isinstance(education_list, list) else str(education_list)

                    # Predict roles match for the uploaded resume
                    prediction_results = predict_for_multiple_roles(
                        resume_skills=result.get('skills', []),
                        resume_experience=result.get('experience', []),
                        resume_certifications=result.get('certifications', []),
                        resume_qualification=qualification_text,
                        resume_projects=result.get('projects', []),
                        resume_internships=result.get('internships', []),
                        resume_text=cleaned_text,
                        selected_roles=selected_roles,
                        role_model_paths=role_model_paths,
                        role_skill_map=role_skill_map,
                        role_qualification_map=role_qualification_map
                    )

                    all_results.append({
                        'filename': filename,
                        'name': name,
                        'phone': phone,
                        'email': email,
                        'predictions': prediction_results
                    })

                except Exception as e:
                    all_results.append({
                        'filename': filename,
                        'name': 'Error parsing',
                        'phone': 'Error',
                        'email': 'Error',
                        'predictions': [{
                            'role': 'N/A',
                            'match_score': 0,
                            'prediction': 'Error',
                            'matched_skills': [],
                            'missing_skills': [],
                            'suggestions': [str(e)],
                            'qualification_required': 'N/A',
                            'candidate_qualification': 'N/A'
                        }]
                    })

        # Clean up uploaded files after processing
        for path in saved_file_paths:
            try:
                os.remove(path)
            except Exception as e:
                print(f"Error deleting file {path}: {e}")

        return render_template('results.html', all_results=all_results)

    # GET request - render home with current roles
    return render_template('home.html', all_roles=dynamic_roles)

@app.route('/add_role', methods=['POST'])
def add_role():
    new_role = request.form.get('new_role', '').strip()
    if new_role and new_role not in dynamic_roles:
        dynamic_roles.append(new_role)
        add_new_role_placeholder(new_role)
    return redirect(url_for('home'))

@app.route('/delete_role/<role_name>', methods=['POST'])
def delete_role(role_name):
    if role_name in dynamic_roles:
        dynamic_roles.remove(role_name)
        # Optionally remove placeholders for cleanliness, but be careful if models exist
        # role_model_paths.pop(role_name, None)
        # role_skill_map.pop(role_name, None)
        # role_qualification_map.pop(role_name, None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
