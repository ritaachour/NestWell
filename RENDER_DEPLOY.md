# Deploy to Render.com (Alternative to Railway)

If Railway is having build issues, Render.com is a reliable alternative.

## Setup on Render

### Step 1: Create Account

1. Go to https://render.com
2. Sign up with GitHub

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select NestWell repository

### Step 3: Configure Build

**Settings:**
- **Name:** nestwell-api
- **Environment:** Python 3
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Plan:** Free

### Step 4: Add Environment Variables

Click "Environment" tab and add:

```
GEMINI_API_KEY=your-key
NCBI_EMAIL=your@email.com
```

### Step 5: Deploy

Click "Create Web Service" and wait for deployment.

## Why Render Might Work Better

- Better Python build environment
- More reliable dependency installation
- Free tier available
- Automatic HTTPS
- Persistent URLs

## After Deployment

Your API will be at: `https://nestwell-api.onrender.com`

Update your Lovable frontend:
```
NEXT_PUBLIC_API_URL=https://nestwell-api.onrender.com
```

## Render vs Railway

| Feature | Render | Railway |
|---------|--------|---------|
| Python Support | Excellent | Good |
| Free Tier | Yes | Yes |
| Build Reliability | High | Medium |
| Setup Complexity | Easy | Medium |

**Recommendation:** Try Render if Railway continues to have issues.
