# AI Career Copilot 🚀

AI Career Copilot is an AI-powered Resume Analysis and Career Guidance web application built using Flask, Gemini AI, SQLAlchemy, and TiDB Cloud.

The application helps users analyze resumes, calculate ATS scores, identify missing skills, generate career roadmaps, provide interview questions, maintain report history, and download professional PDF reports.

---

## Features

### Authentication System

* User Signup
* User Login
* User Logout
* Session Management

### Resume Analysis

* Upload Resume in PDF format
* Upload Resume in DOCX format
* Paste Resume Text Manually
* AI-powered Resume Evaluation

### AI Insights

* Resume Score (0–100)
* ATS Score (0–100)
* Skills Identification
* Missing Skills Detection
* Personalized Learning Roadmap
* Interview Questions Generation

### Report Management

* Store Reports in Database
* View Analysis History
* Download Analysis Report as PDF

### Database

* TiDB Cloud Integration
* SQLAlchemy ORM
* User and Report Management

---

## Tech Stack

### Frontend

* HTML5
* CSS3
* Jinja2 Templates

### Backend

* Python
* Flask

### AI

* Google Gemini API (Gemini 2.5 Flash)

### Database

* TiDB Cloud
* SQLAlchemy
* PyMySQL

### PDF Generation

* ReportLab

### File Processing

* PyPDF2
* Python-Docx

---

## Project Structure

```text
AI-Career-Copilot/
│
├── app.py
├── ai.py
├── db.py
├── models.py
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   └── history.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd AI-Career-Copilot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
DATABASE_URL=YOUR_TIDB_DATABASE_URL
```

---

## Run Application

```bash
python app.py
```

Open browser:

```text
http://127.0.0.1:5000
```

---

## Future Improvements

* Resume vs Job Description Matching
* Skill Gap Visualization
* Career Recommendation Engine
* Resume Improvement Suggestions
* Dark Mode
* Email Report Delivery
* Admin Dashboard
* Multi-language Support

---

## Author

**Niju Shrivastava**

B.Tech Computer Science Engineering Student

Passionate about AI, ML, Software Development, and Software Engineering.

---

## License

This project is created for educational and portfolio purposes.
