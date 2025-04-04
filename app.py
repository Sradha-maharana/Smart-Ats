import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf




from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Gemini Pro Response
def get_gemini_response(input_text):
    model = genai.GenerativeModel("gemini-2.0-flash-lite")

    response = model.generate_content(input_text)
    return response.text

# Extract text from PDF
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Streamlit App
st.title("Smart ATS")
st.text("Improve Your Resume ATS")

jd = st.text_area("Paste the Job Description")
uploaded_file = st.file_uploader("Upload your resume", type=["pdf"], help="Please upload a PDF")

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        
        input_prompt = f"""
        Hey, act like a skilled and experienced ATS (Applicant Tracking System) with a deep understanding of the tech field, software engineering, data science, data analysis, and big data engineering.
        Your task is to evaluate the resume based on the given job description.
        
        Consider that the job market is very competitive, and you should provide the best assistance for improving the resume.
        Assign the percentage match based on the JD and list the missing keywords with high accuracy.
        
        Resume: {text}
        Job Description: {jd}
        
        I want the response in one single string with the structure:
        {{"JD Match":"%", "MissingKeywords":[], "Profile Summary":""}}
        """

        response = get_gemini_response(input_prompt)
        st.subheader("AI ATS Evaluation")
        st.text(response)
