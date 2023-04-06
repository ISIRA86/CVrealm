import nltk
import spacy
import PyPDF2
import io
import pytesseract
from PIL import Image

# Load the pre-trained NLP model
nlp = spacy.load('en_core_web_sm')

# Define the job roles and their corresponding skills
job_roles = {
    'Software Engineer': {
        'skills': ['Python', 'Java', 'JavaScript', 'C++', 'SQL'],
        'courses': ['Python for Everybody', 'Java Programming and Software Engineering Fundamentals', 'JavaScript: Understanding the Weird Parts', 'C++ For C Programmers', 'SQL for Data Science']
    },
    'Data Scientist': {
        'skills': ['Python', 'R', 'SQL', 'Machine Learning', 'Data Visualization'],
        'courses': ['Python for Data Science', 'Data Science: R Basics', 'SQL for Data Analysis', 'Machine Learning', 'Data Visualization with ggplot2']
    },
    'Web Developer': {
        'skills': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular'],
        'courses': ['HTML, CSS, and JavaScript for Web Developers', 'Responsive Web Design', 'JavaScript Algorithms and Data Structures', 'React Tutorial and Projects Course', 'Angular - The Complete Guide (2021 Edition)']
    },
    'Product Manager': {
        'skills': ['Product Strategy', 'Product Development', 'Market Analysis', 'User Research', 'Agile Development'],
        'courses': ['Product Management Fundamentals', 'The Lean Product Playbook', 'Marketing Analytics: Products, Distribution and Sales', 'User Research and Design', 'Agile Project Management']
    },
    'UI/UX Designer': {
        'skills': ['User Interface Design', 'User Experience Design', 'Graphic Design', 'Web Design', 'Prototyping'],
        'courses': ['User Interface Design Fundamentals', 'UX Design Fundamentals', 'Graphic Design Basics: Core Principles for Visual Design', 'Web Design for Everybody: Basics of Web Development & Coding', 'Prototyping and Design']
    }
}

# Define a function to extract skills from the CV
def extract_skills(cv):
    skills = []
    doc = nlp(cv)
    for token in doc:
        if token.pos_ == 'NOUN' and token.text in job_roles.values():
            skills.append(token.text)
    return skills

# Define a function to suggest a job role based on the skills
def suggest_job_role(skills):
    job_role = ''
    max_match = 0
    for role, role_skills in job_roles.items():
        match = len(set(skills) & set(role_skills))
        if match > max_match:
            job_role = role
            max_match = match
    return job_role

# Define a function to suggest online courses based on job role and skills
def suggest_courses(job_role, skills):
    return job_roles[job_role]['courses']

# Get the PDF from the user
pdf_file = input("Enter the path to the PDF file: ")

# Open the PDF file and extract the text
pdf_file_obj = open(pdf_file, 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
num_pages = pdf_reader.numPages
text = ''
for i in range(num_pages):
    page = pdf_reader.getPage(i)
    page_content = page.extractText()
    if page_content:
        text += page_content
    else:
        img = page.getContents()['/Im0'].getObject()
        img_data = img.getData()
        img_stream = io.BytesIO(img_data)
        img_pil = Image.open(img_stream)
        img_text = pytesseract.image_to_string(img_pil, lang='eng')
        text += img_text

# Extract the skills from the CV
skills = extract_skills(text)

# Suggest a job role based on the skills
job_role = suggest_job_role(skills)
courses = suggest_courses(job_role, skills)

# Print the suggested job role
print("Based on your skills, you are suitable for the role of", job_role)
print("We recommend the following online courses to further develop your skills for this role:")
for course in courses:
    print(course)
