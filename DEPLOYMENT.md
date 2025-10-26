# Deployment

## Railway

```bash
npm install -g @railway/cli
railway login
railway init
railway variables set GEMINI_API_KEY=your-key
railway variables set NCBI_EMAIL=your@email.com
railway up
```

## Render

1. Connect GitHub repository
2. Create Web Service
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables in dashboard:
   - `GEMINI_API_KEY`
   - `NCBI_EMAIL`

## Environment Variables

All platforms require:

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Google Gemini API key |
| `NCBI_EMAIL` | Your email for PubMed |
| `PORT` | Server port (auto-set by platform) |

## Testing Production

```bash
curl https://your-app.railway.app/
curl https://your-app.railway.app/stats
```

## Notes

- ChromaDB filesystem is temporary on most platforms
- Consider PostgreSQL with pgvector for production persistence
- Add authentication for production APIs
