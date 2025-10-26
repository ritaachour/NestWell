# ⚠️ CRITICAL: Architecture & Security

## Where Things Live

### 🔵 Lovable Website (Frontend)
- What it has: User interface (forms, buttons)
- What it needs: `NEXT_PUBLIC_API_URL` (Railway URL only!)
- ❌ Does NOT have: Gemini API key, email, or any other secrets

### 🔴 Railway API (Backend)
- What it has: All the logic, database, AI calls
- Environment variables it needs:
  - `GEMINI_API_KEY` - For Google Gemini AI
  - `NCBI_EMAIL` - For PubMed API
  - `PORT` - Auto-set by Railway

---

## ❌ NEVER DO THIS

### Don't put API keys in Lovable:

```typescript
// ❌ NEVER PUT THIS IN LOVABLE
const GEMINI_KEY = "AIza..."; // WRONG!
```

### Don't call Railway APIs directly from Lovable frontend:

```typescript
// ❌ WRONG - Never do this
const response = await fetch('https://railway.app/load-papers', {
  headers: { 'Authorization': 'Bearer key123' } // NEVER!
});
```

---

## ✅ CORRECT ARCHITECTURE

```
User Browser
    ↓
Lovable Frontend (Public)
    ↓
Lovable Edge Function (app/api/check-ingredient/route.ts)
    ↓
Railway API (Has all secrets)
    ↓
Gemini AI, PubMed, ChromaDB
```

### Security Flow:

1. **User** types ingredient in Lovable form
2. **Lovable frontend** calls Lovable edge function: `/api/check-ingredient`
3. **Lovable edge function** (server-side) calls Railway API
4. **Railway API** (has all secrets) calls Gemini, PubMed, etc.

**Important:** Secrets never leave Railway!

---

## What Goes Where

### In Lovable (Only public URL):

```bash
NEXT_PUBLIC_API_URL=https://web-production-b9b9.up.railway.app
```

### In Railway (All secrets):

```bash
GEMINI_API_KEY=your-actual-key-here
NCBI_EMAIL=your@email.com
PORT=${{PORT}}
```

---

## Why This Separation?

✅ **Security**: Secrets stay on Railway  
✅ **Cost**: No API calls from browser  
✅ **Performance**: Edge function is faster  
✅ **Control**: All logic centralized  

---

## What Your Lovable Edge Function Does

Your `app/api/check-ingredient/route.ts` acts as a **proxy**:

1. Receives user input (ingredient name, life stage)
2. Calls Railway API with that input
3. Returns Railway's response to the user
4. **Never** has access to API keys itself

---

## Summary

**Lovable = Lightweight proxy**  
- Just passes requests to Railway
- Doesn't need secrets
- Only needs Railway URL

**Railway = Full backend**  
- Has all the logic
- Has all the secrets
- Does the real work

**Keep them separate!** 🔒
