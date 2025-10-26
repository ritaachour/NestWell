# Quick Start

## Setup

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp .env.example .env
# Edit .env with your keys
```

## Environment Variables

Create `.env` file:

```
GEMINI_API_KEY=your-key-here
NCBI_EMAIL=your@email.com
PORT=8000
```

## Run Server

```bash
uvicorn main:app --reload
```

## Test API

Visit http://localhost:8000/docs for interactive API documentation.

### Example: Load Papers

```bash
curl -X POST http://localhost:8000/load-papers \
  -H "Content-Type: application/json" \
  -d '{"query": "parabens cosmetics toxicity", "max_results": 10}'
```

### Example: Get Assessment

```bash
curl -X POST http://localhost:8000/assess \
  -H "Content-Type: application/json" \
  -d '{
    "substance": "parabens",
    "product_type": "cosmetics",
    "usage_frequency": "daily",
    "min_quality_score": 50,
    "max_papers": 5
  }'
```

## Troubleshooting

- **ModuleNotFoundError**: Ensure virtual environment is activated
- **Port in use**: Change PORT in .env or kill process on port 8000
- **API errors**: Check .env file has correct keys
