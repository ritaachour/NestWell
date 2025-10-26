// app/api/check-ingredient/route.ts

import { NextResponse } from 'next/server';

// Remove trailing slash to prevent double slash issue
const API_URL = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, '') || 'http://localhost:8000';

// Quality thresholds based on stakes
const QUALITY_THRESHOLDS = {
  high: 70,       // Pregnancy, breastfeeding - need highest quality
  moderate: 50,   // General family safety
  low: 30         // Informational only (though this is below min possible)
};

export async function POST(request: Request) {
  try {
    const body = await request.json();
    
    // Build context-aware query based on life stage
    let query = `${body.ingredient} ${body.productType} toxicity`;
    let qualityThreshold = QUALITY_THRESHOLDS.moderate; // Default
    let stageContext = '';
    
    if (body.lifeStage === 'pregnant') {
      query += ' pregnancy effects';
      qualityThreshold = QUALITY_THRESHOLDS.high; // High stakes for pregnancy
      stageContext = 'during pregnancy';
    } else if (body.lifeStage === 'postpartum') {
      query += ' breastfeeding lactation effects';
      qualityThreshold = QUALITY_THRESHOLDS.high; // High stakes for breastfeeding
      stageContext = 'while breastfeeding';
    } else if (body.lifeStage === 'planning') {
      query += ' fertility reproductive effects';
      qualityThreshold = QUALITY_THRESHOLDS.high; // High stakes for fertility
      stageContext = 'when planning a pregnancy';
    } else if (body.lifeStage === 'general') {
      qualityThreshold = QUALITY_THRESHOLDS.moderate;
      stageContext = 'general family safety';
    }
    
    console.log('API Call - Loading papers for:', query);
    console.log('Quality threshold:', qualityThreshold);
    
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

    // Step 3: Try to get assessment with appropriate quality threshold
    console.log(`Getting assessment with quality threshold ${qualityThreshold}...`);
    const assessmentResponse = await fetch(`${API_URL}/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        substance: body.ingredient,
        product_type: body.productType,
        usage_frequency: 'daily',
        min_quality_score: qualityThreshold, // Use stage-appropriate threshold
        max_papers: 5
      })
    });

    // If assessment fails due to quality threshold, try with lower threshold to see what we have
    if (!assessmentResponse.ok) {
      console.log(`High quality threshold (${qualityThreshold}) failed, trying lower threshold...`);
      
      // Try with lower threshold to see what we have
      const lowerQualityResponse = await fetch(`${API_URL}/assess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          substance: body.ingredient,
          product_type: body.productType,
          usage_frequency: 'daily',
          min_quality_score: 0, // Accept all papers to see what's available
          max_papers: 10
        })
      });

      if (!lowerQualityResponse.ok) {
        // Even with no threshold, nothing found
        return NextResponse.json({
          risk_level: "Unable to Assess",
          confidence: "None",
          assessment: `## Unable to Generate Assessment\n\nWe found ${loadData.papers_loaded} research papers, but encountered an issue analyzing them.\n\n### What We Found:\n- ${loadData.papers_loaded} paper(s) loaded from PubMed\n- Average quality score: ${loadData.average_quality_score.toFixed(1)}/100\n- Clinical trials: ${loadData.clinical_trial_count}\n- Minimum quality required: ${qualityThreshold}/100\n\n### Why We Can't Provide a Reliable Assessment:\n- Papers do not meet our minimum quality standards for ${body.lifeStage === 'general' ? 'general safety' : stageContext}\n- Low average quality (${loadData.average_quality_score.toFixed(1)}/100) indicates weak evidence\n- Insufficient high-quality studies for ${body.ingredient} in ${body.productType}\n\n### What This Means:\nLimited or low-quality research makes it impossible to provide a reliable safety assessment.\n\n### Recommendation:\n**Consult your healthcare provider** for personalized advice based on your specific situation and the latest medical guidance.`,
          sources: [],
          papers_analyzed: loadData.papers_loaded,
          avg_quality_score: loadData.average_quality_score,
          transparency_note: `Found ${loadData.papers_loaded} papers, but none met quality standards (≥${qualityThreshold}/100). Average quality: ${loadData.average_quality_score.toFixed(1)}/100.`
        });
      }

      // We have papers but they're low quality for this stage
      const lowerQualityData = await lowerQualityResponse.json();
      const avgQuality = loadData.average_quality_score;

      return NextResponse.json({
        ...lowerQualityData,
        transparency_note: `⚠️ Quality Warning: The available research has an average quality score of ${avgQuality.toFixed(1)}/100, which is below our minimum standard of ${qualityThreshold}/100 for ${body.lifeStage === 'general' ? 'general safety' : stageContext}. Results should be interpreted with caution.`,
        quality_warning: true,
        assessment: `## ⚠️ Limited Evidence Available\n\n### Assessment Based on Lower Quality Studies\n\n${lowerQualityData.assessment}\n\n### Quality Breakdown:\n- **Papers found**: ${loadData.papers_loaded}\n- **Average quality score**: ${avgQuality.toFixed(1)}/100 (below our ${qualityThreshold}/100 minimum)\n- **Clinical trials**: ${loadData.clinical_trial_count}\n- **Quality standard for ${stageContext || 'general use'}**: ≥${qualityThreshold}/100\n\n### Why This Matters:\nStudies with quality scores below ${qualityThreshold} may have:\n- Small sample sizes\n- Lack of proper controls\n- Observational rather than experimental design\n- Incomplete reporting\n- Potential for bias\n\n### Our Recommendation:\nDue to the low quality of available evidence:\n1. **Do NOT rely solely on this assessment**\n2. **Consult your healthcare provider** for personalized advice\n3. **Consider alternative products** with better evidence\n4. **Erring on the side of caution** ${body.lifeStage === 'general' ? 'especially for vulnerable populations' : `during ${stageContext}`}\n\n### Transparency:\nWe're showing you what the research says, even though it doesn't meet our quality standards, so you have all available information to make an informed decision.`,
      });
    }

    // Success! We have high-quality papers
    const data = await assessmentResponse.json();
    
    // Add life stage context to assessment
    if (data.assessment && stageContext) {
      data.assessment = `${data.assessment}\n\n**Note:** This assessment has been weighted toward evidence specific to ${stageContext}. The analysis prioritized research studies that examine safety in this specific context.`;
    }

    // Add quality info for transparency
    const qualityStandards = {
      70: 'high-quality clinical evidence',
      50: 'moderate-quality evidence',
      30: 'basic quality standards'
    };
    
    data.transparency_note = `✅ ${qualityStandards[qualityThreshold]} assessment based on ${data.papers_analyzed} paper(s) with an average quality score of ${data.avg_quality_score}/100 (minimum threshold: ${qualityThreshold}/100).`;
    
    return NextResponse.json(data);
    
  } catch (error: any) {
    console.error('API Error:', error);
    return NextResponse.json(
      { error: 'Unable to check ingredient. Please try again.' },
      { status: 500 }
    );
  }
}
