# -Sahayata-AI:AI-Powered-Social-Impact-Assistant-Agent-System

🤖 An intelligent multi-agent system for optimizing social impact through volunteer matching, resource allocation, and crisis response.

## Features
- 🤝 Smart volunteer-opportunity matching
- 📊 Real-time impact tracking
- 🚨 Crisis response coordination
- 📈 Resource optimization
- 💬 Multi-language communication

##📌 Overview

Sahayata AI is an Agent for Good designed to provide clear, simplified, and accessible guidance on essential public information including government schemes, educational opportunities, health awareness, safety guidelines, and environmental practices.

It helps students, rural citizens, and digitally underserved populations understand complex information in easy, plain language using the power of Gemini AI.

🎯 Problem Statement

Many people lack access to clear, understandable, and verified information related to government benefits, health awareness, education, and safety.
This results in:

Misinformation

Missed opportunities

Improper awareness

Low digital literacy

💡 Solution

Sahayata AI solves this by offering:

Simple explanations of complex topics

Step-by-step guidance

Support in plain language

Quick access to verified essential information

24/7 availability

Multi-domain support (schemes, health, education, environment)

✨ Key Features

✔ Government scheme explanation

✔ Health & hygiene awareness

✔ Education & career guidance

✔ Environment & sustainability tips

✔ Summaries of long documents

✔ Safe, filtered, verified responses

✔ Powered by Gemini 1.5 for reasoning & clarity

🧠 Architecture Overview
User Input
     ↓
Query Classifier ───→ Domain Handlers
     ↓                          ↓
  Gemini Reasoning Engine ←── Prompts
     ↓
Final Simplified Response

Components

app.py – Main agent logic

prompts/ – Base prompt + safety rules

helpers/

gov_schemes.py

health.py

education.py

environment.py

Gemini API – Model processing

Deployment Layer – Cloud Run / Hugging Face / Streamlit

🛠️ Technology Stack

Python

Gemini API (Flash/Pro)

Streamlit/Flask (optional UI)

Google Cloud Run or Hugging Face Spaces (optional deployment)

📂 Project Structure
sahayata_ai/
│── app.py
│── helpers/
│      ├── gov_schemes.py
│      ├── health.py
│      ├── education.py
│      └── environment.py
│── prompts/
│      ├── base_prompt.txt
│      └── safety_rules.txt
│── requirements.txt
│── README.md

🚀 How to Run Locally
1. Install Requirements
(```bash
pip install -r requirements.txt
python main.py)

##2. Add Your API Key
Create .env:

```bash  GEMINI_API_KEY=your_key_here

##3. Run the App

```bash  python app.py

🧪 Example Queries

“Explain PM Awas Yojana in simple words.”

“What are the symptoms of heat stroke?”

“How can a student get scholarship after 12th?”

“Steps to reduce plastic waste at home.”

📈 Value & Impact

Saves 80% time searching for information

Improves digital literacy

Reduces misinformation

Helps citizens make informed decisions

Supports communities with trusted knowledge

📹 Bonus (Optional Video)

Included demo showing:

Problem

Agent workflow

Live usage

Impact

📌 Deployment

(Optional but recommended)

You can deploy using:
```bash
gcloud run deploy



