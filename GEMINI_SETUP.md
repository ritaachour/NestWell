# Google Gemini Setup - FREE Alternative to Claude

## ✅ What Changed

Your code now uses **Google Gemini** instead of Claude AI. Benefits:
- ✅ **FREE** to use (generous free tier)
- ✅ High quality AI assessments
- ✅ Falls back to basic assessment if API unavailable
- ✅ No payment required

---

## 🚀 Quick Setup (2 Minutes)

### Step 1: Get Free API Key

1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (starts with `AIz...`)

### Step 2: Add to Your .env File

```bash
# Add this line to your .env file
GEMINI_API_KEY=AIz...your-key-here

# Keep NCBI_EMAIL
NCBI_EMAIL=your@email.com

# Remove or ignore ANTHROPIC_API_KEY (no longer needed!)
```

### Step 3: Install the Package

```bash
pip install google-generativeai==0.3.1
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### Step 4: Restart Your Server

```bash
# If running, press Ctrl+C, then:
uvicorn main:app --reload
```

---

## 🎉 Done!

That's it! Now when you use the `/assess` endpoint, it will:
1. ✅ Try to use Google Gemini (free, high quality)
2. ✅ Fall back to basic assessment if Gemini is unavailable
3. ✅ Still work without any API key (uses basic mode)

---

## 🧪 Test It

```bash
# Load some papers first
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens cosmetics toxicity", "max_results": 5}'

# Get AI-powered assessment
curl -X POST http://localhost:8000/assess \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 30,
    "max_papers": 3
  }'
```

---

## 💰 Costs

**Google Gemini:**
- **FREE** tier: 60 requests/minute
- After free tier: $0.000125 / 1K characters
- **Approx cost per assessment: $0.002** (almost nothing!)

**Claude (old):**
- $0.05 per assessment

**Savings: 96% cheaper!** 💰

---

## 🔄 What If I Don't Want to Use Any AI?

The system will automatically fall back to basic assessment mode that:
- Analyzes paper quality scores
- Counts clinical trials
- Provides risk level based on data quality
- Gives you the papers to read manually

No API key needed for this!

---

## 🆘 Troubleshooting

**Problem:** "Module not found: google.generativeai"
**Solution:**
```bash
pip install google-generativeai==0.3.1
```

**Problem:** "Invalid API key"
**Solution:**
- Double-check your .env file has `GEMINI_API_KEY=...`
- Make sure you copied the full key
- Restart the server after adding it

**Problem:** "API quota exceeded"
**Solution:**
- Free tier: 60 requests/minute
- Wait a minute and try again
- Or use the basic assessment mode (works without API)

---

## 📊 Quality Comparison

| Feature | Claude AI | Google Gemini | Basic Mode |
|---------|-----------|---------------|------------|
| Cost | $0.05/req | FREE | FREE |
| Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Setup | API key | API key | None |
| Features | Full AI | Full AI | Basic stats |

**Recommendation:** Use Google Gemini for the best free experience!

---

## ✨ Benefits of This Update

1. ✅ **Saves money** - free instead of $0.05 per assessment
2. ✅ **Still high quality** - Gemini is excellent
3. ✅ **Falls back gracefully** - works even without API key
4. ✅ **Easy setup** - just add one line to .env

---

Your toxicity assessment system is now **100% free to use**! 🎉
