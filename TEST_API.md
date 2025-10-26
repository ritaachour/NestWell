# Testing Your API

## Quick Test Guide

### Step 1: Test Root Endpoint

Open in browser or use curl:

```bash
curl https://your-api.railway.app/
```

Should return API information.

### Step 2: Load Papers

Test loading papers from PubMed:

```bash
curl -X POST "https://your-api.railway.app/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "parabens cosmetics toxicity",
    "max_results": 10
  }'
```

**Expected Response:**
```json
{
  "papers_loaded": 10,
  "average_quality_score": 65.5,
  "clinical_trial_count": 2,
  "message": "Papers loaded successfully"
}
```

### Step 3: Check Database Stats

```bash
curl https://your-api.railway.app/stats
```

**Expected Response:**
```json
{
  "total_papers": 10,
  "average_quality_score": 65.5,
  "clinical_trial_count": 2,
  "quality_distribution": {...}
}
```

### Step 4: Get Assessment

```bash
curl -X POST "https://your-api.railway.app/assess" \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 30,
    "max_papers": 5
  }'
```

**Expected Response:**
```json
{
  "risk_level": "Moderate Risk",
  "confidence": "High",
  "assessment": "...",
  "sources": [
    {
      "pmid": "12345678",
      "title": "Safety assessment of parabens in cosmetics",
      "journal": "Journal of Toxicology",
      "year": "2023",
      "quality_score": 85,
      "is_clinical_trial": true,
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678"
    },
    ...
  ],
  "papers_analyzed": 5,
  "avg_quality_score": 72.0
}
```

**To see the paper links:** Look in the `sources` array. Each source has a `url` field that links to PubMed.

## Viewing Paper Links

After you get an assessment, the response includes a `sources` array with links to all the papers used.

### Example Response Structure:

```json
{
  "sources": [
    {
      "pmid": "12345678",
      "title": "Paper Title Here",
      "journal": "Journal Name",
      "year": "2023",
      "quality_score": 85,
      "is_clinical_trial": true,
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678"  ← Click this!
    }
  ]
}
```

Each source object has a `url` field that links directly to PubMed.

### In Your Browser:

1. Get an assessment using `/assess` endpoint
2. Look for the `sources` array in the response
3. Click any `url` field to view that paper on PubMed

### Example: Find All Papers

```bash
curl -X POST "https://your-api.railway.app/assess" \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily"
  }' | jq '.sources[].url'
```

This will print all the PubMed URLs from the sources.

## Using Interactive Docs

Visit: `https://your-api.railway.app/docs`

### How to Use:

1. Click on any endpoint (e.g., `POST /load-papers`)
2. Click "Try it out" button
3. Fill in the JSON request body
4. Click "Execute"

### Sample Request Body for /load-papers:

```json
{
  "query": "parabens cosmetics toxicity",
  "max_results": 10
}
```

### Sample Request Body for /assess:

```json
{
  "substance": "parabens",
  "product_type": "cosmetics",
  "usage_frequency": "daily",
  "min_quality_score": 30,
  "max_papers": 5
}
```

## Troubleshooting

**Interactive docs not loading?**
- Check the URL is correct
- Try `/redoc` instead: `https://your-api.railway.app/redoc`

**Getting 404 errors?**
- Make sure papers are loaded first
- Check endpoint URLs are correct

**Getting "No papers found"?**
- Run `/load-papers` first for that substance
- Check `/stats` to verify papers are in database

## Testing Locally First

Before deploying, test locally:

```bash
# Start local server
uvicorn main:app --reload

# Test in browser
http://localhost:8000/docs

# Test with curl
curl http://localhost:8000/
```
