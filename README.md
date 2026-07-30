<div align="center">

# 🪄 Resume Wizard

> **An AI-powered Resume Generator & Job Finder built with Streamlit, LangChain, Gemini, and Tavily.**

Resume Wizard is an intelligent web application that generates professional, ATS-friendly resumes from user-provided information using Google's Gemini models through LangChain. After creating the resume, the application automatically searches for the latest job opportunities that best match the candidate's profile using Tavily Search.

The project also features a configurable prompt-based styling system, allowing users to customize the resume's tone, structure, and formatting without changing the application's source code.

</div>

---

## 🌐 Live Demo

https://resume-wizard-sus-tushhhh.streamlit.app/

---

# ✨ Features

- 🤖 AI-powered resume generation
- 📄 ATS-friendly resume creation
- 🎨 Configurable prompt-based resume styling
- 🌐 Automatic job search based on generated resume
- 🔍 Fetches latest job opportunities using Tavily Search
- ⚡ Powered by Google Gemini through LangChain
- 🖥️ Interactive web interface built with Streamlit
- 🧩 Easy to customize and extend

---

# 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **LangChain**
- **Google Gemini**
- **Tavily Search API**

---

# 🚀 Workflow

1. User fills in their information through the Streamlit interface.
2. LangChain structures the input.
3. Gemini generates a professional ATS-friendly resume.
4. The application extracts relevant skills and target job roles.
5. Tavily searches the web for recent matching job opportunities.
6. Resume and matching jobs are displayed within the Streamlit application.

---

# 🔧 Installation

Clone the repository

```bash
git clone https://github.com/your-username/resume-wizard.git

cd resume-wizard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` file

```toml
[api_key]
GOOGLE_API_KEY="your_google_api_key"
TAVILY_API_KEY="your_tavily_api_key"
```

Run the application

```bash
streamlit run app.py
```

---

# 📋 Example Flow

### Input

- Personal Information
- Education
- Skills
- Work Experience
- Projects
- Certifications
- Achievements
- Target Job Role

↓

### Output

- ATS-Friendly Resume
- Prompt-Based Customized Resume Style
- Latest Matching Job Opportunities

---

# 📄 License

This project is licensed under the MIT License.

---

# 🙏 Acknowledgements

- Streamlit
- LangChain
- Google Gemini
- Tavily Search API
- Python Community

---

## 👨‍💻 Developer

**Tushant**  
🔗 GitHub: https://github.com/sus-tushhhh
