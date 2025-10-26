# Fix: Double Slash 404 Error (//load-papers)

## The Problem

Railway logs show `POST //load-papers 404` with a **double slash** (`//`) which causes a 404.

The path should be `/load-papers` not `//load-papers`.

---

## Root Cause

This happens when your API URL has a trailing slash, and the code also adds a slash before the endpoint.

**Example:**
```typescript
// API_URL = "https://api.railway.app/" (has trailing slash)
// Code does: API_URL + "/load-papers"
// Result: "https://api.railway.app//load-papers" ❌ WRONG
```

---

## The Fix

### Option 1: Remove Trailing Slash from API URL

**In Lovable Settings:**
1. Go to Environment Variables
2. Update `NEXT_PUBLIC_API_URL`
3. Make sure it has **NO trailing slash**:

**❌ Wrong:**
```
https://web-production-b9b9.up.railway.app/
```

**✅ Correct:**
```
https://web-production-b9b9.up.railway.app
```

### Option 2: Fix in Code

Update your Lovable API route to handle trailing slashes:

```typescript
// app/api/check-ingredient/route.ts

const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';
// Remove trailing slash if present

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Load papers
    const loadResponse = await fetch(`${API_URL}/load-papers`, {
      // Now guaranteed to have exactly one slash
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `${body.ingredient} ${body.productType} toxicity`,
        max_results: 15
      })
    });
    
    // Wait 3 seconds for ChromaDB persistence
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    // Get assessment
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      // Same fix here
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: 'daily',
        min_quality_score: 30,
        max_papers: 5
      })
    });
    
    // ... rest of code
  }
}
```

---

## Key Change

```typescript
// ❌ BEFORE
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ✅ AFTER
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';
```

The `.replace(/\/$/, '')` removes any trailing slash.

---

## Verification

After fixing, check Railway logs. You should see:

**Before:**
```
POST //load-papers 404 ❌
```

**After:**
```
POST /load-papers 200 ✅
```

---

## Why This Happens

Lovable might auto-add a trailing slash to URLs, or you might have accidentally added one when setting the environment variable.

The fix ensures it works regardless of whether the trailing slash is there or not.

---

## Complete Fixed Code

```typescript
import { NextResponse } from 'next/server';

// Remove trailing slash if present
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Build query with life stage context
    let query = `${body.ingredient} ${body.productType} toxicity`;
    
    if (body.lifeStage === 'pregnant') {
      query += ' pregnancy effects';
    } else if (body.lifeStage === 'postpartum') {
      query += ' breastfeeding lactation effects';
    } else if (body.lifeStage === 'planning') {
      query += ' fertility reproductive effects';
    }
    
    console.log('Calling:', `${API_URL}/load-papers`);
    
    // Load papers first
    const loadResponse = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        max_results: 15
      })
    });

    if (!loadResponse.ok) {
      const errorText = await loadResponse.text();
      console.error('Failed to load papers:', errorText);
      throw new Error('Failed to load research papers');
    }

    const loadData = await loadResponse.json();
    console.log('Papers loaded:', loadData.papers_loaded);

    // **WAIT for ChromaDB to persist** (3 seconds)
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Get assessment
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: 'daily',
        min_quality_score: 30,
        max_papers: 5
      })
    });

    if (!assessmentResponse.ok) {
      const errorText = await assessmentResponse.text();
      console.error('Failed to get assessment:', errorText);
      throw new Error('Failed to generate assessment');
    }

    const data = await assessmentResponse.json();
    
    // Add life stage context
    if (data.assessment && body.lifeStage !== 'general') {
      const lifeStageContext = {
        'pregnant': 'during pregnancy',
        'postpartum': 'while breastfeeding',
        'planning': 'when planning a pregnancy'
      }[body.lifeStage] || '';
      
      if (lifeStageContext) {
        data.assessment = `${data.assessment}\n\nNote: This assessment has been weighted toward evidence specific to ${lifeStageContext}.`;
      }
    }
    
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Unable to check ingredient. Please try again.' },
      { status: 500 }
    );
  }
}
```

---

## After Applying Fix

1. Deploy the updated code to Lovable
2. Try searching for "retinol" again
3. Check Railway logs - should see `/load-papers` (not `//load-papers`)
4. Should work! ✅

Good luck! 🚀
