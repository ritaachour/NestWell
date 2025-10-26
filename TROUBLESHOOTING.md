# Troubleshooting Guide

## Common Deployment Issues

### Build Fails with "exit code 1" or pydantic errors

**Problem:** Dependencies fail to install during Railway build

**Solutions:**

1. **Use Dockerfile (Current Solution)**
   - Dockerfile is already created
   - Includes all necessary build tools
   - Railway will automatically use it

2. **If Docker doesn't work, try Nixpacks:**
   - Change railway.json to use `"builder": "NIXPACKS"`
   - Add `nixpacks.toml` file for custom build steps

3. **Pin Python version:**
   - runtime.txt is already set to Python 3.11
   - Ensures consistent builds

### Application Won't Start

**Check Environment Variables:**
```bash
# In Railway dashboard, verify:
GEMINI_API_KEY is set
NCBI_EMAIL is set
PORT is automatically set by Railway
```

### ChromaDB Errors

**Problem:** Vector database not persisting

**Solution:**
- ChromaDB uses local filesystem (temporary on Railway)
- Data resets when app restarts
- For production, consider PostgreSQL with pgvector

### Papers Not Loading

**Problem:** PubMed API returns no results

**Check:**
1. NCBI_EMAIL environment variable is set
2. Internet connection is working
3. Rate limits: PubMed allows 3 requests/second

### Testing Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Test with Docker locally
docker build -t nestwell-api .
docker run -p 8000:8000 --env-file .env nestwell-api

# Or run directly
uvicorn main:app --reload
```

## Railway-Specific Issues

### Build Timeout

**Problem:** Build takes too long

**Solution:**
- Dockerfile already optimizes build cache
- Layers are cached for faster rebuilds

### Memory Issues

**Problem:** App crashes with memory errors

**Solution:**
- Free tier has 512MB RAM
- Upgrade for more memory
- Or optimize ChromaDB usage

### Deployment Fails

**Problem:** Deploy button doesn't work

**Solution:**
1. Check Railway dashboard logs
2. Verify all files are committed to Git
3. Ensure railway.json is in repository
4. Try manual deploy from CLI: `railway up`

## Quick Fixes

### Reset Everything
```bash
# In Railway dashboard:
1. Delete current deployment
2. Clear environment variables
3. Re-add environment variables
4. Redeploy
```

### Check Logs
```bash
railway logs
# Or in Railway dashboard: View Logs tab
```

## Still Having Issues?

1. Check Railway status: https://railway.statuspage.io/
2. Review Railway documentation
3. Check GitHub issues for similar problems
4. Verify your .env file works locally first
