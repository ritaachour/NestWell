# Lovable MVP Implementation

## MVP Scope: Single Ingredient Check

**Simplest Feature to Implement:** Let users check the safety of a single ingredient (e.g., "parabens in cosmetics")

**Why This is the Easiest:**
- No barcode scanning needed
- No ingredient parsing
- No database of products
- Just one input → one output
- Can reuse existing API endpoint

---

## Implementation Steps

### Step 1: Create Simple Ingredient Checker

Create a new page: `app/ingredient-check/page.tsx`

```tsx
'use client';

import { useState } from 'react';

export default function IngredientCheck() {
  const [ingredient, setIngredient] = useState('');
  const [productType, setProductType] = useState('cosmetics');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
    setLoading(true);
    try {
      const response = await fetch('/api/check-ingredient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredient,
          productType,
          usageFrequency: 'daily'
        })
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error('Failed to check ingredient:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Check Ingredient Safety</h1>
      
      <div className="space-y-4 mb-6">
        <div>
          <label className="block text-sm font-medium mb-2">
            Ingredient Name
          </label>
          <input
            type="text"
            value={ingredient}
            onChange={(e) => setIngredient(e.target.value)}
            placeholder="e.g., parabens, phthalates, BPA"
            className="w-full p-3 border rounded-lg"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-2">
            Product Type
          </label>
          <select
            value={productType}
            onChange={(e) => setProductType(e.target.value)}
            className="w-full p-3 border rounded-lg"
          >
            <option value="cosmetics">Cosmetics & Skincare</option>
            <option value="food">Food & Beverages</option>
            <option value="cleaning">Cleaning Products</option>
          </select>
        </div>

        <button
          onClick={handleCheck}
          disabled={!ingredient || loading}
          className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Checking...' : 'Check Safety'}
        </button>
      </div>

      {result && (
        <div className="mt-8 p-6 border rounded-lg bg-white">
          <h2 className="text-2xl font-bold mb-4">
            {result.risk_level}
          </h2>
          
          <div className="prose max-w-none mb-6">
            <div dangerouslySetInnerHTML={{ 
              __html: result.assessment.replace(/\n/g, '<br>')
            }} />
          </div>

          <div className="border-t pt-4">
            <h3 className="font-semibold mb-2">Sources:</h3>
            <ul className="space-y-2">
              {result.sources.map((source: any, idx: number) => (
                <li key={idx} className="text-sm">
                  <a 
                    href={source.url} 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline"
                  >
                    {source.title}
                  </a>
                  <span className="text-gray-600 ml-2">
                    ({source.journal}, {source.year})
                  </span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
```

### Step 2: Create API Route

Create: `app/api/check-ingredient/route.ts`

```typescript
import { NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Load papers first (if not already loaded)
    await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `${body.ingredient} ${body.productType} toxicity`,
        max_results: 10
      })
    });

    // Get assessment
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: body.usageFrequency || 'daily',
        min_quality_score: 30,
        max_papers: 5
      })
    });

    const data = await assessmentResponse.json();
    
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message },
      { status: 500 }
    );
  }
}
```

### Step 3: Add Environment Variable

In Lovable settings:
```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

### Step 4: Update Home Page

Add link to the ingredient checker on your homepage.

---

## Consumer-Friendly Formatting

The API response needs to be formatted for consumers. Add this helper function:

```typescript
// lib/formatAssessment.ts

export function formatAssessment(apiResponse: any) {
  const riskColors: Record<string, string> = {
    'Low Risk': 'text-green-600 bg-green-50 border-green-200',
    'Moderate Risk': 'text-yellow-600 bg-yellow-50 border-yellow-200',
    'High Risk': 'text-red-600 bg-red-50 border-red-200',
    'Insufficient Data': 'text-gray-600 bg-gray-50 border-gray-200'
  };

  const icon: Record<string, string> = {
    'Low Risk': '✓',
    'Moderate Risk': '⚠',
    'High Risk': '⚠',
    'Insufficient Data': '?'
  };

  return {
    ...apiResponse,
    riskColor: riskColors[apiResponse.risk_level] || riskColors['Insufficient Data'],
    riskIcon: icon[apiResponse.risk_level] || '?'
  };
}
```

---

## What This MVP Does

✅ **User types ingredient name** (e.g., "parabens")  
✅ **Selects product type** (cosmetics, food, cleaning)  
✅ **Gets simple safety rating** (Low/Moderate/High Risk)  
✅ **Sees research-based explanation**  
✅ **Can read source papers**

❌ **Future Features** (Not in MVP):
- Barcode scanning
- Full ingredient list analysis
- Product database
- Profile/history
- Alternatives suggestions

---

## Testing the MVP

1. Visit: `/ingredient-check`
2. Enter: "parabens"
3. Select: "cosmetics"
4. Click: "Check Safety"
5. View results with links to research papers

---

## Next Steps After MVP

Once this works, you can add:
1. **Multiple ingredients** - parse ingredient lists
2. **Products database** - store common products
3. **Barcode scanner** - camera input for UPC codes
4. **User profiles** - save history and preferences
5. **Alternatives** - suggest safer products

But start simple! Get one ingredient check working perfectly first.
