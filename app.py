from flask import Flask, render_template, request, send_from_directory, send_file
import os

app = Flask(__name__)

# Path to the folder where question papers are stored
QUESTION_PAPERS_DIR = os.path.join(os.path.dirname(__file__), 'question_papers')

# Route to the home page (where user selects the year and pattern)
@app.route('/')
def index():
    # List BE and TE engineering years
    engineering_years = os.listdir(QUESTION_PAPERS_DIR)
    return render_template('index.html', engineering_years=engineering_years)

# Route to get available patterns for the selected engineering year (BE or TE)
@app.route('/patterns', methods=['GET'])
def patterns():
    engineering_year = request.args.get('engineering_year')
    patterns = os.listdir(os.path.join(QUESTION_PAPERS_DIR, engineering_year))
    return {'patterns': patterns}

# Route to get available subjects for a selected year and pattern
@app.route('/subjects', methods=['GET'])
def subjects():
    engineering_year = request.args.get('engineering_year')
    pattern = request.args.get('pattern')
    pattern_path = os.path.join(QUESTION_PAPERS_DIR, engineering_year, pattern)
    
    subjects = []
    for subject in os.listdir(pattern_path):
        subject_path = os.path.join(pattern_path, subject)
        if os.path.isdir(subject_path):  # Only include directories (subjects)
            subjects.append(subject)
    
    return {'subjects': subjects}

# Route to get available papers (PDFs) for a selected subject
@app.route('/papers', methods=['GET'])
def papers():
    engineering_year = request.args.get('engineering_year')
    pattern = request.args.get('pattern')
    subject = request.args.get('subject')
    
    subject_path = os.path.join(QUESTION_PAPERS_DIR, engineering_year, pattern, subject)
    papers = [f for f in os.listdir(subject_path) if f.endswith('.pdf')]
    
    return {'papers': papers}

# Route to download the selected paper
@app.route('/download')
def download():
    engineering_year = request.args.get('engineering_year')
    pattern = request.args.get('pattern')
    subject = request.args.get('subject')
    paper = request.args.get('paper')
    
    filepath = os.path.join(QUESTION_PAPERS_DIR, engineering_year, pattern, subject, paper)
    return send_from_directory(os.path.dirname(filepath), os.path.basename(filepath), as_attachment=True)

# Route to view the selected paper
@app.route('/view')
def view():
    engineering_year = request.args.get('engineering_year')
    pattern = request.args.get('pattern')
    subject = request.args.get('subject')
    paper = request.args.get('paper')
    
    filepath = os.path.join(QUESTION_PAPERS_DIR, engineering_year, pattern, subject, paper)
    return send_file(filepath)

if __name__ == '__main__':
    app.run(debug=True)
