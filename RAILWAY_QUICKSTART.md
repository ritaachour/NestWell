# Railway Quick Start & Using Your RAG System

## What is Railway?

Railway is a hosting platform that runs your API in the cloud. Think of it like:
- A server in the cloud
- Free to start
- Automatic deployment
- Handles all server management

You can use alternatives: Render, Heroku, or host on your own server.

## Step 1: Prepare Your Code

Your code is already ready. Just make sure all files are committed:

```bash
git status  # Check for uncommitted changes
git add .
git commit -m "Prepare for deployment"
git push
```

## Step 2: Deploy to Railway

### Option A: Using Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Set environment variables
railway variables set GEMINI_API_KEY=your-key-here
railway variables set NCBI_EMAIL=your@email.com

# Deploy!
railway up
```

### Option B: Using GitHub (Easier)

1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your NestWell repository
5. Railway will automatically detect it's a Python project
6. Add environment variables in the Railway dashboard
7. Click "Deploy"

## Step 3: Get Your API URL

After deployment, Railway gives you a URL like:
```
https://your-app-name.railway.app
```

Copy this URL - you'll need it for your frontend!

## Step 4: Test Your API

```bash
# Test if it's working
curl https://your-app-name.railway.app/

# Should return API information
```

## How to Interact with Your RAG System

### Method 1: Interactive API Documentation

1. Open: `https://your-app-name.railway.app/docs`
2. You'll see a full interface to test all endpoints
3. Click on any endpoint to try it out
4. Fill in the form and click "Execute"

### Method 2: Using curl (Command Line)

```bash
# 1. Check API status
curl https://your-app-name.railway.app/

# 2. Load papers about parabens
curl -X POST https://your-app-name.railway.app/load-papers \
  -H "Content-Type: application/json" \
  -d '{
    "query": "parabens cosmetics toxicity",
    "max_results": 10
  }'

# 3. Check how many papers are loaded
curl https://your-app-name.railway.app/stats

# 4. Get toxicity assessment
curl -X POST https://your-app-name.railway.app/assess \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 50,
    "max_papers": 5
  }'
```

### Method 3: Using Python

```python
import requests

API_URL = "https://your-app-name.railway.app"

# Load papers
response = requests.post(f"{API_URL}/load-papers", json={
    "query": "parabens cosmetics toxicity",
    "max_results": 10
})
print(response.json())

# Get assessment
response = requests.post(f"{API_URL}/assess", json={
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily"
})
print(response.json())
```

### Method 4: Using JavaScript/Fetch (for your frontend)

```javascript
// Load papers
const loadPapers = async (query) => {
  const response = await fetch('https://your-app-name.railway.app/load-papers', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      query: query,
      max_results: 10
    })
  });
  return response.json();
};

// Get assessment
const getAssessment = async (substance, productType) => {
  const response = await fetch('https://your-app-name.railway.app/assess', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      substance: substance,
      product_type: productType,
      usage_frequency: 'daily'
    })
  });
  return response.json();
};
```

## Typical Workflow

1. **Load papers first** (one-time per topic)
   - Search PubMed for papers about a substance
   - Store them in your database

2. **Get assessments** (as many as you want)
   - Query your database
   - Get AI-powered toxicity analysis

Example:
```bash
# Step 1: Load papers about parabens
curl -X POST https://your-api.railway.app/load-papers \
  -d '{"query": "parabens cosmetics toxicity", "max_results": 20}'

# Step 2: Get assessment
curl -X POST https://your-api.railway.app/assess \
  -d '{"substance": "parabens", "product_type": "cosmetics", "usage_frequency": "daily"}'
```

## API Endpoints Overview

| Endpoint | What It Does | When to Use |
|----------|-------------|-------------|
| `POST /load-papers` | Fetches papers from PubMed | Once per substance/topic |
| `POST /assess` | Get toxicity assessment | Every time you need analysis |
| `GET /stats` | Database statistics | Check how many papers loaded |
| `GET /papers` | List all papers | Browse your database |
| `DELETE /papers` | Clear database | Start fresh |

## Common Issues

**Papers won't load?**
- Check NCBI_EMAIL is set in Railway
- Verify internet connection
- Wait a moment (rate limits)

**Assessment returns "no papers found"?**
- Run `/load-papers` first for that substance
- Check `/stats` to see what's in database

**Getting errors?**
- Check Railway logs: `railway logs`
- Verify environment variables are set
- Make sure API is deployed

## Free Alternatives to Railway

- **Render** - Similar to Railway, free tier available
- **Fly.io** - Free tier for small apps
- **PythonAnywhere** - Free hosting for Python
- **Heroku** - Free tier (limited hours)

## Costs

- Railway: Free tier with $5 credit/month
- Gemini API: Free tier (60 requests/minute)
- PubMed: Free
- **Total: Free to start!**
