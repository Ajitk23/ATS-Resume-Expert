import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as sl 

import os

from PIL import Image 
import pdf2image
import google.generativeai as genai 



genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content(input,pdf_content[0],prompt)
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page = images[0]
        
        # converting to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                'mime_type': "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
    

# Streamlit App

sl.set_page_config(page_title="ATS RESUME EXPERT")
sl.header("ATS Tracking System")
input_text = sl.text_area("Job Description: ", key="input")
uploaded_file = sl.file_uploader("upload your resume(pdf format only)", type = ["pdf"])

if uploaded_file is not None:
    sl.write("PDF Uploaded Successfully!")
    
submit1 = sl.button("Tell me breiefly about the uploaded Resume")
submit2 = sl.button("How Can i Improvise my skills")
submit3 = sl.button("% Mathed")
        
input_prompt1 = """
You are an experienced Senior HR Manager with tech and staffing experience in the filed of IT Recruitments, Data science, web developer, software engineer, 
devops, big data, machine learning, Data analyst, project manager etc. Your task is here to review the uploaded resume against the job description.
Also share your alpha professional evaluation on whether the candidate's profile align with the job description and highlight the strengths and weakness of the applicant
in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled deep ATS or Application Tracking system scanner with a deep understanding of IT Recruitments, Data science, web developer, software engineer, 
devops, big data, machine learning, Data analyst, project manager etc. your task is to evaluate the resume against the provided job description. Give me the percentage of matching of the 
resume with given job description. 
first the out put should come as percentage of matching with job description and then keywords missing in the resume that has mentioned in job description.
"""

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        sl.subheader("The response is")
        sl.write(response)
    else:
        sl.write("Please upload a resume")
        
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        sl.subheader("The response is")
        sl.write(response)
    else:
        sl.write("Please upload a resume")