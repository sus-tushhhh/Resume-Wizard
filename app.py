# Step 1 : Load Modules
import pytesseract
import streamlit as st
from tavily import TavilyClient
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.tools import tool

import pandas as pd
import numpy as np
import base64
from io import BytesIO
import time

from PIL import Image

import warnings
warnings.filterwarnings('ignore')


# Backend ----------------------------------------------------------------------------------------------

# Step 2 : Create models and clients
gemini_model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=st.secrets.api_key.GOOGLE_API_KEY
)

groq_model = ChatGroq(
    model="qwen/qwen3.6-27b",
    api_key=st.secrets.api_key.GROQ_API_KEY
)

tavily_client = TavilyClient(
    api_key=st.secrets.api_key.TAVILY_API_KEY
)


# Step 3 : Tools
@tool
def search_latest_jobs(query: str) -> dict:
    """This function helps to fetch latest news or jobs related articles using tavily"""

    return tavily_client.search(query)


# Step 4 : Agent
agent = create_agent(
    model=gemini_model,
    tools=[search_latest_jobs]
)


# Step 5 : Main Agent for Resume making
def main_agent(query: str, agent = agent):
    """This is a main agent or leader agent orchestrate sub agent"""

    prompt = """You are AI Assistant and below is a prompt, your task is to give detailed prompt for this.
                You are a professional resume generator where user will give their personal information,
                and you have to create a detailed resume for students or professional one,
                it must be with dynamic UI and UX and make sure to give output in HTML format only with
                advance and professional CSS Designing
                add a placeholder for user image which i can easily replace with replace function of python with my
                image path and write placeholder as USER_IMAGE_PATH_PLACEHOLDER.
                no markdown allowed, and don't use javascript only html and css
                strictly don't write html after ```
    """

    response = agent.invoke({'messages':[{'role':'user', 'content':prompt}]})
    advanced_prompt  = response['messages'][-1].text

    user_details = f""" Below given is user details, generate resume based on that, 
                        if not given keep: Default resume as python developer,
                        user details : {query}

    """

    final_prompt = prompt + advanced_prompt + user_details
    final_response = agent.invoke({'messages':[{'role':'user', 'content':final_prompt}]})
    final_code = (final_response['messages'][-1].text).strip('```')

    with open('resume.html', 'w', encoding='utf-8') as f:
        f.write(final_code)

    return final_code


# Step 6 : Job searching agent
def get_jobs(agent = agent, location = "Delhi", profile = "Data Analyst, AI Engineer", config = None):

    prompt = f"""Bsed on user given job profile, fetch latest jobs or job apply articles
    using naukri, linkedin, indeed, or all popular platforms, show results with job profile name,
    location, salary, company name, apply link, show jobs only related to {location} and {profile}.
    Output must be in professional HTML Naukri theme cards with dynamic design, show atleast top 10-20
    results with direct apply link and don't write html after ```                
    """ + ('.' if not config else config)

    response = agent.invoke({'messages' : [{'role': 'user', 'content': prompt}]})
    code = (response['messages'][-1].text).strip('```')

    return code


# Frontend------------------------------------------------------------------------------------------------

icon = """<svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#75FBFD"><path d="m646-438-86 138q-11 17-30.5 14T505-309l-28-112-273 273q-11 11-27.5 11.5T148-148q-11-11-11-28t11-28l273-274-112-28q-20-5-23-24.5t14-30.5l138-85-12-163q-2-20 16-29t33 4l125 105 151-61q19-8 33 6t6 33l-61 151 105 124q13 15 4 33t-29 16l-163-11ZM134-706q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6l-52-52Zm421 263 48-79 93 7-60-71 35-86-86 35-71-59 7 92-79 49 90 22 23 90Zm151 309-52-52q-6-6-6-14t6-14l52-52q6-6 14-6t14 6l52 52q6 6 6 14t-6 14l-52 52q-6 6-14 6t-14-6ZM569-570Z"/></svg>"""

st.set_page_config(layout='wide', 
                   page_title='Resume Wizard', 
                   page_icon=icon,
                   initial_sidebar_state='expanded'
)


st.title("🪄 Resume Wizard &nbsp;|&nbsp; :green[AI Resume Builder]", text_alignment='center')
st.sidebar.title("User Details", text_alignment='center')


user_image_placeholder = st.sidebar.empty()
uploaded_image = st.sidebar.file_uploader("", type=['jpg', 'jpeg', 'png'], label_visibility="hidden")

if uploaded_image:
    img = Image.open(uploaded_image)
    user_image_placeholder.image(img)
    image_success_placeholder = st.sidebar.empty()
    image_success_placeholder.success('Image uploaded :)')
    time.sleep(2)
    image_success_placeholder.empty()
else:
    img = Image.open(r"assets/user_image_placeholder.png")
    user_image_placeholder.image(img)

st.sidebar.divider()

resume_desc = st.sidebar.text_area(label="Write resume description : ", placeholder="Name, Education, Experience ...")
styling_prompt = st.sidebar.text_area(label="Write styling prompt : ", placeholder="Theme, Design, Layout ...")


def img_to_base64():
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_bytes = buffer.getvalue()
    base64_string = base64.b64encode(img_bytes).decode("utf-8")
    return base64_string


if st.sidebar.button('Generate Resume'):
    with st.spinner():
        code = main_agent(query=resume_desc + styling_prompt)
        with st.container(border=True, horizontal_alignment='center'):
            st.html(code.replace('USER_IMAGE_PATH_PLACEHOLDER', f'data:image/png;base64,{img_to_base64()}'))


