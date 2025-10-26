# Google Gemini Setup

The system uses Google Gemini for AI-powered toxicity assessments. The free tier is sufficient for most use cases.

## Get API Key

1. Visit https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

## Configure

Add to your `.env` file:

```
GEMINI_API_KEY=your-key-here
```

## Install Package

```bash
pip install google-generativeai==0.3.1
```

Or reinstall all dependencies:

```bash
pip install -r requirements.txt
```

## Verify

Restart the server and test an assessment request.

## Fallback Mode

If Gemini API is unavailable, the system falls back to basic assessment mode that analyzes paper quality scores and provides summary statistics.

## Cost

- Free tier: 60 requests/minute
- After free tier: $0.000125 per 1K characters
- Estimated cost per assessment: $0.002
