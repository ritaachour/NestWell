# NestWell - Toxicity Assessment API

RAG system for toxicity assessment using PubMed research papers with quality scoring and AI-powered analysis.

## Features

- Fetch papers from PubMed
- Quality scoring (study design, recency, journal prestige)
- Vector database with semantic search
- AI toxicity assessments using Google Gemini
- RESTful API with FastAPI

## Quick Start

```bash
git clone https://github.com/ritaachour/NestWell.git
cd NestWell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file (see GEMINI_SETUP.md)
uvicorn main:app --reload
```

Visit http://localhost:8000/docs

## Documentation

- `QUICKSTART.md` - Quick setup guide
- `GEMINI_SETUP.md` - Google Gemini API setup
- `DEPLOYMENT.md` - Production deployment guide
- `GIT_WORKFLOW.md` - Development workflow

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/load-papers` | POST | Load papers from PubMed |
| `/assess` | POST | Get toxicity assessment |
| `/stats` | GET | Database statistics |
| `/papers` | GET | List papers |
| `/papers` | DELETE | Clear database |

## Requirements

- Python 3.13+
- Google Gemini API key (free tier available)
- NCBI email (for PubMed API)

## License

MIT
