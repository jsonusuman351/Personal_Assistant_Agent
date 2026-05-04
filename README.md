# 🤖 Personal Assistant Agent

AI-powered personal assistant with weather, calculator, and web search capabilities.

## 🛠️ Tech Stack
- **LLM**: OpenAI GPT-4o-mini
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **Tools**: OpenWeather API, Tavily Search API
- **Deployment**: Docker, Render/AWS

## 🏗️ Architecture
[Insert architecture diagram image]

## 🚀 Setup

### Prerequisites
- Python 3.10+
- Conda
- API keys (OpenAI, OpenWeather, Tavily)

### Installation

```bash
# Clone repo
git clone https://github.com/your-username/personal-assistant-agent.git
cd personal-assistant-agent

# Create environment
conda create -p venv python=3.10 -y
conda activate venv/

# Install dependencies
pip install -r requirements.txt

# Setup .env
cp .env.example .env
# Edit .env with your keys

# Run backend
uvicorn src.api.main:app --reload

# Run UI (new terminal)
streamlit run src/ui/app.py
Docker
```bash
docker-compose up
📚 API Docs
Visit http://localhost:8000/docs

🧪 Testing
```bash
pytest tests/ -v
📁 Project Structure
text
src/
├── config/      # Settings
├── tools/       # Weather, Calc, Search
├── agent/       # Core agent loop
├── api/         # FastAPI
└── ui/          # Streamlit