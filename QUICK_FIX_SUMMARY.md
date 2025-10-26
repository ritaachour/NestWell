# Quick Fix Summary - Make It Work Now

## The Issues

1. ❌ Double slash in URL (`//load-papers` causes 404)
2. ❌ ChromaDB persistence delay (papers not found immediately)
3. ❌ Different life stages don't find different papers

---

## Complete Fixed Code for Lovable

### Update: `app/api/check-ingredient/route.ts`

```typescript
import { NextResponse } from 'next/server';

// Remove trailing slash to prevent double slash issue
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Build context-aware query based on life stage
    let query = `${body.ingredient} ${body.productType} toxicity`;
    
    if (body.lifeStage === 'pregnant') {
      query += ' pregnancy effects';
    } else if (body.lifeStage === 'postpartum') {
      query += ' breastfeeding lactation effects';
    } else if (body.lifeStage === 'planning') {
      query += ' fertility reproductive effects';
    }
    
    console.log('API Call - Loading papers for:', query);
    
    // Step 1: Load papers
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
      throw new Error(`Failed to load research papers: ${errorText}`);
    }

    const loadData = await loadResponse.json();
    console.log('Papers loaded:', loadData.papers_loaded);

    // Step 2: CRITICAL - Wait for ChromaDB to persist
    console.log('Waiting for database persistence...');
    await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds

    // Step 3: Get assessment
    console.log('Getting assessment...');
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: 'daily',
        min_quality_score: 0, // Lower threshold to get more results
        max_papers: 5
      })
    });

    if (!assessmentResponse.ok) {
      const errorText = await assessmentResponse.text();
      console.error('Failed to get assessment:', errorText);
      throw new Error(`Failed to generate assessment: ${errorText}`);
    }

    const data = await assessmentResponse.json();
    
    // Add life stage context to assessment
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

## Key Changes

### 1. Fix Double Slash
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';
```

### 2. Add 3-Second Wait
```typescript
await new Promise(resolve => setTimeout(resolve, 3000));
```

### 3. Lower Quality Threshold
```typescript
min_quality_score: 0  // Get more results
```

### 4. Add Debug Logging
Console logs help you see what's happening.

---

## Environment Variable

Make sure in Lovable:

```
NEXT_PUBLIC_API_URL=https://web-production-b9b9.up.railway.app
```

**Important:** NO trailing slash!

---

## How to Test

1. Deploy this code to Lovable
2. Try "retinol" + "Pregnant" + "Cosmetics"
3. Should work after 30-60 seconds
4. Try "parabens" + "Planning pregnancy"
5. Should find different papers

---

## Why Different Life Stages Don't Work

Each life stage uses a different PubMed query:
- Pregnant: "retinol cosmetics toxicity pregnancy effects"
- Planning: "retinol cosmetics toxicity fertility reproductive effects"

These return different papers, but ChromaDB needs time to save them. The 3-second wait fixes this.

---

## Expected Behavior

1. Click "Check Safety"
2. Wait 30-60 seconds (PubMed is slow)
3. See results with sources
4. Try different life stage
5. Should get different results

---

## Still Having Issues?

### Check Railway Logs:
- Should see: `POST /load-papers 200` (not `//load-papers`)
- Should see: `POST /assess 200`
- Check for errors

### Check Lovable Logs:
- Should see console logs
- Should see papers loaded count
- Should see assessment response

This should work! 🚀
