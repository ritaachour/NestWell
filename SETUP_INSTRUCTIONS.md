# Setup Instructions - Toxicity Assessment RAG System

## Prerequisites

Before starting, ensure you have:
- Python 3.13 or higher
- pip (Python package manager)
- Git (for version control)
- A terminal/command prompt

## Step 1: Activate Virtual Environment

Your virtual environment is already created. Activate it:

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

## Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- ChromaDB (vector database)
- Anthropic (Claude AI client)
- Biopython (PubMed API)
- Other dependencies

## Step 3: Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
nano .env  # or use any text editor
```

Add the following content:

```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
NCBI_EMAIL=your@email.com
PORT=8000
```

### Getting API Keys:

1. **Anthropic API Key:**
   - Go to https://console.anthropic.com/
   - Sign up or log in
   - Navigate to "API Keys"
   - Create a new API key
   - Copy the key (starts with `sk-ant-`)

2. **NCBI Email:**
   - Use your email address
   - Required by PubMed API (for identification purposes only)

## Step 4: Run the Server

```bash
uvicorn main:app --reload
```

The `--reload` flag enables auto-reload during development.

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Step 5: Test the API

Open a new terminal (keep the server running in the first one) and test:

### Test 1: Root Endpoint
```bash
curl http://localhost:8000/
```

Expected response:
```json
{
  "name": "Toxicity Assessment RAG System",
  "version": "1.0.0",
  ...
}
```

### Test 2: Interactive API Docs
Open in your browser:
```
http://localhost:8000/docs
```

This provides an interactive interface to test all endpoints.

### Test 3: Load Papers
In the browser or terminal:
```bash
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{
    "query": "parabens cosmetics toxicity",
    "max_results": 5
  }'
```

### Test 4: Get Stats
```bash
curl http://localhost:8000/stats
```

### Test 5: Get Assessment
```bash
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

## Step 6: Run Automated Tests

```bash
# Make sure the server is running in another terminal
python test_api.py
```

Or with pytest:
```bash
pytest test_api.py -v
```

## Common Issues and Solutions

### Issue 1: ModuleNotFoundError
**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Find and kill the process
lsof -ti:8000 | xargs kill -9

# Or change the port
PORT=8001 uvicorn main:app --reload
```

### Issue 3: Anthropic API Error
**Error:** `Authentication error`

**Solution:**
- Check your `.env` file has the correct ANTHROPIC_API_KEY
- Verify the key is valid at https://console.anthropic.com/
- Make sure there are no spaces in the key

### Issue 4: PubMed API Error
**Error:** `Error fetching papers`

**Solution:**
- Verify NCBI_EMAIL is set in `.env`
- Check internet connection
- Wait a few seconds and retry (rate limit: 3 req/sec)

### Issue 5: ChromaDB Error
**Error:** `Database locked` or similar

**Solution:**
```bash
# Delete and restart
rm -rf chroma_db
# Then restart the server
```

## Verification Checklist

- [ ] Virtual environment activated
- [ ] Dependencies installed successfully
- [ ] `.env` file created with API keys
- [ ] Server starts without errors
- [ ] Root endpoint returns data
- [ ] Interactive docs page loads at /docs
- [ ] Can load papers from PubMed
- [ ] Can get database stats
- [ ] Can run assessments

## Next Steps

Once everything is working:

1. **Explore the API:**
   - Open http://localhost:8000/docs
   - Try different endpoints
   - Experiment with different queries

2. **Load More Papers:**
   ```bash
   # Try different queries
   - "titanium dioxide cosmetics"
   - "artificial sweeteners safety"
   - "sodium lauryl sulfate irritation"
   ```

3. **Test Assessments:**
   - Try different substances
   - Adjust quality scores
   - Experiment with usage frequencies

4. **Deploy to Production:**
   - Follow DEPLOYMENT.md guide
   - Deploy to Railway or Render
   - Update frontend with production URL

5. **Integrate with Frontend:**
   - See documentation for frontend integration
   - Create components for assessment form
   - Display results beautifully

## Development Tips

1. **Auto-reload:** The `--reload` flag automatically restarts the server when you change code

2. **API Documentation:** Use `/docs` endpoint for interactive testing

3. **Logs:** Check terminal output for debugging information

4. **Database:** The `chroma_db/` folder stores your papers (don't delete unless you want to start fresh)

5. **Environment Variables:** Never commit `.env` file to Git (already in `.gitignore`)

## Getting Help

- Check the README.md for full documentation
- See QUICKSTART.md for quick start guide
- Review DEPLOYMENT.md for deployment help
- Check test_api.py for usage examples

## Success Indicators

You'll know everything is working when:
- ✅ Server starts without errors
- ✅ You can load papers from PubMed
- ✅ Quality scores are calculated (0-100)
- ✅ Assessments return risk levels and confidence
- ✅ Source papers have PubMed links
- ✅ All tests pass

## Congratulations! 🎉

Your RAG system is now set up and ready to use. You can now:
- Load papers about toxic substances
- Get quality assessments
- Generate toxicity reports
- Deploy to production
- Integrate with your frontend

Happy coding! 🚀
