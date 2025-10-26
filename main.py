import os
from typing import List, Optional, Dict, Any
from datetime import datetime
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
import time

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import chromadb
from chromadb.config import Settings
from Bio import Entrez

# Load environment variables
load_dotenv()

# Try to import Google Gemini (optional - falls back to basic assessment)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except Exception:
    GEMINI_AVAILABLE = False
    print("Google Gemini not available - will use basic assessment mode")

Entrez.email = os.getenv("NCBI_EMAIL", "user@example.com")

# Initialize FastAPI app
app = FastAPI(
    title="Toxicity Assessment RAG System",
    description="RAG system for toxicity assessment using PubMed papers",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB
chroma_client = chromadb.PersistentClient(
    path="./chroma_db",
    settings=Settings(anonymized_telemetry=False)
)

# Get or create collection
try:
    collection = chroma_client.get_collection(name="toxicity_papers")
except:
    collection = chroma_client.create_collection(
        name="toxicity_papers",
        metadata={"hnsw:space": "cosine"}
    )

# Pydantic models
class LoadPapersRequest(BaseModel):
    query: str = Field(..., description="PubMed search query")
    max_results: int = Field(20, ge=1, le=100, description="Maximum number of papers to fetch")

class LoadPapersResponse(BaseModel):
    papers_loaded: int
    average_quality_score: float
    clinical_trial_count: int
    message: str

class AssessmentRequest(BaseModel):
    substance: str = Field(..., description="Name of the substance")
    product_type: str = Field(..., description="Type of product (food, cosmetics, cleaning)")
    usage_frequency: str = Field(..., description="How often used (daily, weekly, etc.)")
    min_quality_score: int = Field(50, ge=0, le=100, description="Minimum quality score for papers")
    max_papers: int = Field(5, ge=1, le=20, description="Maximum number of papers to use")

class AssessmentResponse(BaseModel):
    risk_level: str
    confidence: str
    assessment: str
    sources: List[Dict[str, Any]]
    papers_analyzed: int
    avg_quality_score: float

class DatabaseStats(BaseModel):
    total_papers: int
    average_quality_score: float
    clinical_trial_count: int
    quality_distribution: Dict[str, int]

# Helper functions
def generate_basic_assessment(request: AssessmentRequest, metadatas: List[Dict]) -> str:
    """Generate basic assessment when AI is not available"""
    # Count clinical trials
    clinical_count = sum(1 for m in metadatas if m.get('is_clinical_trial', False))
    avg_quality = sum(m['quality_score'] for m in metadatas) / len(metadatas)
    
    # Determine risk based on quality and study types
    if avg_quality >= 70 and clinical_count > 0:
        risk = "Low Risk"
        confidence = "High"
    elif avg_quality >= 50:
        risk = "Moderate Risk"
        confidence = "Moderate"
    else:
        risk = "Insufficient Data"
        confidence = "Low"
    
    assessment = f"""## Safety Rating: {risk}

Based on analysis of {len(metadatas)} research papers with an average quality score of {avg_quality:.1f}/100.

### Key Findings:
- {clinical_count} clinical trial(s) included in analysis
- {'High-quality evidence' if avg_quality >= 60 else 'Mixed evidence'} based on available studies
- Further research may be needed to confirm findings

### Usage Frequency Impact:
{request.usage_frequency.capitalize()} usage of {request.substance} in {request.product_type} should be considered in context of overall exposure.

### Confidence Level: {confidence}

**Note:** This is a basic automated assessment. For detailed analysis, please review the source papers listed below."""

    return assessment

def is_high_impact_journal(journal: str) -> bool:
    """Check if journal is high-impact"""
    high_impact = [
        "lancet", "jama", "bmj", "nature", "science", "toxicology",
        "new england journal of medicine", "nejm", "cell", "nature medicine"
    ]
    journal_lower = journal.lower()
    return any(impact in journal_lower for impact in high_impact)

def calculate_quality_score(paper: Dict[str, Any]) -> int:
    """Calculate quality score 0-100 for a paper"""
    score = 0
    
    # Study Design (40 points)
    pub_types = paper.get("pub_types", [])
    if any("Randomized Controlled Trial" in pt for pt in pub_types):
        score += 40
    elif any("Clinical Trial" in pt for pt in pub_types):
        score += 30
    elif any("Systematic Review" in pt or "Meta-Analysis" in pt for pt in pub_types):
        score += 35
    else:
        score += 20
    
    # Recency (20 points)
    year = paper.get("year", "")
    if year:
        try:
            year_int = int(year)
            if year_int >= 2020:
                score += 20
            elif year_int >= 2015:
                score += 15
            elif year_int >= 2010:
                score += 10
            else:
                score += 5
        except:
            score += 5
    else:
        score += 5
    
    # Abstract Quality (20 points)
    abstract_length = len(paper.get("abstract", ""))
    if abstract_length > 500:
        score += 20
    elif abstract_length >= 200:
        score += 15
    else:
        score += 10
    
    # Journal Prestige (20 points)
    journal = paper.get("journal", "")
    if journal and is_high_impact_journal(journal):
        score += 20
    else:
        score += 10
    
    return min(score, 100)

def fetch_pubmed_papers(query: str, max_results: int) -> List[Dict[str, Any]]:
    """Fetch papers from PubMed"""
    try:
        # Search PubMed
        search_handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, sort="relevance")
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        pmids = search_results["IdList"]
        if not pmids:
            return []
        
        # Fetch detailed records
        fetch_handle = Entrez.efetch(db="pubmed", id=pmids, rettype="xml", retmode="xml")
        records = Entrez.read(fetch_handle)
        fetch_handle.close()
        
        # Parse records
        papers = []
        for article in records["PubmedArticle"]:
            medline = article.get("MedlineCitation", {})
            article_data = medline.get("Article", {})
            
            # Extract data
            title = article_data.get("ArticleTitle", "No title")
            abstract = ""
            if "Abstract" in article_data:
                abstract_list = article_data["Abstract"].get("AbstractText", [])
                abstract = " ".join(abstract_list) if isinstance(abstract_list, list) else str(abstract_list)
            
            journal = ""
            if "Journal" in article_data:
                journal = article_data["Journal"].get("Title", "")
            
            year = ""
            if "JournalIssue" in article_data.get("Journal", {}):
                pub_date = article_data["Journal"]["JournalIssue"].get("PubDate", {})
                year = pub_date.get("Year", "")
            
            # Extract publication types
            pub_types = []
            if "PublicationTypeList" in medline:
                pub_types = [pt.get("#text", "") for pt in medline["PublicationTypeList"]]
            
            # Get PMID
            pmid = str(medline.get("PMID", {}))
            
            paper = {
                "pmid": pmid,
                "title": title,
                "abstract": abstract,
                "journal": journal,
                "year": year,
                "pub_types": pub_types
            }
            
            # Calculate quality score
            paper["quality_score"] = calculate_quality_score(paper)
            
            # Check for clinical trials
            paper["is_clinical_trial"] = any("Clinical Trial" in pt or "Randomized Controlled Trial" in pt for pt in pub_types)
            paper["is_rct"] = any("Randomized Controlled Trial" in pt for pt in pub_types)
            
            papers.append(paper)
        
        # Rate limiting
        time.sleep(1)
        
        return papers
    
    except Exception as e:
        print(f"Error fetching PubMed papers: {e}")
        raise HTTPException(status_code=500, detail=f"Error fetching papers: {str(e)}")

def get_quality_category(score: int) -> str:
    """Categorize quality score"""
    if score >= 80:
        return "high"
    elif score >= 60:
        return "good"
    elif score >= 40:
        return "moderate"
    else:
        return "low"

# API Endpoints
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "Toxicity Assessment RAG System",
        "version": "1.0.0",
        "description": "RAG system for toxicity assessment using PubMed papers",
        "endpoints": {
            "POST /load-papers": "Load papers from PubMed",
            "POST /assess": "Get toxicity assessment",
            "GET /stats": "Get database statistics",
            "GET /papers": "List papers in database",
            "DELETE /papers": "Clear database"
        }
    }

@app.post("/load-papers", response_model=LoadPapersResponse)
async def load_papers(request: LoadPapersRequest):
    """Load papers from PubMed into the database"""
    try:
        # Fetch papers
        papers = fetch_pubmed_papers(request.query, request.max_results)
        
        if not papers:
            return LoadPapersResponse(
                papers_loaded=0,
                average_quality_score=0,
                clinical_trial_count=0,
                message="No papers found for the query"
            )
        
        # Prepare documents for ChromaDB
        documents = []
        metadatas = []
        ids = []
        
        for paper in papers:
            doc_text = f"""Title: {paper['title']}
Journal: {paper['journal']} ({paper['year']})
Study Type: {'Randomized Controlled Trial' if paper['is_rct'] else 'Clinical Trial' if paper['is_clinical_trial'] else 'Observational'}
Quality Score: {paper['quality_score']}/100

Abstract:
{paper['abstract']}"""
            
            documents.append(doc_text)
            metadatas.append({
                "pmid": paper['pmid'],
                "quality_score": paper['quality_score'],
                "year": paper['year'],
                "is_rct": paper['is_rct'],
                "is_clinical_trial": paper['is_clinical_trial'],
                "journal": paper['journal'],
                "title": paper['title']
            })
            ids.append(f"pmid_{paper['pmid']}")
        
        # Add to ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        # Calculate statistics
        avg_quality = sum(p['quality_score'] for p in papers) / len(papers)
        clinical_trial_count = sum(1 for p in papers if p['is_clinical_trial'])
        
        return LoadPapersResponse(
            papers_loaded=len(papers),
            average_quality_score=round(avg_quality, 2),
            clinical_trial_count=clinical_trial_count,
            message="Papers loaded successfully"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/assess", response_model=AssessmentResponse)
async def assess(request: AssessmentRequest):
    """Get toxicity assessment for a substance"""
    try:
        # Query ChromaDB for relevant papers
        query_text = f"{request.substance} {request.product_type} toxicity"
        
        results = collection.query(
            query_texts=[query_text],
            n_results=request.max_papers,
            where={"quality_score": {"$gte": request.min_quality_score}}
        )
        
        if not results['documents'] or not results['documents'][0]:
            raise HTTPException(
                status_code=404,
                detail=f"No papers found for '{request.substance}' with quality score >= {request.min_quality_score}"
            )
        
        # Get papers
        papers = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        # Calculate average quality
        avg_quality = sum(m['quality_score'] for m in metadatas) / len(metadatas)
        
        # Prepare context for AI or basic analysis
        context = "\n\n".join(papers)
        
        # Generate assessment using Google Gemini or basic analysis
        prompt = f"""You are a toxicology expert. Analyze the following research papers about {request.substance} in {request.product_type}.

Usage frequency: {request.usage_frequency}

Research Papers:
{context}

Provide a comprehensive toxicity assessment including:
1. **Safety Rating:** (Low Risk / Moderate Risk / High Risk / Insufficient Data)
2. **Key Findings:** Most important findings from highest-quality studies
3. **Usage Frequency Impact:** How {request.usage_frequency} usage affects risk
4. **Vulnerable Populations:** Groups at higher risk (if any)
5. **Confidence Level:** (High/Moderate/Low) based on study quality and quantity
6. **Research Limitations:** Gaps or conflicts in the evidence

Be concise and evidence-based. Start with the safety rating."""

        # Try to use Google Gemini for assessment
        if GEMINI_AVAILABLE:
            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                assessment_text = response.text
            except Exception as e:
                print(f"Gemini error: {e}, falling back to basic assessment")
                assessment_text = generate_basic_assessment(request, metadatas)
        else:
            assessment_text = generate_basic_assessment(request, metadatas)
        
        # Parse risk level and confidence
        risk_level = "Unknown"
        confidence = "Unknown"
        
        assessment_lower = assessment_text.lower()
        if "low risk" in assessment_lower:
            risk_level = "Low Risk"
        elif "moderate risk" in assessment_lower:
            risk_level = "Moderate Risk"
        elif "high risk" in assessment_lower:
            risk_level = "High Risk"
        elif "insufficient data" in assessment_lower:
            risk_level = "Insufficient Data"
        
        if "high confidence" in assessment_lower or "high level" in assessment_lower:
            confidence = "High"
        elif "moderate confidence" in assessment_lower or "moderate level" in assessment_lower:
            confidence = "Moderate"
        elif "low confidence" in assessment_lower or "low level" in assessment_lower:
            confidence = "Low"
        
        # Prepare sources
        sources = []
        for i, metadata in enumerate(metadatas):
            sources.append({
                "pmid": metadata['pmid'],
                "title": metadata['title'],
                "journal": metadata['journal'],
                "year": metadata['year'],
                "quality_score": metadata['quality_score'],
                "is_clinical_trial": metadata['is_clinical_trial'],
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{metadata['pmid']}"
            })
        
        return AssessmentResponse(
            risk_level=risk_level,
            confidence=confidence,
            assessment=assessment_text,
            sources=sources,
            papers_analyzed=len(papers),
            avg_quality_score=round(avg_quality, 2)
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=DatabaseStats)
async def get_stats():
    """Get database statistics"""
    try:
        # Get all papers
        all_data = collection.get()
        
        if not all_data['ids']:
            return DatabaseStats(
                total_papers=0,
                average_quality_score=0,
                clinical_trial_count=0,
                quality_distribution={"high": 0, "good": 0, "moderate": 0, "low": 0}
            )
        
        # Calculate statistics
        metadatas = all_data['metadatas']
        total_papers = len(metadatas)
        
        quality_scores = [m['quality_score'] for m in metadatas]
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        clinical_trial_count = sum(1 for m in metadatas if m.get('is_clinical_trial', False))
        
        # Quality distribution
        quality_dist = {"high": 0, "good": 0, "moderate": 0, "low": 0}
        for score in quality_scores:
            category = get_quality_category(score)
            quality_dist[category] += 1
        
        return DatabaseStats(
            total_papers=total_papers,
            average_quality_score=round(avg_quality, 2),
            clinical_trial_count=clinical_trial_count,
            quality_distribution=quality_dist
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/papers")
async def get_papers(limit: int = 50):
    """List papers in database"""
    try:
        all_data = collection.get()
        
        if not all_data['ids']:
            return {"papers": [], "total": 0}
        
        # Limit results
        limit = min(limit, len(all_data['ids']))
        
        papers = []
        for i in range(limit):
            papers.append({
                "pmid": all_data['metadatas'][i]['pmid'],
                "title": all_data['metadatas'][i]['title'],
                "journal": all_data['metadatas'][i]['journal'],
                "year": all_data['metadatas'][i]['year'],
                "quality_score": all_data['metadatas'][i]['quality_score'],
                "is_clinical_trial": all_data['metadatas'][i].get('is_clinical_trial', False),
                "url": f"https://pubmed.ncbi.nlm.nih.gov/{all_data['metadatas'][i]['pmid']}"
            })
        
        return {"papers": papers, "total": len(all_data['ids'])}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/papers")
async def clear_papers():
    """Clear the entire database"""
    try:
        # Delete and recreate collection
        chroma_client.delete_collection(name="toxicity_papers")
        collection = chroma_client.create_collection(
            name="toxicity_papers",
            metadata={"hnsw:space": "cosine"}
        )
        
        return {"message": "Database cleared successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
