# Toxicity Assessment RAG System - Documentation Index

Welcome! This project is a complete RAG (Retrieval-Augmented Generation) system for toxicity assessment.

## 🚀 Quick Start

**New to this project? Start here:**

1. **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Step-by-step setup guide
2. **[QUICKSTART.md](QUICKSTART.md)** - 5-minute quick start
3. **Run the server:**
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   # Add your API keys to .env file
   uvicorn main:app --reload
   ```

## 📚 Documentation

### Getting Started
- **[SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md)** - Complete setup instructions with troubleshooting
- **[QUICKSTART.md](QUICKSTART.md)** - Fast setup guide (5 minutes)
- **[README.md](README.md)** - Full project documentation

### Deployment
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy to Railway, Render, or Heroku
- **[Procfile](Procfile)** - Deployment configuration

### Project Overview
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Complete project overview and features

### Code
- **[main.py](main.py)** - Main FastAPI application (505 lines)
- **[test_api.py](test_api.py)** - API tests
- **[requirements.txt](requirements.txt)** - Python dependencies

## 🎯 What This System Does

1. **Fetches Papers** from PubMed about toxic substances
2. **Scores Quality** based on study design, recency, journal prestige
3. **Stores Papers** in a vector database (ChromaDB)
4. **Generates Assessments** using Claude AI with quality-weighted results
5. **Provides Risk Ratings** (Low/Moderate/High) with confidence levels

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/load-papers` | POST | Load papers from PubMed |
| `/assess` | POST | Get toxicity assessment |
| `/stats` | GET | Database statistics |
| `/papers` | GET | List papers |
| `/papers` | DELETE | Clear database |

## 🛠️ Technology Stack

- **FastAPI** - REST API framework
- **ChromaDB** - Vector database for semantic search
- **Anthropic Claude** - AI for toxicity assessment
- **PubMed API** - Scientific paper source
- **Python 3.13+** - Backend runtime

## 🔑 Required API Keys

1. **Anthropic API Key** (https://console.anthropic.com/)
2. **NCBI Email** (your email for PubMed)

Add to `.env` file:
```bash
ANTHROPIC_API_KEY=sk-ant-xxx
NCBI_EMAIL=your@email.com
```

## 🧪 Testing

```bash
# Start server first
uvicorn main:app --reload

# In another terminal, run tests
python test_api.py
```

## 🚢 Deployment

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for:
- Railway deployment (recommended)
- Render deployment
- Heroku deployment

## 📖 Example Usage

### Load Papers
```bash
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens cosmetics toxicity", "max_results": 10}'
```

### Get Assessment
```bash
curl -X POST http://localhost:8000/assess \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 50,
    "max_papers": 5
  }'
```

## 🎨 Frontend Integration

Update your Lovable frontend environment:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## 📊 Project Statistics

- **Lines of Code:** ~505 lines (main.py)
- **API Endpoints:** 6 endpoints
- **Quality Scoring:** 4-factor scoring (0-100)
- **Vector Database:** ChromaDB with cosine similarity
- **AI Model:** Claude 3 Sonnet

## 🎯 Next Steps

1. ✅ Read SETUP_INSTRUCTIONS.md
2. ✅ Install dependencies
3. ✅ Configure API keys
4. ✅ Run the server
5. ✅ Test endpoints
6. ✅ Deploy to production
7. ✅ Integrate with frontend

## 📞 Need Help?

- Check **SETUP_INSTRUCTIONS.md** for common issues
- Review **README.md** for full documentation
- See **test_api.py** for usage examples
- Check terminal logs for debugging

## ✅ Success Criteria

- [x] Backend API complete
- [x] PubMed integration working
- [x] Quality scoring implemented
- [x] ChromaDB integration
- [x] Claude AI assessments
- [x] CORS configured
- [x] Documentation complete
- [x] Tests included
- [x] Deployment guide ready

## 🎉 Ready to Use!

Your complete RAG system is ready. Follow the setup instructions to get started!

---

**Last Updated:** October 2024  
**Version:** 1.0.0
