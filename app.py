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
                no markdown allowed
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

    # with open('resume.html', 'w') as f:
    #     f.write(final_code)

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

st.set_page_config(layout='wide')

st.header("🪄 Resume Wizard")