# Fix: PubMed Links Blocked (ERR_BLOCKED_BY_RESPONSE)

## The Problem

When users click article links from your sources, they get an error:
```
pubmed.ncbi.nlm.nih.gov is blocked
ERR_BLOCKED_BY_RESPONSE
```

This is a **browser/network-level block**, not a code issue.

---

## Solutions

### Solution 1: Direct Links (Recommended)

Add an alternative direct link option that bypasses the block:

```tsx
{result.sources?.map((source: any, idx: number) => (
  <div key={idx} className="border-l-4 border-blue-500 pl-4 py-3 hover:bg-blue-50 rounded transition-colors">
    <a 
      href={`https://pubmed.ncbi.nlm.nih.gov/${source.pmid}/`}
      target="_blank"
      rel="noopener noreferrer"
      className="text-blue-600 hover:text-blue-800 hover:underline font-semibold text-base block mb-2"
    >
      {source.title}
    </a>
    <div className="text-sm text-gray-600 space-x-2">
      <span>{source.journal}</span>
      <span>•</span>
      <span>{source.year}</span>
      {source.is_clinical_trial && (
        <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs font-medium">
          Clinical Trial
        </span>
      )}
      <span className="text-gray-500">Quality: {source.quality_score}/100</span>
    </div>
    {/* Alternative link if main one fails */}
    <div className="mt-2 text-xs text-gray-500">
      <span>PMID: </span>
      <a 
        href={`https://www.ncbi.nlm.nih.gov/pubmed/${source.pmid}`}
        target="_blank"
        rel="noopener noreferrer"
        className="text-blue-500 hover:underline"
      >
        {source.pmid}
      </a>
    </div>
  </div>
))}
```

**What this does:**
- Primary link: `pubmed.ncbi.nlm.nih.gov/PMID/`
- Fallback link: `www.ncbi.nlm.nih.gov/pubmed/PMID`
- Shows PMID number for manual search

---

### Solution 2: Search Instead of Direct Link

If links are consistently blocked, provide a search option:

```tsx
<a 
  href={`https://pubmed.ncbi.nlm.nih.gov/?term=${encodeURIComponent(source.title)}`}
  target="_blank"
  rel="noopener noreferrer"
  className="text-blue-600 hover:text-blue-800 hover:underline font-semibold"
>
  {source.title}
</a>
<div className="text-xs text-gray-500 mt-1">
  Search: 
  <a 
    href={`https://pubmed.ncbi.nlm.nih.gov/?term=${source.pmid}`}
    target="_blank"
    className="text-blue-500 hover:underline ml-1"
  >
    PMID {source.pmid}
  </a>
</div>
```

This uses PubMed's search feature, which sometimes works even when direct links don't.

---

### Solution 3: Copy/Manual Access

For users with persistent blocks, provide manual access information:

```tsx
<div className="border-l-4 border-blue-500 pl-4 py-3">
  <div className="text-blue-600 font-semibold mb-2">{source.title}</div>
  <div className="text-sm text-gray-600 mb-3">
    {source.journal} • {source.year}
    {source.is_clinical_trial && (
      <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">
        Clinical Trial
      </span>
    )}
  </div>
  
  {/* Click to copy PMID */}
  <button
    onClick={() => {
      navigator.clipboard.writeText(source.pmid);
      alert('PMID copied! Paste into PubMed search.');
    }}
    className="text-xs bg-gray-100 hover:bg-gray-200 px-2 py-1 rounded border border-gray-300"
  >
    📋 Copy PMID: {source.pmid}
  </button>
  
  <div className="text-xs text-gray-500 mt-2">
    Search manually on PubMed.gov using PMID
  </div>
</div>
```

---

### Solution 4: Multiple Link Options

Provide both direct and search links:

```tsx
<div className="flex flex-col gap-2 mt-2">
  <a 
    href={`https://pubmed.ncbi.nlm.nih.gov/${source.pmid}/`}
    target="_blank"
    rel="noopener noreferrer"
    className="text-sm text-blue-600 hover:underline"
  >
    → Direct Link
  </a>
  <a 
    href={`https://pubmed.ncbi.nlm.nih.gov/?term=${source.pmid}`}
    target="_blank"
    rel="noopener noreferrer"
    className="text-sm text-blue-600 hover:underline"
  >
    → Search Link
  </a>
  <button
    onClick={() => {
      navigator.clipboard.writeText(source.pmid);
      alert(`Copied PMID: ${source.pmid}\n\nPaste this into PubMed search to find the article.`);
    }}
    className="text-sm text-blue-600 hover:underline text-left"
  >
    → Copy PMID: {source.pmid}
  </button>
</div>
```

---

## Root Cause Analysis

### Why This Happens:

1. **Network Policy**: Corporate/school networks block certain domains
2. **Browser Extensions**: Ad blockers, privacy tools blocking external links
3. **Firewall Rules**: Security software preventing outbound connections
4. **Geographic Restrictions**: Some regions may have access limitations
5. **Browser Settings**: Aggressive popup or content blocking

### Why It's Not Your Code:

- ✅ Your links are correctly formatted
- ✅ The URLs are valid (`pubmed.ncbi.nlm.nih.gov/8142110`)
- ✅ The error is browser/network level
- ✅ PubMed itself is blocking/redirecting

---

## Best Solution: Combined Approach

Use multiple access methods to maximize chances of success:

```tsx
{/* Research Sources */}
<div className="bg-white rounded-xl shadow-md p-6">
  <h3 className="text-2xl font-bold mb-4">Scientific Sources ({result.sources?.length || 0})</h3>
  
  <div className="space-y-3">
    {result.sources?.map((source: any, idx: number) => (
      <div key={idx} className="border-l-4 border-blue-500 pl-4 py-3 hover:bg-blue-50 rounded">
        {/* Title */}
        <div className="text-blue-600 font-semibold text-base mb-2">{source.title}</div>
        
        {/* Metadata */}
        <div className="text-sm text-gray-600 mb-3">
          {source.journal} • {source.year}
          {source.is_clinical_trial && (
            <span className="ml-2 px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs">
              Clinical Trial
            </span>
          )}
          <span className="ml-2 text-gray-500">Quality: {source.quality_score}/100</span>
        </div>
        
        {/* Access Options */}
        <div className="flex flex-wrap gap-2 text-sm">
          <a 
            href={`https://pubmed.ncbi.nlm.nih.gov/${source.pmid}/`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 hover:underline bg-blue-50 px-2 py-1 rounded"
          >
            Direct Link
          </a>
          <a 
            href={`https://pubmed.ncbi.nlm.nih.gov/?term=${source.pmid}`}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:text-blue-800 hover:underline bg-blue-50 px-2 py-1 rounded"
          >
            Search Link
          </a>
          <button
            onClick={() => {
              navigator.clipboard.writeText(source.pmid);
              alert(`Copied PMID: ${source.pmid}\n\nPaste this into PubMed to find the article.`);
            }}
            className="text-gray-600 hover:text-gray-800 bg-gray-100 px-2 py-1 rounded"
          >
            Copy PMID: {source.pmid}
          </button>
        </div>
      </div>
    ))}
  </div>
</div>
```

---

## User Education

Add a helpful note in your UI:

```tsx
{/* Info banner */}
<div className="bg-blue-50 border-l-4 border-blue-400 p-3 mb-4 rounded text-sm text-gray-700">
  💡 <strong>Having trouble accessing links?</strong> If you're behind a firewall or using restrictive browser settings, try:
  <ul className="list-disc list-inside mt-2 space-y-1">
    <li>Using the "Search Link" option instead of "Direct Link"</li>
    <li>Copying the PMID and manually searching on PubMed.gov</li>
    <li>Disabling browser extensions temporarily</li>
    <li>Contacting your network administrator</li>
  </ul>
</div>
```

---

## Summary

**The Issue:** Network/browser blocking PubMed connections

**The Solution:** Provide multiple access methods:
1. Direct link (may not work)
2. Search link (more reliable)
3. Copy PMID (always works)
4. User education

**Why This Happens:** 
- Not a code problem
- Network/firewall policy
- Browser extensions
- Security software

**Best Approach:** Give users options so they can always access the papers! 🔗
