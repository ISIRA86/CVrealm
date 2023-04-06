from flask import Flask, render_template, request
from pdf2image import convert_from_path
import os
import spacy
import tempfile
import pytesseract
from PIL import Image

app = Flask(__name__,static_url_path='/static')

# Load the Spacy model
nlp = spacy.load(r'C:\Users\Gigabyte\AppData\Local\Programs\Python\Python39\Lib\site-packages\en_core_web_sm', disable=['parser', 'ner', 'tagger'])


job_roles = {
    'Software Engineer': ['Python', 'Java', 'JavaScript', 'C++', 'SQL'],
    'Data Scientist': ['Python', 'R', 'SQL', 'Machine Learning', 'Data Visualization'],
    'Web Developer': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular']
}

courses = {
    'Python for Data Science': ['Python', 'Data Science', 'Machine Learning'],
    'Web Development Bootcamp': ['HTML', 'CSS', 'JavaScript', 'React', 'Angular'],
    'SQL Fundamentals': ['SQL', 'Database Management']
}


# OCR function
def ocr(file):
    with tempfile.TemporaryDirectory() as path:
         # Convert PDF to images
        images = convert_from_path(file, output_folder=path, dpi=300)
        text = ''
        for i, img in enumerate(images):
            # Save each image temporarily
            img_path = os.path.join(path, f'{i}.png')
            img.save(img_path, 'PNG')
            # Apply OCR
            text += pytesseract.image_to_string(Image.open(img_path))
    return text

# Route to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Route to result.html
@app.route('/result', methods=['POST'])
def result():
    # Get the file from the request
    file = request.files['cv']
    # Save the file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp_file.name)
    # Check if the file is a PDF or image
    if file.filename.endswith('.pdf'):
        text = ocr(temp_file.name)
    elif file.filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        text = pytesseract.image_to_string(Image.open(temp_file.name))
    else:
        return render_template('error.html', message='Invalid file format. Please upload a PDF or image.')
    # Load the text into Spacy
    doc = nlp(text)
    # Extract skills
    skills = []
    for ent in doc.ents:
        if ent.label_ == 'SKILL':
            skills.append(ent.text)
    # Determine job role
    if 'machine learning' in skills:
        job_role = 'Machine Learning Engineer'
    elif 'web development' in skills:
        job_role = 'Web Developer'
    else:
        job_role = 'Unknown'
    # Return the result
    return render_template('result.html', skills=skills, job_role=job_role)

if __name__ == '__main__':
    app.run(debug=True)
