# MVP Demo Guide - Step-by-Step

## Overview

This guide walks through demonstrating the NestWell RAG system for toxicity assessment of ingredients during pregnancy and planning phases.

**Target Audience:** Expecting/pregnant parents, postpartum/breastfeeding parents, those planning pregnancy

**Demo Duration:** 10-15 minutes

---

## Pre-Demo Checklist

### Before the Demo:
- [ ] Railway API is deployed and running
- [ ] Lovable website is live
- [ ] Environment variables are set in Lovable
- [ ] Database is preloaded (optional but recommended)
- [ ] Test account ready
- [ ] Browser ready with Lovable site open

### Test Your Setup:
1. Visit Lovable site URL
2. Try searching for "retinol" 
3. Verify you get an assessment
4. Check that sources display

---

## Demo Flow

### 1. Introduction (1 minute)

**What to Say:**
> "Today I'm demonstrating NestWell, a research-based tool that helps expecting and postpartum parents make informed decisions about product ingredients. It uses AI to analyze scientific papers from PubMed."

**Show:** Landing page

---

### 2. Select Your Stage (30 seconds)

**What to Say:**
> "First, you select your life stage - planning pregnancy, currently pregnant, postpartum/breastfeeding, or general family safety. This tailors the research to your specific situation."

**Show:** Life stage selector on the main page

**Demonstration:**
- Click through each stage option
- Explain that different stages require different quality standards

---

### 3. Common Compound Demo: Retinol (2 minutes)

**What to Say:**
> "Let's check retinol, a common skincare ingredient. Retinol is actually a type of vitamin A derivative that can cause birth defects."

**Action:**
1. Enter "retinol" in ingredient field
2. Select "cosmetics" as product type
3. Select "Pregnant" as life stage
4. Click "Check Ingredient"

**Expected Results:**
- Risk Level: **High Risk** (red badge)
- Quality: 70/100 threshold (high-quality clinical evidence)
- Assessment explains teratogenic risk
- Sources show clinical trials

**What to Say:**
> "As you can see, retinol poses a high risk during pregnancy. The system found clinical trials showing it can cause birth defects. Notice it requires high-quality research (70/100 minimum) because this is a high-stakes decision."

**Show:** Sources section with clickable PubMed links

---

### 4. Understanding Quality Scores (1 minute)

**What to Say:**
> "Let's look at the quality scoring. Each research paper gets a score from 0-100 based on four factors: study design (clinical trials score higher), how recent the research is, the quality of the abstract, and journal prestige."

**Show:** Quality scores for sources

**What to Say:**
> "For pregnancy decisions, we require research scoring at least 70/100. For general family safety, we use a lower threshold of 50/100. This ensures you're getting the most reliable information."

---

### 5. Transparency Demo: Limited Evidence (2 minutes)

**What to Say:**
> "Now let's see what happens when there's limited research available."

**Action:**
1. Enter "some new unknown ingredient" 
2. Select any life stage
3. Click "Check Ingredient"

**Expected Results:**
- Either: "Insufficient Data" with explanation
- Or: Warning about low-quality evidence

**What to Say:**
> "See how transparent the system is? It tells you when research is limited, why it's limited, and what you should do next - which is always to consult your healthcare provider."

**Show:** The warning message or insufficient data message

---

### 6. Postpartum/Breastfeeding Context (1.5 minutes)

**What to Say:**
> "Let's see how the same ingredient changes for a breastfeeding parent."

**Action:**
1. Enter "retinol" again
2. Select "Postpartum / Breastfeeding" life stage
3. Click "Check Ingredient"

**Expected Results:**
- Different assessment focused on lactation effects
- Still high quality threshold (70/100)
- Search query modified to include "breastfeeding"

**What to Say:**
> "Notice how the search automatically includes 'breastfeeding effects' in the query. This ensures you get relevant research for your specific situation."

---

### 7. Different Quality Thresholds (1.5 minutes)

**What to Say:**
> "Let's see how the same ingredient is assessed for general family safety with a lower quality threshold."

**Action:**
1. Enter "retinol" 
2. Select "General family safety" life stage
3. Click "Check Ingredient"

**Expected Results:**
- Moderate quality threshold (50/100)
- May accept more observational studies
- Assessment focused on general safety

**What to Say:**
> "For general safety, we use a 50/100 threshold. This is still good quality research, but less stringent than the 70/100 we require for pregnancy decisions."

---

### 8. Sources and Research Papers (1 minute)

**What to Say:**
> "All assessments are backed by published research. Let's look at the sources."

**Show:** Sources section

**What to Say:**
> "Each source is clickable and takes you to PubMed, the largest medical research database. You can see the paper title, journal, year, quality score, and whether it's a clinical trial."

**Action:** Click on a source link to show it opens PubMed

**What to Say:**
> "Some users may have network restrictions that block PubMed. In those cases, users can try the search link or copy the PMID to search manually."

---

### 9. Speed Demonstration (30 seconds)

**What to Say:**
> "The system has been preloaded with research on common compounds like retinol and parabens. This makes responses much faster."

**Action:** Search for "retinol" again quickly

**Expected:** Fast response (since it's in the database)

**What to Say:**
> "See how fast that was? The database already has this research, so you get instant results for the most common ingredient questions."

---

### 10. Key Features Recap (1 minute)

**What to Say:**
> "Let me summarize the key features:"

**Show each feature:**
1. ✅ **Life stage awareness** - Different research for different stages
2. ✅ **Quality thresholds** - 70/100 for high stakes, 50/100 for general
3. ✅ **Transparency** - Always explains limitations
4. ✅ **Source links** - Direct access to research papers
5. ✅ **Fast responses** - Preloaded database
6. ✅ **Medical disclaimers** - Always consult healthcare provider

---

## Q&A Prep

### Common Questions:

**Q: Is this medical advice?**
**A:** "No, this is a research tool. We analyze published papers and present the findings, but users should always consult their healthcare provider for personalized medical advice."

**Q: How accurate is this?**
**A:** "We use peer-reviewed research from PubMed, rate each study for quality, and require clinical trials for high-stakes decisions. We're also transparent about limitations when research is insufficient."

**Q: What if I get 'insufficient data'?**
**A:** "That means the research isn't available or doesn't meet our quality standards. In that case, we recommend consulting your healthcare provider and the product manufacturer's safety data."

**Q: Can I trust this over my doctor?**
**A:** "No. This is supplementary information to help inform discussions with your healthcare provider. Never replace medical advice with this tool."

**Q: What ingredients work best?**
**A:** "The system works best for well-studied ingredients like retinoids, parabens, salicylic acid. For newer or less common ingredients, you may get limited results."

---

## Closing

**Final Words:**
> "NestWell helps expecting and postpartum parents save time by aggregating research in one place. It provides transparency about research quality and encourages users to consult healthcare providers. The goal is to make informed decisions easier."

**Show:** Landing page again

> "Thank you for your time. Are there any questions?"

---

## Technical Backup Plan

If something doesn't work during the demo:

### If Lovable site is down:
- Show the Railway API directly at `http://your-railway.app/docs`
- Use the interactive Swagger UI
- Demonstrate the API endpoints

### If database is empty:
- Explain the preloading feature
- Show that papers load on first search
- Mention the 3-second delay for database persistence

### If API is slow:
- Explain that first-time searches take longer
- Preloaded compounds should be fast
- Real-world usage will have more preloaded data

### If no papers found:
- Show the transparency message
- Explain quality thresholds
- Demonstrate that low-quality papers show warnings

---

## Demo Checklist

Before demo:
- [ ] API running on Railway
- [ ] Lovable site live
- [ ] Database preloaded
- [ ] Test searches work

During demo:
- [ ] Show life stage selector
- [ ] Search retinol + pregnant
- [ ] Explain quality scores
- [ ] Show limited evidence case
- [ ] Compare different life stages
- [ ] Click on source links
- [ ] Recap key features

After demo:
- [ ] Answer questions
- [ ] Offer to show technical details
- [ ] Provide GitHub repo link if interested
- [ ] Get feedback

---

## Success Metrics

**A successful demo should demonstrate:**
✅ Users understand the life stage concept  
✅ Quality thresholds make sense  
✅ Transparency builds trust  
✅ Sources provide credibility  
✅ Speed is impressive  
✅ Medical disclaimers are clear  

---

## Additional Demo Ideas

### For Technical Audiences:
- Show the API documentation (`/docs` endpoint)
- Explain the RAG architecture
- Show ChromaDB database structure
- Demonstrate quality scoring algorithm

### For Business Audiences:
- Emphasize transparency and trust
- Show competitive differentiation
- Discuss user safety and legal protection
- Highlight scalability potential

### For Investors:
- Market opportunity (expecting parents)
- Problem (lack of easy access to research)
- Solution (AI-powered research aggregation)
- Traction (MVP ready, database preloaded)

---

## Summary

**Demo Time:** 10-15 minutes  
**Key Message:** Research-based, transparent, trustworthy tool for informed ingredient decisions  
**Call to Action:** Try it yourself, ask questions, provide feedback  

Good luck with your demo! 🚀
