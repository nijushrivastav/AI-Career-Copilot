import google.generativeai as genai
import json
import os

# Gemini API Key 
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def analyze_resume(resume_text, user_goal):
    prompt = f"""
You are a senior software engineer and hiring manager.
    
Evaluate the resume based on the user's goal
    
User goal: "{user_goal}"
    
STRICT RULES:
- Give Resume Score out of 100
- Give ATS Score out of 100
- Extract only relevant skills for this goal
- Identify at least 5 missing skills
- Generate at least 5 roadmap steps
- Generate at least 5 interview questions
- Return ONLY valid JSON
- Do not return markdown

Return only JSON:
{{
  "resume_score": 0,
  "ats_score": 0,
  "skills": [],
  "missing_skills": [],
  "roadmap": [],
  "interview_questions": []
}}
Resume:
{resume_text}

"""
   
    try:
        response = model.generate_content(prompt)

        content = response.text.strip()

        # Gemini kabhi ```json ``` wrap kar deta hai
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

        return json.loads(content)

    except Exception as e:
        return {
    "resume_score": 0,
    "ats_score": 0,
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": [],
    "error": str(e)
}