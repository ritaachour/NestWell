# NestWell - Toxicity Assessment RAG System

A RAG (Retrieval-Augmented Generation) system that fetches scientific papers from PubMed about toxicity of substances in foods, cosmetics, and cleaning products, evaluates paper quality, and provides evidence-based toxicity assessments.

## Features

- 🔬 Fetches papers from PubMed with automatic quality scoring
- 📊 Quality assessment based on study design, recency, and journal prestige
- 🧠 AI-powered toxicity assessments using Google Gemini (FREE)
- 💾 Vector database storage with ChromaDB
- 🌐 RESTful API with FastAPI
- 📱 Frontend integration ready (Lovable/Next.js)

## Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/ritaachour/NestWell.git
cd NestWell
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```bash
GEMINI_API_KEY=your-key-here
NCBI_EMAIL=your@email.com
PORT=8000
```

### 3. Run Server

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000/docs

## Documentation

- [Quick Start Guide](QUICKSTART.md)
- [Setup Instructions](SETUP_INSTRUCTIONS.md)
- [Google Gemini Setup](GEMINI_SETUP.md)
- [Deployment Guide](DEPLOYMENT.md)
- [Git Workflow](GIT_WORKFLOW.md)

## API Endpoints

- `POST /load-papers` - Load papers from PubMed
- `POST /assess` - Get toxicity assessment
- `GET /stats` - Database statistics
- `GET /papers` - List papers
- `DELETE /papers` - Clear database

## License

MIT
