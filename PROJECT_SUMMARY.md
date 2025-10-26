# Toxicity Assessment RAG System - Project Summary

## 🎯 Project Overview

A complete RAG (Retrieval-Augmented Generation) system that:
- Fetches scientific papers from PubMed about toxicity of substances
- Evaluates paper quality based on clinical trial design, recency, and journal prestige
- Stores papers in a vector database with quality scores
- Provides toxicity assessments using Claude AI
- Ready for integration with Lovable frontend

## 📁 Project Structure

```
toxicity-rag-api/
├── main.py                 # Main FastAPI application (17KB)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore rules
├── README.md              # Full documentation
├── QUICKSTART.md          # Quick start guide
├── DEPLOYMENT.md          # Deployment instructions
├── test_api.py            # API tests
├── Procfile               # Deployment configuration
└── chroma_db/             # Vector database (auto-created)
```

## 🔑 Key Features

### 1. PubMed Integration
- Fetches papers using Entrez API
- Extracts title, abstract, journal, year, publication types
- Identifies clinical trials and RCTs automatically

### 2. Quality Scoring (0-100 points)
- **Study Design** (40 pts): RCT, Clinical Trial, Systematic Review
- **Recency** (20 pts): Recent papers score higher
- **Abstract Quality** (20 pts): Longer abstracts = better score
- **Journal Prestige** (20 pts): High-impact journals score higher

### 3. Vector Database (ChromaDB)
- Persistent storage with cosine similarity
- Metadata includes: PMID, quality score, year, study type
- Semantic search for relevant papers

### 4. AI Assessment (Claude)
- Analyzes top papers based on quality
- Provides safety rating (Low/Moderate/High Risk)
- Includes key findings, usage frequency impact, vulnerable populations
- Returns confidence level and limitations

## 📡 API Endpoints

### GET /
- Returns API information and endpoints

### POST /load-papers
- Fetches papers from PubMed
- Calculates quality scores
- Stores in ChromaDB
- **Request**: `{"query": "string", "max_results": 20}`
- **Response**: Papers loaded, average quality, clinical trial count

### POST /assess
- Generates toxicity assessment
- **Request**: Substance, product type, usage frequency, quality filters
- **Response**: Risk level, confidence, assessment text, sources

### GET /stats
- Database statistics
- **Response**: Total papers, average quality, clinical trial count, distribution

### GET /papers
- List papers in database
- **Query**: `limit` parameter

### DELETE /papers
- Clear database

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Backend | FastAPI | REST API framework |
| Vector DB | ChromaDB | Semantic search |
| AI Model | Anthropic Claude | Toxicity assessment |
| Data Source | PubMed (Bio.Entrez) | Scientific papers |
| Python | 3.13+ | Backend runtime |

## 📦 Dependencies

- `fastapi==0.109.0` - Web framework
- `uvicorn[standard]==0.27.0` - ASGI server
- `chromadb==0.4.22` - Vector database
- `anthropic==0.18.1` - Claude AI
- `biopython==1.83` - PubMed API
- `python-dotenv==1.0.0` - Environment variables
- `pydantic==2.5.3` - Data validation

## 🚀 Quick Start

```bash
# 1. Activate venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env
ANTHROPIC_API_KEY=sk-ant-xxx
NCBI_EMAIL=user@example.com

# 4. Run server
uvicorn main:app --reload

# 5. Test
curl http://localhost:8000/
```

Visit: http://localhost:8000/docs for interactive API docs

## 🧪 Testing

```bash
# Run tests
python test_api.py

# Or with pytest
pytest test_api.py -v
```

## 🌐 Deployment

### Railway (Recommended)
```bash
railway login
railway init
railway variables set ANTHROPIC_API_KEY=xxx
railway up
```

### Render
1. Connect GitHub repo
2. Build: `pip install -r requirements.txt`
3. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add environment variables

## 🎨 Frontend Integration

Update your Lovable project environment:
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

## 🔍 Example Usage

### 1. Load Papers
```bash
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{
    "query": "parabens cosmetics toxicity",
    "max_results": 10
  }'
```

**Response:**
```json
{
  "papers_loaded": 10,
  "average_quality_score": 68.5,
  "clinical_trial_count": 2,
  "message": "Papers loaded successfully"
}
```

### 2. Get Assessment
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

**Response:**
```json
{
  "risk_level": "Moderate Risk",
  "confidence": "High",
  "assessment": "Based on recent clinical trials...",
  "sources": [...],
  "papers_analyzed": 5,
  "avg_quality_score": 72.0
}
```

## 📊 Quality Score Categories

| Score Range | Category | Description |
|------------|----------|-------------|
| 80-100 | High | RCTs, recent, high-impact journals |
| 60-79 | Good | Strong evidence, recent studies |
| 40-59 | Moderate | Moderate quality, some limitations |
| 0-39 | Low | Lower quality, older studies |

## 🔒 Security Features

- CORS enabled for frontend integration
- Environment variables for API keys
- Input validation with Pydantic
- Error handling throughout

## 📝 Example Queries

**Cosmetics:**
- "parabens cosmetics toxicity"
- "titanium dioxide nanoparticles cosmetics"
- "fragrance allergens sensitization"

**Food Additives:**
- "artificial sweeteners safety metabolic"
- "BPA food packaging endocrine"

**Cleaning Products:**
- "ammonia household cleaners respiratory"
- "triclosan antimicrobial toxicity"

## ⚙️ Configuration

### Environment Variables
- `ANTHROPIC_API_KEY` - Required for AI assessments
- `NCBI_EMAIL` - Required for PubMed API
- `PORT` - Server port (default: 8000)

### Quality Filters
- `min_quality_score` - Minimum paper quality (0-100)
- `max_papers` - Maximum papers to analyze (1-20)

## 🐛 Troubleshooting

**Problem**: Papers not loading
- Check NCBI_EMAIL is set
- Verify internet connection
- PubMed rate limit: 3 requests/second

**Problem**: Assessment fails
- Ensure papers are loaded first
- Check min_quality_score isn't too high
- Verify ANTHROPIC_API_KEY is valid

**Problem**: CORS errors
- CORS configured for all origins
- Verify frontend API_URL is correct

## 🎯 Success Criteria

✅ Backend API deployed and accessible  
✅ Can load papers from PubMed with quality scores  
✅ Can run toxicity assessments  
✅ Frontend can connect to backend  
✅ Assessment results display correctly  
✅ Source papers have working PubMed links  
✅ Database stats update correctly  
✅ Error handling works throughout  

## 📚 Documentation

- **README.md** - Full documentation
- **QUICKSTART.md** - Quick start guide
- **DEPLOYMENT.md** - Deployment instructions
- **PROJECT_SUMMARY.md** - This file

## 🚀 Next Steps

1. Test all endpoints locally
2. Load papers for your use case
3. Test assessments with different substances
4. Deploy to production
5. Integrate with Lovable frontend
6. Add frontend components (see below)

## 🎨 Frontend Components Needed

### Assessment Form
- Substance name input
- Product type dropdown
- Usage frequency selector
- Quality score slider
- Max papers slider

### Results Display
- Risk level badge (color-coded)
- Confidence level
- Assessment text (markdown)
- Source papers list
- PubMed links

### Admin Panel
- Database stats display
- Load papers form
- Clear database button
- Quality distribution chart

## 🎉 Ready to Deploy!

Your RAG system is complete and ready for production use. Follow the deployment guide to get it live!
