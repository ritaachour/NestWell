# Troubleshooting "Unable to check ingredient" Error (404)

## The Problem

You're getting a 404 error when trying to load papers. This means your API endpoint isn't being found.

**Error:** `POST //load-papers 404`

## Quick Fixes

### Fix 1: Check Your API is Running

**Test your Railway API:**

```bash
curl https://your-railway-app.railway.app/
```

**Expected:** Should return API information
**If this fails:** Your Railway deployment isn't running or crashed

---

### Fix 2: Verify the API URL in Lovable

**In Lovable, check your secret:**

1. Go to Settings → Environment Variables (or Secrets)
2. Verify `NEXT_PUBLIC_API_URL` is set
3. Make sure it's your **actual Railway URL**, not a placeholder

**Should be:**
```
https://your-actual-railway-app.up.railway.app
```

**NOT:**
```
https://your-railway-app.railway.app  # placeholder
```

---

### Fix 3: Check Railway Logs

**On Railway dashboard:**

1. Go to your Railway project
2. Click on your service
3. Go to "Logs" tab
4. Look for errors

**Common issues:**
- ❌ API crashed on startup
- ❌ Missing environment variables
- ❌ Python dependencies failed to install
- ❌ Port conflict

---

### Fix 4: Restart Railway Deployment

**On Railway:**

1. Go to your deployment
2. Click "Redeploy" or "Restart"
3. Wait for it to finish
4. Test again: `curl https://your-railway-app.railway.app/`

---

## Step-by-Step Debugging

### Step 1: Test API Directly

```bash
# Test if API is alive
curl https://your-railway-app.railway.app/

# Should return JSON with API info
# If not, Railway deployment has issues
```

### Step 2: Test the Endpoint

```bash
# Test load-papers endpoint
curl -X POST https://your-railway-app.railway.app/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens", "max_results": 5}'

# If this works, issue is in Lovable code
# If this fails, issue is in Railway deployment
```

### Step 3: Check Lovable Code

**In your API route (`app/api/check-ingredient/route.ts`):**

Make sure it's using the environment variable correctly:

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Add debugging
console.log('API_URL:', API_URL);

if (!API_URL) {
  throw new Error('API_URL not configured');
}
```

---

## Common Issues

### Issue 1: Double Slash in Path

**Problem:** Path has `//load-papers` instead of `/load-papers`

**Fix:** In your API route code, ensure you're not adding an extra slash:

```typescript
// ❌ BAD
const response = await fetch(`${API_URL}//load-papers`);

// ✅ GOOD
const response = await fetch(`${API_URL}/load-papers`);
```

### Issue 2: Environment Variable Not Set

**Problem:** `process.env.NEXT_PUBLIC_API_URL` is undefined

**Fix:**
1. Go to Lovable settings
2. Add secret: `NEXT_PUBLIC_API_URL`
3. Value: Your Railway URL
4. Redeploy Lovable app

### Issue 3: Railway Service Not Running

**Problem:** Railway deployment crashed or isn't running

**Fix:**
1. Check Railway logs for errors
2. Restart the deployment
3. Ensure all environment variables are set:
   - `GEMINI_API_KEY`
   - `NCBI_EMAIL`
   - `PORT` (usually auto-set)

### Issue 4: CORS Error

**Problem:** Railway is rejecting requests from Lovable domain

**Check:** Make sure `main.py` has CORS enabled:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Quick Check List

- [ ] Railway API is running (test with curl)
- [ ] `NEXT_PUBLIC_API_URL` is set in Lovable
- [ ] API URL doesn't have trailing slash
- [ ] Railway logs show no errors
- [ ] All Railway environment variables are set
- [ ] CORS is enabled in your backend
- [ ] Both services are deployed

---

## Still Not Working?

**Last resort - check your API route code:**

```typescript
// app/api/check-ingredient/route.ts

import { NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function POST(request: Request) {
  try {
    console.log('API_URL:', API_URL); // Debug line
    
    if (!API_URL) {
      return NextResponse.json(
        { error: 'API URL not configured' },
        { status: 500 }
      );
    }

    const body = await request.json();
    
    console.log('Calling:', `${API_URL}/load-papers`); // Debug line
    
    const loadResponse = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `${body.ingredient} ${body.productType} toxicity`,
        max_results: 15
      })
    });

    console.log('Response status:', loadResponse.status); // Debug line

    // ... rest of code
  }
}
```

Check Lovable logs to see what's actually being called.

---

## Success Checklist

When it works, you should see:
- ✅ API responds to `curl https://your-api.railway.app/`
- ✅ No errors in Railway logs
- ✅ Lovable can reach the API
- ✅ Ingredient checker returns results

Good luck! 🚀
