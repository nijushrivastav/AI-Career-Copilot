from flask import Flask, render_template, request, redirect, session
from db import Base, engine, Sessionlocal
from ai import analyze_resume
import models
import PyPDF2
import docx
import json
from flask import send_file
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
app = Flask(__name__)
app.secret_key ="secret123"

Base.metadata.create_all(bind=engine)


#HOME
@app.route("/")
def home():
   if "user" in session:
       return redirect("/dashboard")
   return redirect("/login")

#-----SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    db = Sessionlocal()

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        existing_user = db.query(models.User).filter_by(email=email).first()
        if existing_user:
            return "user already exists"
        
        user = models.User(email=email, password=password)
        db.add(user)
        db.commit()
         
        return redirect("/login")
    
    return render_template("signup.html")

#LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    db = Sessionlocal()
    
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.query(models.User).filter_by(email=email, password=password).first()
        
        if user:
            session["user"] = user.email
            return redirect("/dashboard")
        else:
            return "Invalid credentials"
        
    return render_template("login.html")


#DASHBOARD
@app.route("/dashboard", methods =["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect("/login") 
    
    result = None
    
    if request.method == "POST":
        user_goal = request.form.get("role")
        resume_text = request.form.get("resume")
        
        file = request.files.get("file")
        
        #file handling
        if file and file.filename != "":
            if file.filename.endswith(".pdf"):
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() or ""
                        resume_text = text
                except Exception as e:
                    result = {"error": f"PDF error: {str(e)}"}
                     
            elif file.filename.endswith(".docx"):
                try:
                      doc = docx.Document(file)
                      text = ""
                      for para in doc.paragraphs:
                          text += para.text +"\n"
                          resume_text = text
                except Exception as e: 
                    result = {"error:" f"Docx error: {str(e)}"}      
        
        if resume_text and user_goal:
           try:
            result = analyze_resume(resume_text, user_goal)
            session["last_result"] = json.dumps(result)
            
            #save to database
            db = Sessionlocal()
            user = db.query(models.User).filter_by(email=session["user"]).first()
            
            report = models.Reports(
                user_id = user.id,
                resume_text = resume_text,
                result = json.dumps(result)
            )
            
            db.add(report)
            db.commit()
            
           except Exception as e:
            result = {"error": f"AI error: {str(e)}"}  
            
    return render_template(
        "dashboard.html",
        user = session["user"],
        result = result
    ) 
    
    
    
#history
@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")
    
    db = Sessionlocal()
    user = db.query(models.User).filter_by(email=session["user"]).first()
    
    reports = db.query(models.Reports).filter_by(user_id = user.id).all()
    
    #convert  JSON string > dict
    pasred_reports = []
    for r in reports:
        try:
            pasred_result = json.loads(r.result)
        except:
            pasred_result = []
            
        pasred_reports.append({
            "resume": r.resume_text,
            "result": pasred_result
        })
        
    return render_template("history.html", reports=pasred_reports)
        
  #logout route
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")
  
#For PDF
@app.route("/download-report")
def download_report():

    if "last_result" not in session:
        return "No report available"

    result = json.loads(session["last_result"])

    pdf_file = "report.pdf"

    doc = SimpleDocTemplate(pdf_file)

    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Career Copilot Report", styles["Title"]))

    content.append(
        Paragraph(
            f"Resume Score: {result.get('resume_score',0)}/100",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"ATS Score: {result.get('ats_score',0)}/100",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(Paragraph("Skills", styles["Heading2"]))

    for item in result.get("skills", []):
        content.append(Paragraph("• " + str(item), styles["Normal"]))

    content.append(Paragraph("Missing Skills", styles["Heading2"]))

    for item in result.get("missing_skills", []):
        content.append(Paragraph("• " + str(item), styles["Normal"]))

    content.append(Paragraph("Roadmap", styles["Heading2"]))

    for item in result.get("roadmap", []):
        content.append(Paragraph("• " + str(item), styles["Normal"]))

    content.append(Paragraph("Interview Questions", styles["Heading2"]))

    for item in result.get("interview_questions", []):
        content.append(Paragraph("• " + str(item), styles["Normal"]))

    doc.build(content)

    return send_file(
        pdf_file,
        as_attachment=True
    )

      
if __name__ == "__main__":
    app.run(debug=True)

