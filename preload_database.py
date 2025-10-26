#!/usr/bin/env python3
"""
Preload ChromaDB database with research papers on toxic compounds
for pregnant women and those planning pregnancy.
"""

import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Import from main.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from main import (
    fetch_pubmed_papers, 
    calculate_quality_score,
    collection,
    chroma_client
)

# Toxic compounds for pregnant women
PREGNANCY_COMPOUNDS = {
    "retinoids": {
        "query": "retinoids retinyl palmitate retinol pregnancy teratogenic birth defects",
        "max_results": 15,
        "description": "Retinoids (vitamin A derivatives) - high risk during pregnancy"
    },
    "salicylic_acid": {
        "query": "salicylic acid aspirin pregnancy congenital malformations",
        "max_results": 15,
        "description": "Salicylic acid - anti-inflammatory risk in pregnancy"
    },
    "hydroquinone": {
        "query": "hydroquinone pregnancy skin lightening teratogenicity",
        "max_results": 15,
        "description": "Hydroquinone - skin lightening agent risk"
    },
    "formaldehyde": {
        "query": "formaldehyde pregnancy cosmetics miscarriage reproductive toxicity",
        "max_results": 15,
        "description": "Formaldehyde - carcinogen and reproductive toxin"
    },
    "parabens": {
        "query": "parabens pregnancy endocrine disruption reproductive health",
        "max_results": 15,
        "description": "Parabens - potential endocrine disruptors"
    }
}

# Toxic compounds for women planning pregnancy
PLANNING_COMPOUNDS = {
    "glycolic_acid": {
        "query": "glycolic acid fertility reproductive health pregnancy planning",
        "max_results": 10,
        "description": "Glycolic acid - fertility and reproductive effects"
    },
    "benzoyl_peroxide": {
        "query": "benzoyl peroxide fertility reproductive hormones acne treatment",
        "max_results": 10,
        "description": "Benzoyl peroxide - reproductive health considerations"
    }
}

def load_papers_for_compound(compound_name, search_query, max_results, description):
    """Load and store papers for a specific compound."""
    print(f"\n{'='*60}")
    print(f"Loading papers for: {compound_name}")
    print(f"Description: {description}")
    print(f"Query: {search_query}")
    print(f"{'='*60}\n")
    
    try:
        # Query PubMed
        papers = fetch_pubmed_papers(search_query, max_results)
        
        if not papers:
            print(f"❌ No papers found for {compound_name}")
            return 0
        
        # Store papers in ChromaDB
        added_count = 0
        for paper in papers:
            try:
                # Check if paper already exists
                results = collection.get(
                    where={"pmid": paper['pmid']},
                    limit=1
                )
                
                if results['ids']:
                    print(f"⏭️  Paper {paper['pmid']} already exists, skipping")
                    continue
                
                # Quality score is already calculated in paper dict
                quality_score = paper.get('quality_score', 0)
                
                # Create metadata
                metadata = {
                    'pmid': paper['pmid'],
                    'title': paper['title'],
                    'journal': paper.get('journal', 'Unknown'),
                    'year': paper.get('year', 'Unknown'),
                    'quality_score': quality_score,
                    'is_clinical_trial': paper.get('is_clinical_trial', False),
                    'abstract': paper.get('abstract', 'No abstract available'),
                    'compound': compound_name,
                    'category': 'pregnancy' if compound_name in PREGNANCY_COMPOUNDS else 'planning'
                }
                
                # Add to ChromaDB
                collection.add(
                    documents=[paper.get('abstract', 'No abstract available')],
                    metadatas=[metadata],
                    ids=[f"PMID_{paper['pmid']}"]
                )
                
                added_count += 1
                print(f"✅ Added paper {paper['pmid']}: {paper['title'][:70]}...")
                print(f"   Quality score: {quality_score}/100")
                
            except Exception as e:
                print(f"⚠️  Error adding paper {paper.get('pmid', 'unknown')}: {e}")
                continue
        
        print(f"\n✅ Successfully added {added_count} papers for {compound_name}")
        return added_count
        
    except Exception as e:
        print(f"❌ Error loading papers for {compound_name}: {e}")
        return 0

def main():
    """Main function to preload database."""
    print("\n" + "="*60)
    print("DATABASE PRELOADING SCRIPT")
    print("Loading toxic compound research papers")
    print("="*60)
    
    total_added = 0
    
    # Load pregnancy-related compounds
    print("\n" + "="*60)
    print("LOADING PREGNANCY-RELATED COMPOUNDS")
    print("="*60)
    for compound_name, compound_data in PREGNANCY_COMPOUNDS.items():
        added = load_papers_for_compound(
            compound_name=compound_name,
            search_query=compound_data["query"],
            max_results=compound_data["max_results"],
            description=compound_data["description"]
        )
        total_added += added
    
    # Load planning-related compounds
    print("\n" + "="*60)
    print("LOADING PLANNING PREGNANCY COMPOUNDS")
    print("="*60)
    for compound_name, compound_data in PLANNING_COMPOUNDS.items():
        added = load_papers_for_compound(
            compound_name=compound_name,
            search_query=compound_data["query"],
            max_results=compound_data["max_results"],
            description=compound_data["description"]
        )
        total_added += added
    
    # Summary
    print("\n" + "="*60)
    print("PRELOADING SUMMARY")
    print("="*60)
    print(f"Total papers added: {total_added}")
    print(f"Compounds loaded: {len(PREGNANCY_COMPOUNDS) + len(PLANNING_COMPOUNDS)}")
    print("="*60)
    
    # Get stats
    try:
        stats = collection.count()
        print(f"\nTotal papers in database: {stats}")
    except Exception as e:
        print(f"Could not get database stats: {e}")
    
    print("\n✅ Preloading complete!")
    print("\nThe database is now ready to serve faster responses for:")
    for compound in PREGNANCY_COMPOUNDS.keys():
        print(f"  - {compound} (pregnancy)")
    for compound in PLANNING_COMPOUNDS.keys():
        print(f"  - {compound} (planning)")
    print("\n")

if __name__ == "__main__":
    main()
