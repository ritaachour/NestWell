# API Not Being Reached - Debugging Guide

## The Problem

You searched for "retinol" at 18:55, but Railway logs show no requests at that time.

**This means:** Your Lovable app isn't successfully calling the Railway API.

---

## Quick Debugging Steps

### Step 1: Verify Railway is Running

Test your Railway API directly:

```bash
curl https://web-production-b9b9.up.railway.app/
```

**Expected:** Should return API information

**If this fails:** Railway is down, check Railway dashboard

### Step 2: Check Lovable Secret Configuration

**In Lovable:**

1. Go to **Settings** → **Environment Variables** (or **Secrets**)
2. Find `NEXT_PUBLIC_API_URL`
3. Verify the value is exactly:
   ```
   https://web-production-b9b9.up.railway.app
   ```

**Common mistakes:**
- ❌ Missing the secret entirely
- ❌ Wrong URL
- ❌ Placeholder URL
- ❌ Trailing slash

### Step 3: Check Lovable API Route Logs

**In Lovable:**

1. Go to your API route logs
2. Look for errors when you click "Check Safety"
3. Check what URL it's trying to call

**Look for:**
- Network errors
- Timeout errors
- 404 errors
- "API_URL not configured" messages

### Step 4: Add Debug Logging

Update your Lovable API route to log what's happening:

```typescript
// app/api/check-ingredient/route.ts

export async function POST(request: Request) {
  try {
    const API_URL = process.env.NEXT_PUBLIC_API_URL;
    
    console.log('=== API Route Called ===');
    console.log('API_URL:', API_URL);
    console.log('Timestamp:', new Date().toISOString());
    
    const body = await request.json();
    console.log('Request body:', body);
    
    if (!API_URL) {
      console.error('ERROR: API_URL not configured');
      return NextResponse.json(
        { error: 'API URL not configured' },
        { status: 500 }
      );
    }
    
    console.log('Calling:', `${API_URL}/load-papers`);
    
    // ... rest of code
  }
}
```

Check Lovable logs after clicking "Check Safety" to see what's logged.

---

## Common Issues

### Issue 1: Secret Name Wrong

**Problem:** Secret named incorrectly

**Check:**
- Must be exactly: `NEXT_PUBLIC_API_URL`
- Case-sensitive
- No spaces

### Issue 2: Secret Value Wrong

**Problem:** URL is incorrect or placeholder

**Should be:**
```
https://web-production-b9b9.up.railway.app
```

**NOT:**
- `https://your-railway-app.railway.app` (placeholder)
- `http://web-production-b9b9.up.railway.app` (wrong protocol)
- `web-production-b9b9.up.railway.app` (missing https://)

### Issue 3: Not Redeployed After Secret Change

**Problem:** Changed secret but Lovable didn't redeploy

**Fix:**
1. Save secret in Lovable
2. Manually trigger redeploy
3. Wait for deployment to complete

### Issue 4: CORS Blocked

**Problem:** Railway rejecting requests from Lovable domain

**Check Railway logs for CORS errors**

**Fix in `main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Should allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Quick Test Checklist

- [ ] `curl https://web-production-b9b9.up.railway.app/` works
- [ ] Lovable has `NEXT_PUBLIC_API_URL` secret
- [ ] Secret value is correct URL (no placeholder)
- [ ] No trailing slash in URL
- [ ] Lovable redeployed after secret change
- [ ] Check Lovable logs for errors
- [ ] Check Railway logs for incoming requests

---

## Manual Test

Try calling the API from your local terminal:

```bash
# Test from command line (simulates what Lovable should do)
curl -X POST https://web-production-b9b9.up.railway.app/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "retinol cosmetics toxicity", "max_results": 3}'
```

**If this works:** API is fine, issue is in Lovable configuration  
**If this fails:** API has issues, check Railway logs

---

## Still Not Working?

### Get More Debugging Info

Add this to your Lovable page component:

```typescript
const handleCheck = async () => {
  console.log('Check button clicked');
  console.log('Environment:', process.env.NODE_ENV);
  console.log('API URL available:', !!process.env.NEXT_PUBLIC_API_URL);
  
  setLoading(true);
  try {
    console.log('Calling API...');
    const response = await fetch('/api/check-ingredient', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ingredient,
        productType,
        lifeStage
      })
    });
    
    console.log('Response status:', response.status);
    const data = await response.json();
    console.log('Response data:', data);
    
  } catch (error) {
    console.error('Error:', error);
  } finally {
    setLoading(false);
  }
};
```

Check browser console (F12) for these logs.

---

## Expected Flow

When working correctly:

1. User clicks "Check Safety" at 18:55
2. Browser console shows logs
3. Lovable API route logs show request
4. Railway logs show incoming request at 18:55
5. Railway processes request
6. Response sent back
7. User sees results

If step 4 is missing, Lovable isn't reaching Railway!

Good luck debugging! 🚀
