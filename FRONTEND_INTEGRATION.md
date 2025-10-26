# Frontend Integration Guide

Integration guide for connecting the Toxicity Assessment RAG API with your Lovable frontend.

## Setup

### 1. Environment Variable

In your Lovable project settings, add:

```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

Replace with your deployed API URL (Railway, Render, etc.)

### 2. API Client

Create or update your API client in Lovable:

```typescript
// lib/api.ts or similar

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface AssessmentRequest {
  substance: string;
  product_type: string;
  usage_frequency: string;
  min_quality_score?: number;
  max_papers?: number;
}

export interface AssessmentResponse {
  risk_level: string;
  confidence: string;
  assessment: string;
  sources: Source[];
  papers_analyzed: number;
  avg_quality_score: number;
}

export interface Source {
  pmid: string;
  title: string;
  journal: string;
  year: string;
  quality_score: number;
  is_clinical_trial: boolean;
  url: string;
}

export interface LoadPapersRequest {
  query: string;
  max_results: number;
}

export interface LoadPapersResponse {
  papers_loaded: number;
  average_quality_score: number;
  clinical_trial_count: number;
  message: string;
}

export const toxicityAPI = {
  async assess(request: AssessmentRequest): Promise<AssessmentResponse> {
    const response = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    if (!response.ok) throw new Error('Assessment failed');
    return response.json();
  },

  async loadPapers(request: LoadPapersRequest): Promise<LoadPapersResponse> {
    const response = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request)
    });
    if (!response.ok) throw new Error('Failed to load papers');
    return response.json();
  },

  async getStats() {
    const response = await fetch(`${API_URL}/stats`);
    if (!response.ok) throw new Error('Failed to get stats');
    return response.json();
  }
};
```

## UI Components

### Assessment Form Component

```typescript
'use client';

import { useState } from 'react';
import { toxicityAPI, type AssessmentResponse } from '@/lib/api';

export default function AssessmentForm() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AssessmentResponse | null>(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const formData = new FormData(e.currentTarget);
    
    try {
      const assessment = await toxicityAPI.assess({
        substance: formData.get('substance') as string,
        product_type: formData.get('product_type') as string,
        usage_frequency: formData.get('usage_frequency') as string,
        min_quality_score: parseInt(formData.get('min_quality_score') as string) || 50,
        max_papers: parseInt(formData.get('max_papers') as string) || 5
      });
      setResult(assessment);
    } catch (err) {
      setError('Failed to get assessment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label>Substance Name</label>
          <input
            name="substance"
            required
            className="w-full p-2 border rounded"
            placeholder="e.g., parabens"
          />
        </div>

        <div>
          <label>Product Type</label>
          <select name="product_type" className="w-full p-2 border rounded">
            <option value="cosmetics">Cosmetics</option>
            <option value="food">Food Additives</option>
            <option value="cleaning">Cleaning Products</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div>
          <label>Usage Frequency</label>
          <select name="usage_frequency" className="w-full p-2 border rounded">
            <option value="daily">Daily</option>
            <option value="weekly">Several times per week</option>
            <option value="monthly">Monthly</option>
            <option value="rarely">Rarely</option>
          </select>
        </div>

        <div>
          <label>Minimum Quality Score: {50}</label>
          <input
            type="range"
            name="min_quality_score"
            min="0"
            max="100"
            defaultValue="50"
            className="w-full"
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white p-3 rounded hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? 'Analyzing...' : 'Get Assessment'}
        </button>
      </form>

      {error && <div className="mt-4 text-red-600">{error}</div>}

      {result && <AssessmentResult data={result} />}
    </div>
  );
}
```

### Results Display Component

```typescript
interface AssessmentResultProps {
  data: AssessmentResponse;
}

function AssessmentResult({ data }: AssessmentResultProps) {
  const getRiskColor = (risk: string) => {
    if (risk.includes('Low')) return 'text-green-600 bg-green-50';
    if (risk.includes('Moderate')) return 'text-yellow-600 bg-yellow-50';
    if (risk.includes('High')) return 'text-red-600 bg-red-50';
    return 'text-gray-600 bg-gray-50';
  };

  return (
    <div className="mt-8 space-y-6">
      {/* Risk Level */}
      <div className={`p-4 rounded-lg ${getRiskColor(data.risk_level)}`}>
        <h2 className="text-2xl font-bold">Risk Level: {data.risk_level}</h2>
        <p>Confidence: {data.confidence}</p>
        <p className="text-sm mt-2">
          Based on {data.papers_analyzed} papers (avg quality: {data.avg_quality_score}/100)
        </p>
      </div>

      {/* Assessment Text */}
      <div className="prose max-w-none">
        <h3>Assessment</h3>
        <div dangerouslySetInnerHTML={{ 
          __html: data.assessment.replace(/\n/g, '<br>') 
        }} />
      </div>

      {/* Sources */}
      <div>
        <h3 className="text-xl font-semibold mb-4">Source Papers</h3>
        <div className="space-y-3">
          {data.sources.map((source, idx) => (
            <div key={idx} className="border rounded p-3 hover:bg-gray-50">
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline"
              >
                {source.title}
              </a>
              <div className="text-sm text-gray-600 mt-1">
                {source.journal} ({source.year}) · Quality: {source.quality_score}/100
                {source.is_clinical_trial && ' · Clinical Trial'}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

## Example Page

Complete example page for your Lovable app:

```typescript
// app/assess/page.tsx
'use client';

import { useState } from 'react';
import { toxicityAPI } from '@/lib/api';
import AssessmentForm from '@/components/AssessmentForm';

export default function AssessPage() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-8">Toxicity Assessment</h1>
      <AssessmentForm />
    </div>
  );
}
```

## Testing

1. Deploy your backend API to Railway or Render
2. Add the API URL to Lovable environment variables
3. Test the assessment flow in your frontend
4. Verify source links work correctly

## Error Handling

Add proper error handling:

```typescript
try {
  const result = await toxicityAPI.assess(request);
  // Handle success
} catch (error) {
  if (error.message.includes('No papers found')) {
    // Suggest loading papers first
  } else if (error.message.includes('network')) {
    // Network error
  } else {
    // Generic error
  }
}
```

## Production Checklist

- API URL configured in environment variables
- Error handling implemented
- Loading states displayed
- Source links open in new tabs
- Mobile-responsive design
- Rate limiting consideration
