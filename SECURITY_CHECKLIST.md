# Security Checklist for Lovable Deployment

## ⚠️ Critical: Never Expose Sensitive Information

### What NOT to Commit to Lovable

❌ **Never commit these to Lovable:**
- API keys (Gemini, etc.)
- Email addresses
- Passwords
- Database credentials
- Private SSH keys
- Personal information

✅ **Safe to commit:**
- Code files
- Public URLs
- Documentation
- Environment variable **names** (not values)

---

## Pre-Deployment Security Check

### 1. Check Your Code Files

**Before deploying, search for:**

```bash
# In Lovable, search for these patterns:
AIza          # Gemini API key pattern
sk-ant-       # Anthropic API key pattern
sk-           # OpenAI API key pattern
@gmail.com    # Email addresses
password      # Obvious passwords
```

### 2. Verify Environment Variables

**✅ Correct Setup:**

In Lovable Settings → Environment Variables:
```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

**❌ NEVER do this in code:**
```typescript
// ❌ BAD - hardcoded API key
const API_KEY = "AIzaSyDqi2ntfLK77TR1UuyyeHcAt6cLXGu0tUI";

// ✅ GOOD - use environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL;
```

### 3. API Route Security Check

**✅ SAFE API Route Code:**

```typescript
// app/api/check-ingredient/route.ts

import { NextResponse } from 'next/server';

// ✅ Environment variable loaded securely
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // ✅ No sensitive data in client-side code
    // ✅ API calls happen server-side
    
    const response = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `${body.ingredient} ${body.productType} toxicity`,
        max_results: 15
      })
    });
    
    // ... rest of code
  }
}
```

**Key Points:**
- ✅ Environment variables used server-side only
- ✅ API calls happen in API route (not client)
- ✅ No API keys in client-side code
- ✅ Sensitive operations stay on server

### 4. Frontend Code Security

**✅ SAFE Client-Side Code:**

```typescript
// app/ingredient-check/page.tsx

'use client';

export default function IngredientCheck() {
  // ✅ Only user input, no sensitive data
  const [ingredient, setIngredient] = useState('');
  
  const handleCheck = async () => {
    // ✅ Calls YOUR API route, not external API directly
    const response = await fetch('/api/check-ingredient', {
      method: 'POST',
      body: JSON.stringify({
        ingredient,  // User input only
        productType,
        lifeStage
      })
    });
  };
}
```

**Why This is Safe:**
- ✅ No API keys in client code
- ✅ Calls internal API route
- ✅ API route handles external API calls
- ✅ Sensitive data stays on server

---

## What's Exposed to Users?

### ✅ Safe for Users to See:
- Ingredient names (user input)
- Product types (user input)
- Results from your API
- Research paper URLs
- Your domain name

### ❌ NEVER Exposed:
- Your backend API URL (should be server-side)
- API keys (Gemini, etc.)
- Email addresses
- Internal server details
- Database credentials

---

## Browser DevTools Check

**Test what's exposed:**

1. Open your deployed Lovable site
2. Open browser DevTools (F12)
3. Go to Network tab
4. Use the ingredient checker
5. Check if any API keys are visible in requests

**What you should see:**
- ✅ Calls to `/api/check-ingredient` (your API route)
- ✅ No direct calls to external APIs with keys
- ✅ No API keys in request headers

**What you should NOT see:**
- ❌ Calls to Railway/Render API with credentials
- ❌ API keys in any requests
- ❌ Sensitive headers

---

## Environment Variables in Lovable

### How to Set (Correct):

1. Open Lovable project settings
2. Go to **Environment Variables**
3. Add: `NEXT_PUBLIC_API_URL`
4. Value: `https://your-railway-app.railway.app`
5. **Do NOT include credentials in URL**

### ❌ Wrong:
```
NEXT_PUBLIC_API_URL=https://username:password@your-api.com
```

### ✅ Right:
```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Hardcoding in Component

```typescript
// ❌ DON'T DO THIS
const response = await fetch('https://api.railway.app/assess', {
  headers: {
    'Authorization': 'Bearer AIzaSyDqi2ntfLK77TR1UuyyeHcAt6cLXGu0tUI'
  }
});
```

### ✅ Correct: Use API Route

```typescript
// ✅ DO THIS
const response = await fetch('/api/check-ingredient', {
  body: JSON.stringify({ ingredient, productType })
});
```

### ❌ Mistake 2: Exposing Server URLs in Client

```typescript
// ❌ DON'T EXPOSE TO CLIENT
const API_URL = 'https://secret-internal-api.railway.app';
```

### ✅ Correct: Keep Server-Side

```typescript
// ✅ SERVER-SIDE ONLY (in API route)
const API_URL = process.env.NEXT_PUBLIC_API_URL;
```

---

## Security Verification Steps

### Before Launching:

1. ✅ **No API keys in code** - Search entire project
2. ✅ **No emails in code** - Check all files
3. ✅ **Environment variables set** - Lovable settings
4. ✅ **API routes used** - Client calls internal routes
5. ✅ **No sensitive data in logs** - Check deployment logs
6. ✅ **CORS configured** - Backend only accepts your domain

### After Launching:

1. ✅ **Test in browser DevTools** - Check network tab
2. ✅ **View page source** - No keys visible
3. ✅ **Check browser console** - No errors with sensitive data
4. ✅ **Test API directly** - Should require auth
5. ✅ **Monitor logs** - No credentials logged

---

## If You Accidentally Exposed Keys

**Immediate Action:**

1. 🔴 **Regenerate API key immediately**
2. 🔴 **Update environment variable**
3. 🔴 **Redeploy application**
4. 🔴 **Review Git history** (if possible, remove from history)
5. 🔴 **Monitor for unauthorized use**

**For Your Case:**
- Your Gemini API key was exposed in documentation
- ✅ You've already removed it
- ✅ Replace with new key before launch
- ✅ Old commits in Git history still have it (okay if repo is private)

---

## Quick Security Checklist

Before deploying to Lovable:

- [ ] No API keys in any `.tsx` or `.ts` files
- [ ] No API keys in any `.env` files (committed)
- [ ] Environment variables set in Lovable (not in code)
- [ ] All sensitive API calls happen in API routes
- [ ] Client code only calls internal routes (`/api/*`)
- [ ] Tested in DevTools - no exposed credentials
- [ ] Regenerated any previously exposed keys
- [ ] Reviewed all code for hardcoded secrets

---

## Summary

**Your code should be safe because:**

1. ✅ API calls happen in API route (server-side)
2. ✅ Environment variables used, not hardcoded
3. ✅ Client code only interacts with your API routes
4. ✅ No API keys in component code
5. ✅ Sensitive operations stay on server

**The architecture protects you:**
```
User Browser → /api/check-ingredient → Your Server → External API
     ↑                                            ↑
     └──────────── No keys here ──────────────┘
```

Your API route acts as a secure proxy, keeping all credentials server-side where users can't see them.
