import streamlit as st
import requests
import json
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Set Streamlit page configuration first
st.set_page_config(page_title="Career Clarity Hub", page_icon="📄", layout="wide")

# Load environment variables
load_dotenv()

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, Dataset, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, Dataset, prompt])
    return response.text
#css 
with open("style.css") as source:
    st.markdown(f"<style>{source.read()}</style>", unsafe_allow_html=True)

st.markdown('<h1 class="title" style="background-color:#4a2b7a; color:#FFFF9E; border-radius:10px;">Career Clarity Hub<h1>', unsafe_allow_html=True)
#st.markdown('<img src="RoboChecking.jpeg" alt="image of a robo" width="500" height="200"' />,unsafe_allow_html=True)
st.components.v1.iframe("https://lottie.host/embed/dc2478c0-452f-447b-aa01-93a123bb8301/AzpnSbHPvm.json", height=300)

# Set API Key
RAPIDAPI_KEY = '95e7a83b41msh254814734f17e9dp197ce7jsn95d16420dd39'  # Replace with correct API key
RAPIDAPI_HOST = 'linkedin-data-api.p.rapidapi.com'

# Streamlit UI
st.title("LinkedIn Profile Data Extractor")

# User Input
linkedin_profile_url = st.text_input("Enter LinkedIn Profile URL:")

# Initialize session state for formatted_text1
if 'formatted_text1' not in st.session_state:
    st.session_state['formatted_text1'] = ""

if st.button("Fetch Data"):
    if linkedin_profile_url:
        # Define API URL & Headers
        url = "https://linkedin-data-api.p.rapidapi.com/get-profile-data-by-url"
        headers = {
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": RAPIDAPI_HOST,
            "Content-Type": "application/json"
        }
        params = {"url": linkedin_profile_url}  # Pass profile URL

        # API Request with Error Handling
        try:
            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                st.subheader("Extracted Profile Data:")
                #st.json(data)  # Display raw JSON data

                # Function to format profile data dynamically
                def format_profile_data(data):
                    # Basic Profile Information
                    text = f"Name: {data.get('firstName', 'N/A')} {data.get('lastName', 'N/A')}\n"
                    text += f"Headline: {data.get('headline', 'N/A')}\n"
                    text += f"Location: {data.get('geo', {}).get('full', 'N/A')}\n"
                    text += f"Summary: {data.get('summary', 'N/A')}\n\n"

                    # Education
                    text += "Education:\n"
                    for edu in data.get('educations', []):
                        text += f"  - {edu.get('degree', 'N/A')} in {edu.get('fieldOfStudy', 'N/A')} at {edu.get('schoolName', 'N/A')} "
                        text += f"({edu.get('start', {}).get('year', 'N/A')} - {edu.get('end', {}).get('year', 'N/A')})\n"
                    text += "\n"

                    # Experience (Positions)
                    text += "Experience:\n"
                    for exp in data.get('position', []):
                        text += f"  - {exp.get('title', 'N/A')} at {exp.get('companyName', 'N/A')} "
                        text += f"({exp.get('start', {}).get('year', 'N/A')} - {exp.get('end', {}).get('year', 'N/A')})\n"
                    text += "\n"

                    # Skills
                    text += "Skills:\n"
                    skills = [skill.get('name', 'N/A') for skill in data.get('skills', [])]
                    text += f"  - {', '.join(skills)}\n\n"

                    # Certifications
                    text += "Certifications:\n"
                    for cert in data.get('certifications', []):
                        text += f"  - {cert.get('name', 'N/A')} by {cert.get('authority', 'N/A')}\n"
                    text += "\n"

                    # Projects
                    text += "Projects:\n"
                    for project in data.get('projects', {}).get('items', []):
                        text += f"  - {project.get('title', 'N/A')}\n"
                        text += f"    Description: {project.get('description', 'N/A')}\n"
                        text += f"    Duration: {project.get('start', {}).get('year', 'N/A')} - {project.get('end', {}).get('year', 'N/A')}\n"
                    text += "\n"

                    return text

                # Get Formatted Text
                formatted_text = format_profile_data(data)
                st.subheader("Formatted Data:")
                st.session_state['formatted_text1'] = formatted_text
                st.text(formatted_text)  # Display formatted text data

            else:
                st.error(f"Failed to fetch data: {response.status_code}")
                st.text(f"Response: {response.text}")  # Show the exact API error response

        except requests.exceptions.RequestException as e:
            st.error(f"API Request Error: {e}")

    else:
        st.warning("Please enter a valid LinkedIn Profile URL.")

# Job Description Input


# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
input_text = st.text_area("Enter The Job Description Of Your Desired Job:", key="input", height=150)
st.markdown('</div>', unsafe_allow_html=True)
#input_text = st.text_area("Enter The Job Description Of Your Desired Job:", key="input", height=150)
st.markdown("<h3>Click the Buttons Below & Wait for the Amazing Result of Your Resume</h3>",unsafe_allow_html=True)
st.markdown("___")
#if uploaded_files is not None:
  #  st.write("PDF Uploaded Successfully")
st.components.v1.iframe("https://lottie.host/embed/2c94fbf2-b141-4d33-afa7-fc0dcc8ec1d8/D7nHn6herj.json",height=180)
submit1 = st.button("Strength and weakness")
submit2 = st.button("Skill Gap Analysis and Learning Resources")
submit3 = st.button("Percentage match")
submit4 = st.button("Interview question's")
submit6 = st.button("Job suggestions based on your skills")

input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided data against the job description. 
 Please share your professional evaluation on whether the candidate's profile aligns with the role.  
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """ You are a experinced  career mentor, First the output should come as candidate name highlight     it  and  identify the skills that are missing in thedata based on job discription.
and suggest how can the candidate improve missing  skills along with some platforms,popular options along with links  with some small discription
"""

input_prompt3 = """
   You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
   your task is to evaluate the data against the provided job description. give me the percentage of match if the data matches
   the job description. First the output should come as candidate firstName and lastName  and percentage and last final thoughts .
   """
input_prompt4 = """You are an experienced Technical Human Resource Manager, your task is to generate interview questions for a candidate based on this job description and data and make sure that provide answers for each at the end """
input_prompt6 = """ You are a experinced  career mentor adn recruitment consultant, your task is to identify the skills in the data and provide job suggestion that he is suitable for that and the output should be job role, list of companies and link for applying if that company is currently in recruiting  """

if submit1:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt1, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")

if submit2:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt2, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")
if submit3:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt3, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")
if submit4:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt4, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")

if submit6:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt6, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")



#         streamlit 
# google-generativeai
# python-dotenv