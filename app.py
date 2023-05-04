# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for, jsonify
import util
import PyPDF2
import io

# Initialize the Flask application
app = Flask(__name__)

# Define the route for processing data
@app.route('/hello', methods=['GET'])
def process():
    return {
        "res": "Hello, World",
    }

@app.route('/resume', methods=['POST'])
def process_resume():
    pdf_file = "/users/shashank/Downloads/" + request.json['resume']
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))

    # Read the content of the PDF file and store it in a single string
    pdf_content = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_content += page.extract_text()

    resume = pdf_content
    print(resume)

    job_desc = request.json['job_desc']
    clean_resume = util.clean_string(resume)
    clean_job_desc = util.clean_string(job_desc)
    resume_skills = util.get_skills(clean_resume)
    job_skills = util.get_skills(clean_job_desc)

    score = 0
    for x in job_skills:
        if x in resume_skills:
            score += 1
    req_skills_len = len(job_skills)
    match = round(score / req_skills_len * 100, 1)
    print("done", match)

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "match": match
    }


# Run the application
if __name__ == '__main__':
    app.run(debug=True)

