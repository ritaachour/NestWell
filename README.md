# Toxicity Assessment RAG System

A RAG (Retrieval-Augmented Generation) system that fetches scientific papers from PubMed about toxicity of substances in foods, cosmetics, and cleaning products, evaluates paper quality, and provides evidence-based toxicity assessments.

## Features

- 🔬 Fetches papers from PubMed with automatic quality scoring
- 📊 Quality assessment based on study design, recency, and journal prestige
- 🧠 AI-powered toxicity assessments using Claude
- 💾 Vector database storage with ChromaDB
- 🌐 RESTful API with FastAPI
- 📱 Frontend integration ready (Lovable/Next.js)

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
NCBI_EMAIL=your@email.com
PORT=8000
```

**Required API Keys:**
- **Anthropic API**: Get from https://console.anthropic.com/
- **NCBI Email**: Your email address (required by PubMed API)

### 4. Run the Server

```bash
uvicorn main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

## API Endpoints

### GET /
Returns API information and available endpoints.

### POST /load-papers
Load papers from PubMed into the database.

**Request Body:**
```json
{
  "query": "parabens cosmetics toxicity",
  "max_results": 20
}
```

**Response:**
```json
{
  "papers_loaded": 15,
  "average_quality_score": 68.5,
  "clinical_trial_count": 3,
  "message": "Papers loaded successfully"
}
```

### POST /assess
Get toxicity assessment for a substance.

**Request Body:**
```json
{
  "substance": "parabens",
  "product_type": "cosmetics",
  "usage_frequency": "daily",
  "min_quality_score": 50,
  "max_papers": 5
}
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

### GET /stats
Get database statistics.

**Response:**
```json
{
  "total_papers": 150,
  "average_quality_score": 65.4,
  "clinical_trial_count": 25,
  "quality_distribution": {
    "high": 30,
    "good": 45,
    "moderate": 50,
    "low": 25
  }
}
```

### GET /papers
List papers in the database.

**Query Parameters:**
- `limit`: Number of papers to return (default: 50)

### DELETE /papers
Clear the entire database.

## Quality Scoring

Papers are scored from 0-100 based on:

- **Study Design** (40 points): RCT (40), Clinical Trial (30), Systematic Review (35), Observational (20)
- **Recency** (20 points): Recent years score higher
- **Abstract Quality** (20 points): Longer abstracts score higher
- **Journal Prestige** (20 points): High-impact journals score higher

## Frontend Integration

Update your Lovable frontend's environment variable:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
```

See the frontend implementation guide for complete integration details.

## Deployment

### Railway

```bash
railway login
railway init
railway variables set ANTHROPIC_API_KEY=your_key
railway variables set NCBI_EMAIL=your_email
railway up
```

### Render

1. Connect GitHub repository
2. Create new Web Service
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

## Troubleshooting

**Papers not loading**
- Check NCBI_EMAIL is set correctly
- Verify internet connection
- Respect PubMed API rate limits (3 requests/second)

**Assessment fails**
- Ensure papers are loaded first (check /stats)
- Verify min_quality_score isn't too restrictive
- Check ANTHROPIC_API_KEY is valid

**CORS errors**
- CORS is configured for all origins
- Verify frontend API_URL is correct

## License

MIT
