# Life Stage Implementation in RAG System

## Your Life Stages

Based on your UI, the stages are:
1. **Planning pregnancy**
2. **Pregnant**
3. **Postpartum / Breastfeeding**
4. **General family safety**

---

## How They're Implemented in the Code

### In the API Route (Lovable):

```typescript
if (body.lifeStage === 'pregnant') {
  query += ' pregnancy effects';
} else if (body.lifeStage === 'postpartum') {
  query += ' breastfeeding lactation effects';
} else if (body.lifeStage === 'planning') {
  query += ' fertility reproductive effects';
}
// 'general' gets no addition
```

### In the Frontend (Lovable Page):

The stages should map as:
- `'planning'` → Planning pregnancy
- `'pregnant'` → Pregnant  
- `'postpartum'` → Postpartum / Breastfeeding
- `'general'` → General family safety

---

## How It Works in the RAG System

### Step 1: Query Building

**Input:** "retinol" + "Pregnant" + "Skincare"

**PubMed Query Built:**
```
"retinol cosmetics toxicity pregnancy effects"
```

**What PubMed Returns:**
- Papers specifically about retinol effects during pregnancy
- Fetal development studies
- Teratogenicity research
- Pregnancy-specific safety data

### Step 2: Contextual Retrieval

ChromaDB's semantic search finds papers most relevant to:
- The ingredient (retinol)
- The product type (cosmetics)
- The life stage context (pregnancy effects)

### Step 3: AI Assessment

Google Gemini receives:
- The retrieved papers
- Context: "Usage frequency: daily"
- The substance and product type
- Analysis tailored to the life stage

### Step 4: User Display

Final assessment is prefixed with:
```
"Note: This assessment has been weighted toward evidence specific to during pregnancy."
```

---

## Example Queries by Stage

### Planning Pregnancy:
```
Input: "parabens" + "Planning pregnancy" + "Cosmetics"
Query: "parabens cosmetics toxicity fertility reproductive effects"
Returns: Studies on fertility, reproductive health, conception
```

### Pregnant:
```
Input: "retinol" + "Pregnant" + "Skincare"
Query: "retinol cosmetics toxicity pregnancy effects"
Returns: Teratogenicity, fetal development, pregnancy safety
```

### Postpartum / Breastfeeding:
```
Input: "salicylic acid" + "Postpartum / Breastfeeding" + "Skincare"
Query: "salicylic acid cosmetics toxicity breastfeeding lactation effects"
Returns: Milk transfer, infant exposure, breastfeeding safety
```

### General Family Safety:
```
Input: "BPA" + "General family safety" + "Food"
Query: "BPA food toxicity"
Returns: General population safety data, no specific life stage focus
```

---

## Is It Properly Implemented?

### ✅ What's Working:

1. **Query modification:** Each stage adds relevant terms to PubMed search
2. **Context-aware retrieval:** Papers are pre-filtered by life stage
3. **AI awareness:** Assessment notes include life stage context
4. **User transparency:** Users see what stage influenced the results

### ⚠️ Potential Issues:

1. **Mixed results:** PubMed might return some general papers along with stage-specific ones
2. **Limited research:** Some ingredients may have no pregnancy-specific studies
3. **AI interpretation:** Gemini might not always emphasize the stage context enough

---

## Improving the Implementation

### Option 1: Add Stage to AI Prompt

```typescript
// Make AI more aware of the stage
prompt = f"""You are a toxicology expert specializing in {body.lifeStage}.

Analyze these papers about {body.ingredient} in {body.productType}.

CRITICAL CONTEXT: User is {lifeStageDescription}.

Focus on:
- {stageSpecificRisks}
- Safety specifically for this life stage
- Any stage-specific contraindications
"""
```

### Option 2: Filter Papers by Stage Keywords

After loading papers, filter to keep only papers mentioning:
- Pregnancy stage: "pregnancy", "fetal", "teratogenic", "prenatal"
- Planning stage: "fertility", "conception", "reproductive"
- Postpartum stage: "breastfeeding", "lactation", "milk transfer"

### Option 3: Weight Scores by Relevance

Boost quality scores for papers that specifically mention the life stage.

---

## Current State Assessment

### ✅ Properly Implemented:

- Query terms are stage-specific
- Different stages search different PubMed content
- Users see transparency about stage context
- Assessment notes which stage was prioritized

### ⚠️ Could Be Better:

- No explicit filtering of irrelevant papers (e.g., general studies in pregnancy search)
- AI prompt could be more stage-focused
- No way to ensure ALL retrieved papers are stage-relevant

---

## Recommendations

### Quick Wins:

1. **Make AI prompt more stage-aware** (see Option 1)
2. **Add stage description to assessment** (already done ✅)
3. **Note in UI** which papers are stage-specific

### Better Implementation:

1. **Post-load filtering:** After loading, filter papers by stage keywords
2. **Boost stage-specific papers:** Increase quality scores for relevant papers
3. **Show stage-specific count:** "5 papers, 3 specific to pregnancy"

---

## Testing Each Stage

### Test with Same Ingredient, Different Stages:

**Ingredient:** Retinol
**Product:** Cosmetics

| Stage | Expected Papers | What to Look For |
|-------|----------------|------------------|
| Planning | Fertility studies, conception safety | "Does retinol affect conception?" |
| Pregnant | Teratogenicity, fetal development | "Is retinol safe during pregnancy?" |
| Postpartum | Breast milk transfer, infant exposure | "Can you use retinol while breastfeeding?" |
| General | Overall toxicity, general population | "Is retinol generally safe?" |

**Expected behavior:** Each stage should return different papers with different safety conclusions.

---

## Summary

**Current Status: ✅ Partially Implemented**

- ✅ Stages modify PubMed query
- ✅ Different papers retrieved per stage
- ⚠️ Could use better filtering
- ⚠️ AI could be more stage-aware
- ⚠️ No explicit verification of stage-relevant papers

**Overall:** The system recognizes different stages and searches appropriately, but could do more to ensure 100% stage-relevant results.
