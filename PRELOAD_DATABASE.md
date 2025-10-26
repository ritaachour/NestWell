# Preloading Database with Toxic Compounds

## Purpose

Preload the ChromaDB database with research papers on common toxic compounds for pregnant women and those planning pregnancy. This makes API responses **much faster** because papers are already in the database.

---

## Compounds Being Loaded

### For Pregnant Women (5 compounds):
1. **Retinoids** (retinol, retinyl palmitate) - High teratogenic risk
2. **Salicylic Acid** - Anti-inflammatory, risk of birth defects
3. **Hydroquinone** - Skin lightening, teratogenic effects
4. **Formaldehyde** - Carcinogen and reproductive toxin
5. **Parabens** - Potential endocrine disruptors

### For Women Planning Pregnancy (2 compounds):
1. **Glycolic Acid** - Fertility and reproductive health effects
2. **Benzoyl Peroxide** - Reproductive hormone considerations

---

## How to Run

### Step 1: Activate Virtual Environment

```bash
source venv/bin/activate
```

### Step 2: Run Preload Script

```bash
python preload_database.py
```

### Step 3: Wait for Completion

The script will:
- Query PubMed for each compound
- Download abstracts and metadata
- Calculate quality scores
- Store papers in ChromaDB
- Show progress for each compound

Expected time: **5-10 minutes** (depends on PubMed API rate limits)

---

## Expected Output

```
============================================================
DATABASE PRELOADING SCRIPT
Loading toxic compound research papers
============================================================

============================================================
LOADING PREGNANCY-RELATED COMPOUNDS
============================================================

============================================================
Loading papers for: retinoids
Description: Retinoids (vitamin A derivatives) - high risk during pregnancy
Query: retinoids retinyl palmitate retinol pregnancy teratogenic birth defects
============================================================

✅ Added paper 12345678: Retinoid exposure during pregnancy and risk of birth defects...
   Quality score: 85/100

✅ Successfully added 15 papers for retinoids

...

============================================================
PRELOADING SUMMARY
============================================================
Total papers added: 95
Compounds loaded: 7
============================================================

Total papers in database: 95

✅ Preloading complete!

The database is now ready to serve faster responses for:
  - retinoids (pregnancy)
  - salicylic_acid (pregnancy)
  - hydroquinone (pregnancy)
  - formaldehyde (pregnancy)
  - parabens (pregnancy)
  - glycolic_acid (planning)
  - benzoyl_peroxide (planning)
```

---

## What This Does

### Benefits:
✅ **Faster Responses** - Papers already in database, no waiting for PubMed  
✅ **More Reliability** - Papers loaded upfront, less dependent on API  
✅ **Better Coverage** - 95+ papers on critical compounds  
✅ **Quality Scored** - All papers rated for research quality  

### Papers Loaded:
- **~75 papers** for pregnancy compounds (15 per compound × 5)
- **~20 papers** for planning compounds (10 per compound × 2)
- **Total: ~95 papers**

---

## Verification

After running, check the database:

```bash
# Start your API
uvicorn main:app --reload

# In another terminal, check papers
curl http://localhost:8000/papers | python -m json.tool | head -50
```

You should see papers for retinoids, salicylic acid, hydroquinone, formaldehyde, parabens, glycolic acid, and benzoyl peroxide.

---

## Testing

Test with a compound that was preloaded:

```bash
# Example: Check retinoids
curl -X POST "http://localhost:8000/load-papers" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "retinol retinyl palmitate",
    "max_results": 5
  }'

# Should respond quickly since papers are already in database
```

Then test the assess endpoint:

```bash
curl -X POST "http://localhost:8000/assess" \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "retinol",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 30
  }'
```

---

## Adding More Compounds

To add more compounds, edit `preload_database.py`:

```python
PREGNANCY_COMPOUNDS = {
    "retinoids": {
        "query": "retinoids retinyl palmitate retinol pregnancy teratogenic birth defects",
        "max_results": 15,
        "description": "Retinoids (vitamin A derivatives) - high risk during pregnancy"
    },
    "NEW_COMPOUND": {
        "query": "your search query here",
        "max_results": 15,
        "description": "Description here"
    }
}
```

Then re-run the script.

---

## Troubleshooting

### Issue: "No papers found"

**Cause:** PubMed API rate limiting or query too specific

**Solution:** Wait a few minutes and try again, or simplify the query

### Issue: "Already exists, skipping"

**Good!** This means the paper is already in your database from a previous run.

### Issue: Script hangs on one compound

**Cause:** PubMed API slow or unresponsive

**Solution:** Press Ctrl+C, wait a minute, then re-run. The script will skip already-loaded papers.

---

## Database Location

Papers are stored in: `chroma_db/`

This directory is in `.gitignore` so it won't be committed to Git.

---

## Summary

**Run:** `python preload_database.py`

**Result:** ~95 papers on 7 critical toxic compounds preloaded

**Benefit:** Much faster API responses for common ingredient queries

**Time:** ~5-10 minutes

🚀 **Your database is now ready for production use!**
