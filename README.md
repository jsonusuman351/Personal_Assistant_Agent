# 🤖 Personal Assistant Agent

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![Render](https://img.shields.io/badge/Render-Deploy-black?style=flat&logo=render)](https://render.com/)


An AI-powered personal assistant equipped with real-time weather updates, a mathematical calculator, and web search capabilities. Built using a modern tech stack and designed for seamless deployment.

---

## 🌟 Live Demo
Try out the Personal Assistant Agent here:
**[👉 Click here to access the Live UI](#)** *(https://personal-assistant-agent-1-ui.onrender.com)*

---

## 📸 Screenshots

### 🖥️ User Interface (Streamlit)
![UI Screenshot]<img width="1922" height="1080" alt="Image" src="https://github.com/user-attachments/assets/f8b2296f-ff42-4004-817c-ee9779e611a2" />
*Our interactive and user-friendly chat interface.*

### 🐳 Docker Deployment
![Docker Screenshot]<img width="1922" height="1080" alt="Image" src="https://github.com/user-attachments/assets/b45b52d2-f307-451b-b09b-19a2582679c0" />
*Running the API and UI seamlessly using Docker Compose.*

### ☁️ Render Cloud Deployment
![Render Screenshot]<img width="1922" height="1080" alt="Image" src="https://github.com/user-attachments/assets/0dc679ee-1d54-42f0-923f-b904333127ce" />
*Backend and Frontend successfully deployed on Render.*

---

## 🛠️ Tech Stack
- **LLM**: OpenAI GPT-4o-mini
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Tools**: OpenWeather API, Tavily Search API
- **Deployment**: Docker, Render / AWS

## 🏗️ Architecture
![Architecture Diagram](link_to_architecture_diagram_if_any.png)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Conda or standard Python `venv`
- API keys (OpenAI, OpenWeather, Tavily)
- Docker (Optional, for containerized run)

### Local Installation (Without Docker)

```bash
# Clone the repository
git clone [https://github.com/jsonusuman351/Personal_Assistant_Agent.git](https://github.com/jsonusuman351/Personal_Assistant_Agent.git)
cd Personal_Assistant_Agent

# Create and activate environment
conda create -p venv python=3.10 -y
conda activate venv/

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your respective API keys

# Run backend (API)
uvicorn src.api.main:app --reload

# Run Frontend UI (Open a new terminal)
streamlit run src/ui/app.py

🐳 Run via Docker (Recommended)
You can run both the UI and the API together with a single command using Docker Compose:

```bash
docker-compose up --build
The UI will be available at http://localhost:8501 and the API at http://localhost:8000.

📚 API Documentation
Once the backend is running, visit the interactive Swagger UI to test the endpoints:
👉 http://localhost:8000/docs

🧪 Testing
To run the automated tests, use pytest:

```bash
pytest tests/ -v
📁 Project Structure
Plaintext
src/
├── config/      # Settings and environment configurations
├── tools/       # Tools implementation (Weather, Calc, Search)
├── agent/       # Core agent loop and LLM orchestration
├── api/         # FastAPI backend setup
└── ui/          # Streamlit frontend application