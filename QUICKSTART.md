# Quick Start Guide

## 🚀 Fast Setup (5 minutes)

### Step 1: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys

Edit `.env` file (or create it):

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
NCBI_EMAIL=your@email.com
PORT=8000
```

**Get API Keys:**
- **Anthropic API**: https://console.anthropic.com/ → API Keys
- **NCBI Email**: Your email (required by PubMed)

### Step 4: Run the Server

```bash
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs

## 🧪 Test the API

### Test 1: Check API Status

```bash
curl http://localhost:8000/
```

### Test 2: Load Papers

```bash
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{
    "query": "parabens cosmetics toxicity",
    "max_results": 10
  }'
```

### Test 3: Check Stats

```bash
curl http://localhost:8000/stats
```

### Test 4: Get Assessment

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

## 📊 Expected Response Format

### Load Papers Response
```json
{
  "papers_loaded": 10,
  "average_quality_score": 68.5,
  "clinical_trial_count": 2,
  "message": "Papers loaded successfully"
}
```

### Assessment Response
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

## 🔍 Common Queries to Try

```bash
# Food additives
"artificial sweeteners safety metabolic"

# Cosmetics
"titanium dioxide nanoparticles cosmetics"

# Cleaning products
"ammonia household cleaners respiratory"

# Sulfates
"sodium lauryl sulfate dermal irritation"

# Fragrance
"fragrance allergens sensitization"
```

## 🐛 Troubleshooting

**Problem**: `ModuleNotFoundError`
**Solution**: Make sure virtual environment is activated and dependencies installed

**Problem**: Papers not loading
**Solution**: Check NCBI_EMAIL is set, verify internet connection

**Problem**: Assessment fails
**Solution**: Make sure papers are loaded first (check /stats endpoint)

**Problem**: CORS errors (frontend)
**Solution**: CORS is already configured for all origins

## 🚢 Next Steps

1. ✅ Test all endpoints
2. ✅ Load papers for your use case
3. ✅ Test assessments
4. 🌐 Deploy to production (Railway/Render)
5. 📱 Integrate with frontend

See full README.md for deployment instructions!
