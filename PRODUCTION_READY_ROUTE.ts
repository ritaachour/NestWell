// app/api/check-ingredient/route.ts

import { NextResponse } from 'next/server';

// Remove trailing slash to prevent double slash issue
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

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
    
    console.log('API Call - Loading papers for:', query);
    
    // Step 1: Load papers
    const loadResponse = await fetch(`${API_URL}/load-papers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: query,
        max_results: 15
      })
    });

    if (!loadResponse.ok) {
      const errorText = await loadResponse.text();
      console.error('Failed to load papers:', errorText);
      throw new Error(`Failed to load research papers: ${errorText}`);
    }

    const loadData = await loadResponse.json();
    console.log('Papers loaded:', loadData.papers_loaded);

    // Check if any papers were found
    if (loadData.papers_loaded === 0) {
      return NextResponse.json({
        risk_level: "Insufficient Data",
        confidence: "None",
        assessment: `## No Research Available\n\nWe couldn't find any published research papers about ${body.ingredient} in ${body.productType}.\n\n### What This Means:\n- No peer-reviewed studies were found in PubMed database\n- This ingredient may be: poorly studied, newly used, or search terms too specific\n- **Recommendation**: Consult with your healthcare provider for personalized advice\n\n### How to Proceed:\n1. Speak with your doctor or dermatologist\n2. Check product manufacturer's safety data\n3. Consider alternatives with more research available`,
        sources: [],
        papers_analyzed: 0,
        avg_quality_score: 0,
        transparency_note: "No research papers found to analyze."
      });
    }

    // Step 2: CRITICAL - Wait for ChromaDB to persist
    console.log('Waiting for database persistence...');
    await new Promise(resolve => setTimeout(resolve, 3000)); // 3 seconds

    // Step 3: Try to get assessment with normal quality threshold
    console.log('Getting assessment with quality threshold 30...');
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: 'daily',
        min_quality_score: 30, // Keep high quality standard
        max_papers: 5
      })
    });

    // If assessment fails due to quality threshold, get what's available
    if (!assessmentResponse.ok) {
      console.log('High quality threshold failed, trying lower threshold...');
      
      // Try with lower threshold to see what we have
      const lowerQualityResponse = await fetch(`${API_URL}/assess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          substance: body.ingredient,
          product_type: body.productType,
          usage_frequency: 'daily',
          min_quality_score: 0, // Accept all papers
          max_papers: 10
        })
      });

      if (!lowerQualityResponse.ok) {
        // Even with no threshold, nothing found
        return NextResponse.json({
          risk_level: "Unable to Assess",
          confidence: "None",
          assessment: `## Unable to Generate Assessment\n\nWe found ${loadData.papers_loaded} research papers, but encountered an issue analyzing them.\n\n### What We Found:\n- ${loadData.papers_loaded} paper(s) loaded from PubMed\n- Average quality score: ${loadData.average_quality_score.toFixed(1)}/100\n- Clinical trials: ${loadData.clinical_trial_count}\n\n### Why We Can't Provide a Reliable Assessment:\n- Papers may not meet our minimum quality standards (≥30/100)\n- Low average quality (${loadData.average_quality_score.toFixed(1)}/100) indicates weak evidence\n- Insufficient high-quality studies for ${body.ingredient} in ${body.productType}\n\n### What This Means:\nLimited or low-quality research makes it impossible to provide a reliable safety assessment.\n\n### Recommendation:\n**Consult your healthcare provider** for personalized advice based on your specific situation and the latest medical guidance.`,
          sources: [],
          papers_analyzed: loadData.papers_loaded,
          avg_quality_score: loadData.average_quality_score,
          transparency_note: `Found ${loadData.papers_loaded} papers, but none met quality standards (≥30/100). Average quality: ${loadData.average_quality_score.toFixed(1)}/100.`
        });
      }

      // We have papers but they're low quality
      const lowerQualityData = await lowerQualityResponse.json();
      const avgQuality = loadData.average_quality_score;

      return NextResponse.json({
        ...lowerQualityData,
        transparency_note: `⚠️ Quality Warning: The available research has an average quality score of ${avgQuality.toFixed(1)}/100, which is below our minimum standard of 30/100. Results should be interpreted with caution.`,
        quality_warning: true,
        assessment: `## ⚠️ Limited Evidence Available\n\n### Assessment Based on Lower Quality Studies\n\n${lowerQualityData.assessment}\n\n### Quality Breakdown:\n- **Papers found**: ${loadData.papers_loaded}\n- **Average quality score**: ${avgQuality.toFixed(1)}/100 (below our 30/100 minimum)\n- **Clinical trials**: ${loadData.clinical_trial_count}\n\n### Why This Matters:\nStudies with quality scores below 30 may have:\n- Small sample sizes\n- Lack of proper controls\n- Observational rather than experimental design\n- Incomplete reporting\n- Potential for bias\n\n### Our Recommendation:\nDue to the low quality of available evidence:\n1. **Do NOT rely solely on this assessment**\n2. **Consult your healthcare provider** for personalized advice\n3. **Consider alternative products** with better evidence\n4. **Erring on the side of caution** during pregnancy, breastfeeding, or when planning conception\n\n### Transparency:\nWe're showing you what the research says, even though it doesn't meet our quality standards, so you have all available information to make an informed decision.`,
      });
    }

    // Success! We have high-quality papers
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

    // Add quality info for transparency
    data.transparency_note = `✅ High-quality assessment based on ${data.papers_analyzed} paper(s) with an average quality score of ${data.avg_quality_score}/100.`;
    
    return NextResponse.json(data);
    
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Unable to check ingredient. Please try again.' },
      { status: 500 }
    );
  }
}
