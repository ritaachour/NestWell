# System Flow: How NestWell Works

## Complete User Journey

### Step 1: User Input

User enters:
- **Ingredient:** e.g., "retinol"
- **Life Stage:** e.g., "Pregnant"
- **Product Type:** e.g., "Skincare & Cosmetics"

### Step 2: Life Stage Context Applied

The system modifies the search query based on life stage:

| Life Stage | Query Addition |
|------------|----------------|
| Planning pregnancy | `+ fertility reproductive effects` |
| Pregnant | `+ pregnancy effects` |
| Postpartum / Breastfeeding | `+ breastfeeding lactation effects` |
| General family safety | No addition |

**Example for "retinol" + "Pregnant":**
```
Original: "retinol cosmetics toxicity"
Modified: "retinol cosmetics toxicity pregnancy effects"
```

This ensures PubMed returns relevant pregnancy-specific research.

---

## Backend Processing Flow

### Phase 1: Load Research Papers

**API Call:** `POST /load-papers`

**Request:**
```json
{
  "query": "retinol cosmetics toxicity pregnancy effects",
  "max_results": 15
}
```

**What Happens:**
1. ✅ Query PubMed database via Bio.Entrez
2. ✅ Fetch paper metadata (title, abstract, journal, year)
3. ✅ Calculate quality score (study design, recency, journal prestige)
4. ✅ Store in ChromaDB vector database
5. ✅ **Wait 3 seconds** for ChromaDB to persist to disk

**Response:**
```json
{
  "papers_loaded": 12,
  "average_quality_score": 68.5,
  "clinical_trial_count": 3,
  "message": "Papers loaded successfully"
}
```

### Phase 2: Generate Assessment

**API Call:** `POST /assess`

**Request:**
```json
{
  "substance": "retinol",
  "product_type": "cosmetics",
  "usage_frequency": "daily",
  "min_quality_score": 30,
  "max_papers": 5
}
```

**What Happens:**
1. ✅ Query ChromaDB for relevant papers (semantic search)
2. ✅ Filter by quality score (≥ 30 in this case)
3. ✅ Retrieve top 5 most relevant papers
4. ✅ Pass papers to Google Gemini AI
5. ✅ AI generates toxicity assessment
6. ✅ Return structured response

**Response:**
```json
{
  "risk_level": "High Risk",
  "confidence": "High",
  "assessment": "Based on clinical research, retinol use during pregnancy...",
  "sources": [
    {
      "pmid": "12345678",
      "title": "Retinoid use in pregnancy and birth defects...",
      "journal": "Reproductive Toxicology",
      "year": "2022",
      "quality_score": 85,
      "is_clinical_trial": true,
      "url": "https://pubmed.ncbi.nlm.nih.gov/12345678"
    }
  ],
  "papers_analyzed": 5,
  "avg_quality_score": 72.0
}
```

---

## RAG System Architecture

```
User Input (retinol + pregnant)
    ↓
Life Stage Context Applied
    ↓
Query PubMed API
    ↓
Fetch Papers + Quality Scoring
    ↓
Store in ChromaDB Vector Database
    ↓
Wait for Persistence (3 sec)
    ↓
Semantic Search in ChromaDB
    ↓
Retrieve Top Papers
    ↓
Generate AI Assessment (Google Gemini)
    ↓
Return Structured Response
    ↓
User Sees Results
```

---

## Key Components

### 1. Context-Aware Query Building

The system modifies PubMed searches based on life stage to ensure relevant research.

**Example:**
- Input: "parabens" + "Planning pregnancy"
- Search: "parabens cosmetics toxicity fertility reproductive effects"

### 2. Quality Scoring System

Each paper receives a score (0-100) based on:
- **Study Design** (40 points): RCT, clinical trial, observational
- **Recency** (20 points): Recent papers score higher
- **Abstract Quality** (20 points): Comprehensive abstracts preferred
- **Journal Prestige** (20 points): High-impact journals score higher

### 3. Semantic Search

ChromaDB uses embeddings to find papers semantically similar to the query, not just keyword matches.

### 4. AI Assessment

Google Gemini analyzes the retrieved papers and generates:
- Risk level (Low/Moderate/High/Insufficient Data)
- Key findings
- Usage frequency impact
- Confidence level

---

## Tools Called in Order

1. **Bio.Entrez** → Query PubMed database
2. **XML Parser** → Extract paper metadata
3. **Quality Scorer** → Rate each paper
4. **ChromaDB** → Store papers as embeddings
5. **ChromaDB Query** → Semantic search for relevant papers
6. **Google Gemini** → Generate AI assessment
7. **Parser** → Extract risk level and confidence

---

## Why This Order Matters

### Correct Order:
1. Load papers first (get the data)
2. Wait for persistence (save to disk)
3. Query database (search the data)
4. Generate assessment (analyze the data)

### Wrong Order Would:
- Try to assess before papers are loaded → Error
- Query before data is saved → Not found
- Skip quality scoring → Lower quality results

---

## Example: Complete Flow for "Retinol" + "Pregnant"

```
User clicks "Check Safety"
    ↓
Inputs: retinol, Pregnant, Skincare & Cosmetics
    ↓
Lovable builds query: "retinol cosmetics toxicity pregnancy effects"
    ↓
Calls Railway API: POST /load-papers
    ↓
PubMed returns 15 papers about retinol + pregnancy
    ↓
Papers scored: avg quality 68.5, 3 clinical trials
    ↓
Papers stored in ChromaDB
    ↓
⏱️ Wait 3 seconds (ChromaDB persistence)
    ↓
Query ChromaDB for most relevant papers
    ↓
Top 5 papers retrieved
    ↓
Google Gemini analyzes papers
    ↓
Generates: "High Risk - Retinoids are teratogenic..."
    ↓
Response with sources sent to Lovable
    ↓
User sees: Risk Level HIGH with explanation
    ↓
User can click to read the 5 source papers
```

---

## Benefits of This Approach

✅ **Context-Aware** - Results tailored to life stage
✅ **Evidence-Based** - All sources from peer-reviewed research
✅ **Quality-Filtered** - Only high-quality studies
✅ **Transparent** - Users can read original papers
✅ **Fast** - 30-60 seconds total (acceptable for research)

---

This is your complete RAG (Retrieval-Augmented Generation) system! 🚀
