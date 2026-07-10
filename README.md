🚀 Multi-AI Web Platform
This project is a modern web application that integrates various Artificial Intelligence (AI) and Machine Learning (ML) models into a single unified platform. It enables users to perform data analysis, make predictions, and access intelligent assistance through a user-friendly interface.

🛠️ Core Modules
AI Chatbot (Gemini): An intelligent assistant powered by Google's advanced Gemini-2.5-Flash model to answer queries in real-time.

Real Estate Price Predictor: Estimates property prices based on the number of rooms and total area.

Resume Screener (NLP): Analyzes resume text to determine candidate compatibility and seniority levels.

Credit Scoring: Uses a Random Forest model to assess the risk and eligibility of credit applicants.

Auto Analyzer: A multimodal system that predicts car market prices based on images (Computer Vision) and text descriptions (NLP).

⚙️ Tech Stack
Backend: Python 3.11, FastAPI

Frontend: Tailwind CSS, Jinja2 Templates

AI/ML: TensorFlow/Keras, Scikit-Learn, Pandas, NumPy

API: Google GenAI SDK

🚀 Installation & Setup
Clone the repository:

Bash
git clone https://github.com/ShodmonboyevShoxrux/Multi-Ai.git
cd Multi-Ai
Setup virtual environment:

Bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies:

Bash
pip install -r requirements.txt
Configure API Key:
Create a .env file in the root directory and add your Google Gemini API key:

Plaintext
GEMINI_API_KEY=your_api_key_here
Run the server:

Bash
python main.py
Open http://127.0.0.1:8000 in your browser.

🎯 Project Goal
This platform aims to provide enterprises and individual users with an intuitive interface to analyze complex data through AI-powered insights. Our goal is to make advanced artificial intelligence solutions accessible and understandable for everyone.

🔮 Roadmap
[ ] Real-time Data: Integration with external APIs for live market price updates.

[ ] User Dashboard: Personalized user profiles and history tracking.

[ ] Docker: Full containerization for simplified deployment.

[ ] Multilingual Support: Expanding platform localization (Uzbek, Russian, English).
