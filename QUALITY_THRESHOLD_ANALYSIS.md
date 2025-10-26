# Quality Threshold Analysis

## Current System

**Maximum Score:** 100 points  
**Current Threshold:** 30 points (30%)

### Scoring Breakdown:
- Study Design: 40 points (40%)
- Recency: 20 points (20%)
- Abstract Quality: 20 points (20%)
- Journal Prestige: 20 points (20%)

---

## Is 30/100 the Right Threshold?

### Analysis of Minimum Scores

#### Worst Possible Paper (0-29):
- Study Design: Observational (20 points)
- Recency: Pre-2010 (5 points)
- Abstract: Short <200 chars (10 points)
- Journal: Low-tier (10 points)
- **Total: 45/100 minimum possible score**

Wait, this is a problem! Even the worst papers score 45/100, so threshold of 30 would accept everything.

**Actually, let me recalculate...**

Looking at the code:
- Minimum in each category:
  - Study Design: 20 (observational)
  - Recency: 5 (old papers)
  - Abstract: 10 (short abstract)
  - Journal: 10 (low-tier)
- **Total minimum: 45/100**

So threshold of 30 doesn't make sense. You'd accept papers that could score as low as 45, but 30 is impossible to achieve.

---

## The Real Minimum Scores

Let's calculate actual minimums:

### Scenario 1: Worst Possible Paper
- Observational study (20)
- Pre-2010 paper (5)
- Short abstract <200 chars (10)
- Low-tier journal (10)
- **Total: 45/100**

### Scenario 2: Typical Low-Quality Paper
- Observational study (20)
- 2015-2019 paper (15)
- Medium abstract 200-500 chars (15)
- Low-tier journal (10)
- **Total: 60/100**

### Scenario 3: Decent Quality Paper
- Clinical trial (30)
- 2020-2024 paper (20)
- Long abstract >500 chars (20)
- Low-tier journal (10)
- **Total: 80/100**

---

## Recommended Threshold

### Option 1: Minimum Possible (45/100)
- Accepts everything, even lowest quality
- ❌ Too low, includes unreliable studies

### Option 2: Current (30/100)
- **Doesn't make sense** - impossible to achieve below 45
- Would accept nothing (or everything if code has bug)

### Option 3: Moderate Quality (50-60/100)
- Minimum: 50/100
- Accepts studies with at least some quality
- ✅ Reasonable for an MVP
- Example: Observational + recent + decent abstract

### Option 4: High Quality (70-80/100)
- Minimum: 70/100
- Only clinical trials and recent papers
- ✅ Very reliable for pregnancy recommendations
- Example: Clinical trial + recent + good abstract

### Option 5: Evidence-Based Medical Standard
- Use established systems like GRADE
- RCTs only for medical recommendations
- Minimum quality threshold based on systematic review standards
- ✅ Industry standard
- Example: Only systematic reviews and RCTs

---

## Recommendation

### For Pregnancy/Toxicity Assessment (High Stakes):

**Use 70/100 as minimum threshold**

**Why?**
1. Pregnancy decisions need highest quality evidence
2. 70+ ensures clinical trials, recent papers, good reporting
3. Filters out weak observational studies
4. Still allows papers that aren't perfect (might not be in top journals)

**What 70+ typically means:**
- Clinical trial (30) + Recent paper (20) + Long abstract (20) + Any journal (10+) = **80+**
- OR Systematic review (35) + Recent (15) + Good abstract (15) + Any journal (10+) = **75+**
- OR Observational (20) + Recent (20) + Long abstract (20) + Top journal (20) = **80**

### For General Family Safety (Moderate Stakes):

**Use 50/100 as minimum threshold**

**What this means:**
- Accepts decent observational studies
- Recent papers preferred
- Some quality control
- More papers available for assessment

---

## Evidence Hierarchy

Medical evidence quality (from best to worst):

1. **Systematic Reviews / Meta-Analyses** (35 points in your system)
2. **Randomized Controlled Trials** (40 points)
3. **Clinical Trials** (30 points)
4. **Observational Studies** (20 points)
5. **Case Reports / Anecdotal** (would be 20 or lower)

For safety assessments, you typically want at least #3 (Clinical Trials) or higher.

---

## Proposed Changes

### Update Thresholds:

```python
# In your API route or settings
QUALITY_THRESHOLDS = {
    'high_stakes': 70,      # Pregnancy, breastfeeding
    'moderate_stakes': 50,  # General safety
    'low_stakes': 30        # Informational only
}
```

### For Your Use Case (Pregnancy Safety):

**Recommended: 70/100**

This ensures:
- Clinical trials or better
- Recent evidence (2015+)
- Well-reported studies
- Some degree of peer review quality

---

## Alternative: Use Study Type Filtering

Instead of arbitrary numbers, filter by study type:

```python
MINIMUM_STUDY_TYPES = {
    'pregnancy': ['Randomized Controlled Trial', 'Clinical Trial', 'Systematic Review'],
    'general': ['Clinical Trial', 'Observational Study']
}
```

This is more transparent to users: "Based on X clinical trials..."

---

## Current Issue with Your System

**The 30/100 threshold is meaningless because:**
1. Minimum possible score is 45/100
2. So 30 accepts nothing (impossible to score that low)
3. Or your code has a bug

**Please verify:**
```python
# Test minimum score
min_score = 20 + 5 + 10 + 10  # = 45
print(f"Minimum possible score: {min_score}/100")
```

Your threshold of 30 is below the minimum possible!

---

## Recommendation Summary

### Immediate Fix:
Change threshold from 30 to either:
- **70** for high-stakes decisions (recommended for pregnancy)
- **50** for general use

### Long-term Improvement:
Implement different thresholds per use case:
- Planning pregnancy: 70
- General family safety: 50
- Informational: 30 (but note it will get everything)

**My strong recommendation: Use 70/100 for pregnancy-related queries.**
