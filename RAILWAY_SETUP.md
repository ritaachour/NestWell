# Railway Setup Guide

## Railway Configuration vs Environment Variables

Your `railway.toml` file configures how Railway runs your app. Environment variables are separate.

## Setting Environment Variables

### Method 1: Railway Web Dashboard (Recommended)

1. Go to https://railway.app
2. Click on your project
3. Go to "Variables" tab (left sidebar)
4. Click "New Variable"
5. Add these variables:

```
Name: GEMINI_API_KEY
Value: your-gemini-api-key-here

Name: NCBI_EMAIL  
Value: your@email.com
```

6. Click "Add Variable" for each one

### Method 2: Railway CLI

```bash
# Set variables from command line
railway variables set GEMINI_API_KEY=your-key-here
railway variables set NCBI_EMAIL=your@email.com
```

### Method 3: From Local .env File

```bash
# Railway can read your local .env file
railway variables set --from .env
```

## What is railway.json?

Your `railway.json` file tells Railway:
- How to build your app
- Which command to start your server
- How many instances to run
- Restart policies

It does NOT contain your API keys or secrets - those go in Environment Variables.

## Deploy

After setting environment variables:

```bash
# Deploy to Railway
railway up
```

Or if using GitHub integration, just push:
```bash
git push
```

Railway automatically deploys when you push to main branch.

## Verify Variables Are Set

```bash
# Check variables in Railway dashboard
# Or via CLI:
railway variables
```

## The Diffusion

**railway.json** = Configuration (how to run)
- Build settings
- Start commands
- Scaling settings
- NOT secrets!

**Environment Variables** = Secrets & Settings (what to use)
- API keys
- Database URLs
- Email addresses
- Your actual secrets!

## Complete Railway Setup

1. ✅ Create railway.json (already done)
2. ✅ Push code to GitHub
3. ⬜ Connect to Railway
4. ⬜ Set environment variables in Railway dashboard
5. ⬜ Deploy!

## Quick Start

```bash
# 1. Login to Railway
railway login

# 2. Initialize project
railway init

# 3. Set environment variables
railway variables set GEMINI_API_KEY=your-key
railway variables set NCBI_EMAIL=your@email.com

# 4. Deploy
railway up
```

Done! Your API will be live at https://your-project.railway.app
