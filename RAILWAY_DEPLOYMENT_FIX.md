# Railway Deployment Fix - 404 Error

## The Problem

Your Railway API at `https://web-production-b9b9.up.railway.app` is returning 404.

This means the deployment either:
1. ❌ Failed to deploy
2. ❌ Crashed on startup
3. ❌ Never deployed in the first place

---

## Quick Fix: Deploy to Railway

### Option 1: Deploy via Railway Dashboard (Easiest)

1. **Go to https://railway.app**
2. **Sign in** with GitHub
3. **Click "New Project"**
4. **Select "Deploy from GitHub repo"**
5. **Choose your NestWell repository**
6. **Railway auto-detects it's Python**
7. **Set environment variables** (see below)
8. **Click "Deploy"**
9. **Wait for deployment to finish** (2-5 minutes)

### Option 2: Deploy via Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Set environment variables
railway variables set GEMINI_API_KEY=your-key-here
railway variables set NCBI_EMAIL=your@email.com

# Deploy
railway up
```

---

## Required Environment Variables

**In Railway dashboard, go to Variables tab and add:**

| Variable Name | Value | Example |
|---------------|-------|---------|
| `GEMINI_API_KEY` | Your Gemini API key | `AIza...` |
| `NCBI_EMAIL` | Your email | `your@email.com` |
| `PORT` | (Auto-set by Railway) | `${{PORT}}` |

**Important:** Railway automatically sets `PORT`, but make sure your `Procfile` or start command uses it.

---

## Verify Deployment

### 1. Check Railway Logs

In Railway dashboard:
1. Click your service
2. Go to "Logs" tab
3. Look for:
   - ✅ "Application startup complete"
   - ✅ "Uvicorn running on..."
   - ❌ Any red errors

### 2. Test the API

```bash
# Test root endpoint
curl https://web-production-b9b9.up.railway.app/

# Should return JSON with API info
```

### 3. Test the Endpoint

```bash
# Test load-papers endpoint
curl -X POST https://web-production-b9b9.up.railway.app/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens toxicity", "max_results": 5}'

# Should return papers data
```

---

## Common Deployment Issues

### Issue 1: Dependencies Failed to Install

**Symptom:** Build fails with pip errors

**Fix:** Check `requirements.txt` syntax

```bash
# Test locally first
pip install -r requirements.txt
```

### Issue 2: Missing Start Command

**Symptom:** Deployment succeeds but API doesn't respond

**Fix:** Ensure `railway.json` or `Procfile` has:

```json
{
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### Issue 3: Port Not Configured

**Symptom:** App crashes on startup

**Fix:** Use `$PORT` environment variable:

```python
# In main.py or uvicorn command
port = int(os.getenv("PORT", 8000))
```

### Issue 4: ChromaDB Path Issue

**Symptom:** Database errors

**Fix:** ChromaDB uses `./chroma_db` by default, which works in Railway's filesystem.

---

## Railway Configuration Files

### railway.json

Make sure you have this file in your repo:

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT"
  }
}
```

### requirements.txt

Ensure all dependencies are listed:

```
fastapi
uvicorn
chromadb
google-generativeai
biopython
python-dotenv
python-multipart
```

---

## Step-by-Step Deployment

### Complete Fresh Deployment:

1. **Clean slate:**
   - Delete old Railway deployment if exists
   - Start fresh

2. **Connect GitHub:**
   - Railway dashboard → New Project
   - Select NestWell repo

3. **Configure:**
   - Railway auto-detects Python
   - No build command needed (auto)

4. **Set variables:**
   ```
   GEMINI_API_KEY=your-key
   NCBI_EMAIL=your@email.com
   ```

5. **Deploy:**
   - Click "Deploy"
   - Wait for build to complete

6. **Test:**
   ```bash
   curl https://your-new-api.railway.app/
   ```

---

## After Successful Deployment

### Update Lovable

1. **Get your new Railway URL:**
   - In Railway dashboard
   - Copy the URL (e.g., `https://your-app.up.railway.app`)

2. **Update Lovable secret:**
   - Settings → Environment Variables
   - Update `NEXT_PUBLIC_API_URL` with new URL

3. **Redeploy Lovable** (should auto-redeploy)

4. **Test:**
   - Try ingredient checker again
   - Should work now!

---

## Quick Verification Checklist

After deploying Railway:

- [ ] Railway logs show "Application startup complete"
- [ ] `curl https://your-railway.app/` returns API info
- [ ] `curl -X POST https://your-railway.app/load-papers` returns data
- [ ] No errors in Railway logs
- [ ] Environment variables are set
- [ ] Lovable has the correct API URL

---

## If It Still Doesn't Work

### Debug Steps:

1. **Check Railway logs for errors**
2. **Test API manually with curl**
3. **Verify environment variables are set**
4. **Check if port is configured correctly**
5. **Try redeploying from scratch**

### Get Help:

- Railway docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check Railway status page

---

## Alternative: Use Render Instead

If Railway keeps having issues:

1. Go to https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy

See `RENDER_DEPLOY.md` for full instructions.

Good luck! 🚀
