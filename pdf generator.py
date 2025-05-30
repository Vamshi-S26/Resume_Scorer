from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Rahul Sharma - Resume', 0, 1, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, body)
        self.ln()

def create_resume_pdf(filename):
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("Contact Info:")
    pdf.chapter_body(
        "Email: rahul.sharma@example.com\n"
        "Phone: +91 98765 43210\n"
        "LinkedIn: linkedin.com/in/rahulsharma"
    )

    pdf.chapter_title("Objective:")
    pdf.chapter_body(
        "Aspiring Machine Learning Engineer with 2 years of experience in Python programming, TensorFlow, and model training. "
        "Looking to contribute in AI research and development."
    )

    pdf.chapter_title("Qualification:")
    pdf.chapter_body(
        "Bachelor of Technology in Computer Science and Engineering (2018-2022)\n"
        "University of Delhi"
    )

    pdf.chapter_title("Skills:")
    pdf.chapter_body(
        "Python, TensorFlow, Keras, Scikit-learn, Machine Learning, Data Analysis, Pandas, Numpy"
    )

    pdf.chapter_title("Education:")
    pdf.chapter_body(
        "- Bachelor of Technology in Computer Science and Engineering, University of Delhi, 2018-2022, 8.2 CGPA\n"
        "- Higher Secondary School, CBSE Board, 2016-2018, 90%"
    )

    pdf.chapter_title("Experience:")
    pdf.chapter_body(
        "- ML Intern at AI Labs (June 2021 - December 2021)\n"
        "  Developed predictive models using TensorFlow and improved accuracy by 15%.\n"
        "- Data Analyst at DataCorp (January 2022 - Present)\n"
        "  Worked on data cleaning, visualization, and report generation."
    )

    pdf.chapter_title("Certifications:")
    pdf.chapter_body(
        "- TensorFlow Developer Certificate, Google, 2022\n"
        "- Data Science Specialization, Coursera, 2021"
    )

    pdf.chapter_title("Projects:")
    pdf.chapter_body(
        "- Sentiment Analysis using BERT: Built a sentiment classifier using BERT transformer model achieving 90% accuracy.\n"
        "- Image Classification: Developed CNN-based image classifier on CIFAR-10 dataset."
    )

    pdf.chapter_title("Internships:")
    pdf.chapter_body(
        "- Machine Learning Intern, AI Labs, June 2021 to December 2021\n"
        "- Data Science Intern, Tech Solutions, January 2020 to May 2020"
    )

    pdf.chapter_title("Full Text:")
    pdf.chapter_body(
        "Aspiring Machine Learning Engineer skilled in Python, TensorFlow, Keras, and scikit-learn. "
        "Experienced in developing machine learning models and data analysis. "
        "Completed internships at AI Labs and Tech Solutions with hands-on experience in real-world projects including sentiment analysis and image classification. "
        "Certified TensorFlow Developer and Data Science Specialist."
    )

    pdf.output(filename)

if __name__ == "__main__":
    create_resume_pdf("sample_resume.pdf")
    print("sample_resume.pdf created successfully!")
