import json
from flask import jsonify
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from reportlab.platypus import HRFlowable

app = Flask(__name__)


# Home page
@app.route('/')
def home():
    return render_template('dashboard.html')


# Generate resume
@app.route('/generate', methods=['POST'])
def generate():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "linkedin": request.form['linkedin'],
        "degree": request.form['degree'],
        "college": request.form['college'],
        "year": request.form['year'],
        "schooling": request.form['schooling'],
        "job": request.form['job'],
        "company": request.form['company'],
        "description": request.form['description'],
        "certifications": request.form['certifications'],
        "awards": request.form['awards'],
        "skills": request.form['skills']
    }

    with open('data.json', 'w') as f:
        json.dump(data, f)

    return redirect(url_for('resume'))


# Resume page
@app.route('/resume')
def resume():
    with open('data.json') as f:
        data = json.load(f)

    return render_template('resume.html', data=data)
@app.route('/suggest', methods=['POST'])
def suggest():
    text = request.form.get('description', '')

    suggestions = []

    if len(text) < 50:
        suggestions.append("Add more details to your experience")

    if "worked" in text.lower():
        suggestions.append("Use action verbs like Developed, Built, Designed")

    if "python" not in text.lower():
        suggestions.append("Consider adding technical skills like Python")

    return jsonify({"suggestions": suggestions})
@app.route('/download')
def download():
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib import colors

    with open('data.json') as f:
        data = json.load(f)

    file_path = "resume.pdf"

    styles = getSampleStyleSheet()

    # Custom styles
    heading = ParagraphStyle(
        'Heading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.blue,
        spaceAfter=6,
        underlineWidth=1,
        underlineOffset=-2
    )

    normal = ParagraphStyle(
        'Normal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        spaceAfter=4
    )

    name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.black
    )

    story = []

    # Name
    story.append(Paragraph(data['name'], name_style))
    story.append(Paragraph(f"{data['email']} | {data['phone']}", normal))
    story.append(Paragraph(data['address'], normal))
    story.append(Paragraph(f"LinkedIn: {data['linkedin']}", normal))
    story.append(Spacer(1, 6))

    # Summary
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Professional Summary", heading))
    story.append(Paragraph(
        """Motivated and detail-oriented Computer Science student with strong foundation
in programming, web development and database management. Passionate about
learning new technologies and applying problem-solving skills to real-world projects.""",
        normal))

    # Education
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Education", heading))
    story.append(Paragraph(
        f"{data['degree']} - {data['college']} ({data['year']})", normal))

    # Schooling
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Schooling", heading))
    schooling = [ListItem(Paragraph(i, normal))
                 for i in data['schooling'].split('\n') if i.strip()]
    story.append(ListFlowable(schooling, bulletType='bullet'))

    # Experience
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Experience", heading))
    story.append(Paragraph(f"{data['job']} - {data['company']}", normal))
    exp = [ListItem(Paragraph(i, normal))
           for i in data['description'].split('\n') if i.strip()]
    story.append(ListFlowable(exp, bulletType='bullet'))

    # Certifications
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Certifications", heading))
    cert = [ListItem(Paragraph(i, normal))
            for i in data['certifications'].split('\n') if i.strip()]
    story.append(ListFlowable(cert, bulletType='bullet'))

    # Awards
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Awards & Achievements", heading))
    awards = [ListItem(Paragraph(i, normal))
              for i in data['awards'].split('\n') if i.strip()]
    story.append(ListFlowable(awards, bulletType='bullet'))

    # Skills
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black))
    story.append(Paragraph("Skills", heading))
    skills = [ListItem(Paragraph(i, normal))
              for i in data['skills'].split('\n') if i.strip()]
    story.append(ListFlowable(skills, bulletType='bullet'))

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=20,
        bottomMargin=20
    )

    doc.build(story)

    from flask import send_file
    return send_file(file_path, as_attachment=True)
    
# Run server
if __name__ == '__main__':
    app.run(debug=True)