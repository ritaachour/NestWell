# Lovable MVP Implementation - For Expecting & Postpartum Parents

## Target Audience
- Planning a family / Trying to conceive
- Pregnant women
- Postpartum / New mothers
- Lactating mothers

## MVP Scope: Single Ingredient Check

**Simplest Feature to Implement:** Let users quickly check ingredient safety for their family

**Why This is the Easiest:**
- No barcode scanning needed
- No ingredient parsing
- No database of products
- Just one input → one output
- Can reuse existing API endpoint
- **Saves parents time** - no need to research each ingredient

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
  const [lifeStage, setLifeStage] = useState('planning');
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleCheck = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch('/api/check-ingredient', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ingredient,
          productType,
          lifeStage
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to check ingredient');
      }
      
      const data = await response.json();
      setResult(data);
    } catch (error) {
      setError('Unable to check this ingredient. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold mb-3">
          Is this ingredient safe for my family?
        </h1>
        <p className="text-gray-600 text-lg">
          Get science-backed safety info in seconds, not hours of research
        </p>
      </div>

      {/* Life Stage Selector */}
      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
        <label className="block text-sm font-medium mb-2 text-gray-700">
          My stage:
        </label>
        <div className="flex flex-wrap gap-2">
          {[
            { value: 'planning', label: 'Planning pregnancy' },
            { value: 'pregnant', label: 'Pregnant' },
            { value: 'postpartum', label: 'Postpartum / Breastfeeding' },
            { value: 'general', label: 'General family safety' }
          ].map((stage) => (
            <button
              key={stage.value}
              onClick={() => setLifeStage(stage.value)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                lifeStage === stage.value
                  ? 'bg-blue-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {stage.label}
            </button>
          ))}
        </div>
      </div>

      {/* Input Form */}
      <div className="bg-white rounded-xl shadow-md p-6 mb-6">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700">
              What ingredient are you concerned about?
            </label>
            <input
              type="text"
              value={ingredient}
              onChange={(e) => setIngredient(e.target.value)}
              placeholder="e.g., parabens, phthalates, retinol, salicylic acid"
              className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg"
              onKeyPress={(e) => e.key === 'Enter' && handleCheck()}
            />
            <p className="text-xs text-gray-500 mt-1">
              Tip: Copy ingredient name from your product label
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2 text-gray-700">
              What type of product?
            </label>
            <select
              value={productType}
              onChange={(e) => setProductType(e.target.value)}
              className="w-full p-4 border-2 border-gray-300 rounded-lg focus:border-blue-500 focus:outline-none text-lg"
            >
              <option value="cosmetics">Skincare & Cosmetics</option>
              <option value="food">Food & Beverages</option>
              <option value="cleaning">Household Cleaning Products</option>
            </select>
          </div>

          <button
            onClick={handleCheck}
            disabled={!ingredient || loading}
            className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Checking research...' : 'Check Safety'}
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* Results */}
      {result && (
        <div className="space-y-4">
          {/* Risk Level Badge */}
          <div className={`rounded-xl p-6 text-center ${
            result.risk_level === 'Low Risk' 
              ? 'bg-green-50 border-2 border-green-500' 
              : result.risk_level === 'Moderate Risk'
              ? 'bg-yellow-50 border-2 border-yellow-500'
              : result.risk_level === 'High Risk'
              ? 'bg-red-50 border-2 border-red-500'
              : 'bg-gray-50 border-2 border-gray-400'
          }`}>
            <div className="text-5xl mb-2">
              {result.risk_level === 'Low Risk' ? '✓' : 
               result.risk_level === 'Moderate Risk' ? '⚠' :
               result.risk_level === 'High Risk' ? '✗' : '?'}
            </div>
            <h2 className="text-3xl font-bold mb-2">{result.risk_level}</h2>
            <p className="text-gray-700">
              Confidence: {result.confidence} • Based on {result.papers_analyzed} research papers
            </p>
          </div>

          {/* Assessment */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-2xl font-bold mb-4">What the research says:</h3>
            <div className="prose max-w-none text-gray-700 leading-relaxed whitespace-pre-line">
              {result.assessment}
            </div>
          </div>

          {/* Research Sources */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h3 className="text-2xl font-bold mb-4">Scientific Sources ({result.sources.length})</h3>
            <p className="text-gray-600 mb-4">
              Published research papers used in this assessment
            </p>
            <div className="space-y-3">
              {result.sources.map((source: any, idx: number) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2 hover:bg-gray-50 transition-colors">
                  <a 
                    href={source.url} 
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline font-medium block"
                  >
                    {source.title}
                  </a>
                  <div className="text-sm text-gray-600 mt-1">
                    {source.journal} • {source.year}
                    {source.is_clinical_trial && (
                      <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">
                        Clinical Trial
                      </span>
                    )}
                    <span className="ml-2 text-gray-500">Quality: {source.quality_score}/100</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Disclaimer */}
          <div className="bg-blue-50 border-l-4 border-blue-500 p-4 text-sm text-gray-700">
            <strong className="font-semibold">Important:</strong> This is a research-based tool, not medical advice. 
            Always consult with your healthcare provider about product use during pregnancy, breastfeeding, or when planning to conceive.
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
    const loadResponse = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        max_results: 15
      })
    });

    if (!loadResponse.ok) {
      throw new Error('Failed to load research papers');
    }

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

### Step 3: Add Environment Variable

In Lovable settings:
```
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

### Step 4: Update Home Page

Add link to ingredient checker with parent-focused messaging:

```tsx
<div className="text-center">
  <h1 className="text-5xl font-bold mb-4">
    Know what's safe for your growing family
  </h1>
  <p className="text-xl text-gray-600 mb-8">
    Research-backed ingredient safety for pregnancy, postpartum, and beyond
  </p>
  <Link 
    href="/ingredient-check"
    className="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700"
  >
    Check an ingredient →
  </Link>
</div>
```

---

## Key Features for Parents

✅ **Life stage context** - Results adjusted for pregnancy/breastfeeding  
✅ **Time-saving** - Instant research synthesis  
✅ **Trustworthy** - All sources are peer-reviewed research  
✅ **Actionable** - Clear risk levels and explanations  
✅ **Transparent** - Links to original research papers  
✅ **Safe** - Includes medical disclaimer  

---

## What This MVP Does

✅ User selects their stage (planning/pregnant/postpartum)  
✅ User enters ingredient name  
✅ Gets pregnancy/postpartum-specific safety assessment  
✅ Sees clear risk level with easy-to-understand explanation  
✅ Can read all source research papers  
✅ Saves hours of researching individual studies  

❌ **Future Features** (Not in MVP):
- Full product ingredient lists
- Barcode scanning
- Personalized recommendations
- Product alternatives
- Save history

---

## Testing the MVP

1. Go to `/ingredient-check`
2. Select "Pregnant" stage
3. Enter: "retinol"
4. Select: "Skincare & Cosmetics"
5. Click "Check Safety"
6. View results with pregnancy-specific information

---

## Next Steps After MVP

1. **Common concerns database** - Quick answers for BPA, phthalates, etc.
2. **Product ingredient lists** - Check full products, not just ingredients
3. **Favorites/Saved** - Save frequently checked ingredients
4. **Mobile app** - Barcode scanner for instant product check
5. **Community features** - Share safe products with other parents

But start with this simple ingredient checker - it solves the core problem of time-consuming research!
