# Deployment Guide

## 🚀 Deploy to Railway (Recommended)

### Step 1: Prepare Repository

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
```

### Step 2: Install Railway CLI

```bash
npm install -g @railway/cli
```

### Step 3: Login to Railway

```bash
railway login
```

### Step 4: Initialize Railway Project

```bash
railway init
```

### Step 5: Set Environment Variables

```bash
railway variables set ANTHROPIC_API_KEY=sk-ant-your-key-here
railway variables set NCBI_EMAIL=your@email.com
railway variables set PORT=8000
```

### Step 6: Deploy

```bash
railway up
```

### Step 7: Get Your URL

```bash
railway status
```

Your API will be available at: `https://your-project.up.railway.app`

---

## 🌐 Deploy to Render

### Step 1: Create Account

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create New Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select the repository

### Step 3: Configure Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Step 4: Add Environment Variables

In the Render dashboard:
- `ANTHROPIC_API_KEY`: Your Anthropic API key
- `NCBI_EMAIL`: Your email
- `PORT`: (auto-set by Render)

### Step 5: Deploy

Click "Create Web Service" and wait for deployment.

---

## ☁️ Deploy to Heroku

### Step 1: Install Heroku CLI

```bash
brew install heroku/brew/heroku  # macOS
```

### Step 2: Login

```bash
heroku login
```

### Step 3: Create App

```bash
heroku create your-app-name
```

### Step 4: Set Environment Variables

```bash
heroku config:set ANTHROPIC_API_KEY=sk-ant-your-key-here
heroku config:set NCBI_EMAIL=your@email.com
```

### Step 5: Deploy

```bash
git push heroku main
```

---

## 🔧 Environment Variables

All platforms require these variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | `sk-ant-xxx` |
| `NCBI_EMAIL` | Your email (for PubMed) | `user@example.com` |
| `PORT` | Server port (auto-set by platform) | `8000` |

---

## 📋 Pre-Deployment Checklist

- [ ] All code committed and pushed to Git
- [ ] `.env` file is in `.gitignore` (should not be committed)
- [ ] Environment variables configured on platform
- [ ] `requirements.txt` is up to date
- [ ] API keys are valid and have sufficient quota

---

## 🧪 Test Production Deployment

After deployment:

```bash
# Test root endpoint
curl https://your-app.railway.app/

# Test load papers
curl -X POST https://your-app.railway.app/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens cosmetics", "max_results": 5}'

# Test stats
curl https://your-app.railway.app/stats
```

---

## 🔍 Troubleshooting

### Build Fails on Railway

**Problem**: Missing dependencies
**Solution**: Verify `requirements.txt` has all packages

### Application Crashes

**Problem**: Missing environment variables
**Solution**: Check all variables are set in platform dashboard

### CORS Errors

**Problem**: Frontend can't access API
**Solution**: CORS is configured for all origins (`*`)

### ChromaDB Issues

**Problem**: Vector database not persisting
**Solution**: 
- Railway: Filesystem is temporary, use external storage
- Render: Use persistent disk (paid plan)
- Consider PostgreSQL with pgvector for production

---

## 💡 Production Recommendations

1. **Use PostgreSQL**: ChromaDB is for development only
2. **Add Authentication**: Protect your API endpoints
3. **Rate Limiting**: Prevent abuse
4. **Monitoring**: Add logging and error tracking
5. **Backup**: Regular database backups
6. **CDN**: Use CloudFlare for better performance

---

## 📊 Monitoring

### Railway Dashboard
- View logs: `railway logs`
- Check metrics in dashboard

### Render Dashboard
- View logs in service logs tab
- Check metrics in metrics tab

### Health Check

Add a health check endpoint to your API:

```python
@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now()}
```

Test: `curl https://your-app.railway.app/health`

---

## 🎉 Success!

Once deployed, update your frontend:

```bash
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

Your RAG system is now live! 🚀
