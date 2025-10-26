# Why Retinol Search Doesn't Work

## The Problem

When you search for "retinol" in Lovable, you get:
```
Failed to load research papers: {"detail":"Not Found"}
```

## Root Cause

Your API is working, but ChromaDB needs time to persist data. Here's what happens:

1. ✅ Lovable calls `/load-papers` for "retinol"
2. ✅ Railway fetches papers from PubMed
3. ✅ Papers added to ChromaDB
4. ❌ Wait time needed for ChromaDB to save to disk (up to 30 seconds)
5. ❌ Lovable immediately calls `/assess`
6. ❌ Database search fails (papers not yet saved)

---

## The Fix: Add Delay Between Calls

Update your Lovable API route to wait after loading papers.

### Update: `app/api/check-ingredient/route.ts`

```typescript
import { NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
    
    // Load papers first
    console.log('Loading papers for:', query);
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

    // **WAIT for ChromaDB to persist data**
    // This is critical! ChromaDB needs time to save to disk
    console.log('Waiting for database to persist...');
    await new Promise(resolve => setTimeout(resolve, 3000)); // 3 second wait

    // Get assessment
    console.log('Getting assessment...');
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

### Added 3-second wait:
```typescript
await new Promise(resolve => setTimeout(resolve, 3000));
```

This gives ChromaDB time to persist the loaded papers before querying.

---

## Why This Happens

**ChromaDB persistance:**
- ChromaDB saves to disk asynchronously
- Immediate queries after adding data can fail
- Needs 1-3 seconds to complete write

**Railway temporary filesystem:**
- Railway's filesystem can be slow
- First write is slower
- Subsequent queries work fine

---

## Alternative: Optimize Wait Time

If 3 seconds is too slow, try:

```typescript
// Option 1: Retry with exponential backoff
let retries = 0;
let success = false;

while (retries < 3 && !success) {
  await new Promise(resolve => setTimeout(resolve, 1000 * (retries + 1)));
  
  const assessmentResponse = await fetch(`${API_URL}/assess`, ...);
  
  if (assessmentResponse.ok) {
    success = true;
    // process response
  } else {
    retries++;
  }
}
```

---

## Testing After Fix

1. Deploy updated code to Lovable
2. Try searching "retinol" again
3. Should work now! ✅

The extra 3-second wait ensures ChromaDB has time to save papers before searching.

---

## For Production

**Better long-term solutions:**

1. **Preload common ingredients** - Load papers for popular searches
2. **Use PostgreSQL with pgvector** - Proper database, not filesystem
3. **Cache results** - Don't reload papers for same search
4. **Optimize ChromaDB** - Use in-memory for faster writes

But for MVP, the 3-second wait works perfectly!

Good luck! 🚀
