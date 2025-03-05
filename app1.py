import streamlit as st
import requests
import json
from dotenv import load_dotenv

load_dotenv()

import os
import google.generativeai as genai

# Configure Gemini AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, Dataset, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, Dataset, prompt])
    return response.text

# Set API Key
RAPIDAPI_KEY = 'dcd5852aa7msh22a4ffca0dcca9fp1ee828jsn921fb28c961a'  # Replace with correct API key
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
input_text = st.text_area("Enter The Job Description Of Your Desired Job:", key="input", height=150)
submit3 = st.button("Percentage match")
input_prompt3 = """
   You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
   your task is to evaluate the data against the provided job description. give me the percentage of match if the data matches
   the job description. First the output should come as candidate firstName and lastName  and percentage and last final thoughts .
   """

if submit3:
    if st.session_state['formatted_text1']:
        response = get_gemini_response(input_prompt3, st.session_state['formatted_text1'], input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.warning("Please fetch LinkedIn profile data first.")