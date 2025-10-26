# API Key Explanation - Why You Need It

## 🔑 Why the Anthropic API Key is Required

The **Anthropic API key** is needed for the `/assess` endpoint, which uses **Claude AI** to generate intelligent toxicity assessments from the research papers you load.

### What Claude Does:

1. **Reads** all the papers you've loaded about a substance
2. **Analyzes** the findings across multiple studies
3. **Synthesizes** the information
4. **Generates** a human-readable assessment with:
   - Safety rating (Low/Moderate/High Risk)
   - Key findings summary
   - Usage frequency impact
   - Vulnerable populations
   - Confidence level
   - Research limitations

Without Claude, you would just get raw papers without any analysis or interpretation.

---

## 💰 Cost & Getting a Key

### Cost
- Anthropic pricing: **~$0.003 per 1K input tokens, $0.015 per 1K output tokens**
- An average assessment costs about **$0.05-0.10** (very cheap!)
- Example: 100 assessments ≈ $5-10

### How to Get a Key:
1. Go to https://console.anthropic.com/
2. Sign up for free
3. You get **$5 free credit** to start
4. Create an API key
5. Copy it to your `.env` file

### Is It Worth It?
**Yes!** Claude provides:
- ✅ Intelligent analysis of complex research
- ✅ Synthesis of multiple conflicting studies
- ✅ Clear, actionable safety ratings
- ✅ Human-readable reports

Without it, you'd need to manually read and interpret dozens of papers yourself.

---

## 🆓 Free Alternatives

### Option 1: Use OpenAI Instead (Similar Cost)
If you prefer OpenAI, I can modify the code to use ChatGPT API instead. Costs are similar.

### Option 2: Use Free AI Services
You could use:
- **Hugging Face** (free tier available)
- **Google Gemini** (free tier)
- **Local LLMs** (Ollama - completely free)

Trade-off: Lower quality analysis compared to Claude.

### Option 3: Skip AI Assessment
Remove AI entirely and just return paper summaries. You'd get:
- List of relevant papers
- Quality scores
- PubMed links

But no automated analysis or safety ratings.

---

## 🛠️ Recommended Approach

**Start with Anthropic Claude because:**
1. You get $5 free credit (enough for ~100 assessments)
2. Best quality analysis for this use case
3. Very affordable (~$0.05 per assessment)
4. No setup required

**If you hit the free limit:**
- Use alternative AI services
- Or manually review the papers the system finds for you

---

## 📊 What Each Component Costs

| Component | Cost | Free Alternative |
|-----------|------|------------------|
| PubMed Papers | FREE | N/A (government database) |
| ChromaDB | FREE | Built-in vector storage |
| Claude AI | ~$0.05/assessment | Hugging Face, OpenAI, or skip |
| **Total** | **~$0.05 per assessment** | **$0 (manual review)** |

---

## ❓ Bottom Line

**Do you need the API key?**
- **Yes** - if you want AI-powered assessments
- **No** - if you just want to search papers and read them yourself

**My recommendation:**
- Get the free Anthropic account
- Use the $5 free credit (100 assessments)
- Then decide if it's worth the small cost

For a production system, $0.05 per assessment is extremely cheap for the value it provides!

---

## 🚀 Quick Start Without AI

If you want to test the system WITHOUT the API key:

1. Use the `/load-papers` endpoint (no key needed)
2. Use the `/papers` endpoint to see all papers
3. Manually read the papers via PubMed links
4. Skip the `/assess` endpoint that needs AI

This lets you try everything except the AI assessment feature!
