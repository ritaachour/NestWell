# Quality Scoring System

## Overview

Each research paper receives a quality score from **0 to 100** based on four factors that determine scientific rigor and reliability.

---

## Scoring Components (Total: 100 points)

### 1. Study Design (40 points)

**Highest priority - determines research rigor**

| Study Type | Points | Why |
|------------|--------|-----|
| Randomized Controlled Trial (RCT) | 40 | Gold standard - eliminates bias |
| Clinical Trial | 30 | Direct human evidence |
| Systematic Review / Meta-Analysis | 35 | Aggregates multiple studies |
| Observational / Case Study / Other | 20 | Weaker evidence |

**Example:**
- RCT on retinoids → 40 points
- Observational study → 20 points

---

### 2. Recency (20 points)

**Recent research is valued more**

| Year Published | Points | Reason |
|----------------|--------|--------|
| 2020 or newer | 20 | Most current evidence |
| 2015-2019 | 15 | Recent research |
| 2010-2014 | 10 | Moderately current |
| Before 2010 | 5 | Older studies |

**Example:**
- Paper from 2023 → 20 points
- Paper from 2008 → 5 points

---

### 3. Abstract Quality (20 points)

**Length indicates thoroughness**

| Abstract Length | Points | Quality |
|-----------------|--------|---------|
| > 500 characters | 20 | Comprehensive description |
| 200-500 characters | 15 | Adequate information |
| < 200 characters | 10 | Brief/short abstract |

**Why it matters:**
- Longer abstracts contain more detail
- Indicates thorough research reporting
- Better abstracts = better studies typically

---

### 4. Journal Prestige (20 points)

**High-impact journals publish quality research**

### High-Impact Journals (20 points):
- The Lancet
- JAMA (Journal of the American Medical Association)
- BMJ (British Medical Journal)
- Nature
- Science
- Nature Medicine
- New England Journal of Medicine (NEJM)
- Cell
- Toxicology journals

### Other Journals (10 points):
- All other journals get 10 points

**Why it matters:**
- Rigorous peer review
- High editorial standards
- Widely cited research

---

## Complete Scoring Examples

### Example 1: High-Quality Study

**Paper:** RCT on retinoids, published 2022, long abstract, in Lancet

- Study Design: RCT → **40 points**
- Recency: 2022 → **20 points**
- Abstract: 600 chars → **20 points**
- Journal: Lancet → **20 points**

**Total: 100/100** ✅

---

### Example 2: Moderate-Quality Study

**Paper:** Clinical trial on parabens, published 2017, medium abstract, in middle-tier journal

- Study Design: Clinical Trial → **30 points**
- Recency: 2017 → **15 points**
- Abstract: 300 chars → **15 points**
- Journal: Other journal → **10 points**

**Total: 70/100** ✅

---

### Example 3: Lower-Quality Study

**Paper:** Observational study on phthalates, published 2008, short abstract, in low-tier journal

- Study Design: Observational → **20 points**
- Recency: 2008 → **5 points**
- Abstract: 150 chars → **10 points**
- Journal: Other journal → **10 points**

**Total: 45/100** ⚠️

---

## Quality Boundaries

### How Papers are Classified:

| Score Range | Category | Usage |
|-------------|----------|-------|
| 80-100 | Excellent | Prioritized in assessments |
| 60-79 | Good | Included in analysis |
| 40-59 | Fair | Included but weighted less |
| 0-39 | Poor | Excluded by default (can set min score) |

### Default Settings:

**In Lovable, by default:**
- Minimum quality score: **30**
- Maximum papers used: **5**
- Higher quality papers prioritized

**Can be adjusted:**
```typescript
{
  min_quality_score: 50,  // Only papers ≥ 50
  max_papers: 10          // Use more papers
}
```

---

## Why This Matters

### For Your Users:

**High-quality papers (70-100):**
- More trustworthy
- More likely to have correct conclusions
- Include RCTs and meta-analyses

**Lower-quality papers (30-50):**
- May have bias
- Smaller sample sizes
- Weaker evidence

**The system automatically:**
- ✅ Prioritizes high-quality studies
- ✅ Averages quality scores
- ✅ Shows quality score to users
- ✅ Flags clinical trials

---

## Quality Score Display

Users see quality scores in results:

```
Sources:
- "Retinoid safety in pregnancy" (2023)
  Lancet · Quality: 95/100 · Clinical Trial
```

This helps users understand:
- How trustworthy each paper is
- Whether it's a clinical trial (stronger evidence)
- Year published (recency)

---

## Summary

**Quality Score = Evidence Strength**

- **100**: Perfect RCT in top journal
- **70-90**: Strong clinical evidence
- **50-70**: Good observational studies
- **30-50**: Limited evidence
- **<30**: Weak evidence (usually filtered out)

The system ensures users get assessments based on the **strongest available evidence**.
