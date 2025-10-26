# Launch Steps for Lovable Website

## Pre-Launch Checklist

### ✅ Backend API (Already Done)
- [x] API deployed to Railway/Render
- [x] API is working and responding
- [x] Environment variables set

### 📋 Frontend Setup

## Step-by-Step Launch Guide

### Step 1: Deploy Your Backend API

**If not already deployed:**

1. Go to Railway (or Render)
2. Ensure environment variables are set:
   ```
   GEMINI_API_KEY=your-key
   NCBI_EMAIL=your@email.com
   ```
3. Note your API URL (e.g., `https://your-api.railway.app`)

**Test your API:**
```bash
curl https://your-api.railway.app/
```

Should return API information.

---

### Step 2: Set Up Environment Variable in Lovable

1. Open your Lovable project
2. Go to **Settings** → **Environment Variables**
3. Add:
   ```
   NEXT_PUBLIC_API_URL=https://your-api.railway.app
   ```
   Replace with your actual Railway/Render URL

4. **Save** (Lovable may auto-deploy)

---

### Step 3: Create the Ingredient Checker Page

In your Lovable project:

1. Create new file: `app/ingredient-check/page.tsx`
2. Copy the entire component from `LOVABLE_MVP.md` (the full page.tsx section)
3. Save the file

**File structure should be:**
```
app/
  ingredient-check/
    page.tsx    ← New file
```

---

### Step 4: Create the API Route

1. Create new folder: `app/api/check-ingredient/`
2. Create file: `route.ts` inside that folder
3. Copy the API route code from `LOVABLE_MVP.md`
4. Save the file

**File structure:**
```
app/
  api/
    check-ingredient/
      route.ts    ← New file
```

---

### Step 5: Update Your Homepage

Open your main page (probably `app/page.tsx` or `src/app/page.tsx`):

Add a link to the ingredient checker:

```tsx
import Link from 'next/link';

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-16">
      <div className="text-center">
        <h1 className="text-5xl font-bold mb-4">
          Know what's safe for your growing family
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          Research-backed ingredient safety for pregnancy, postpartum, and beyond
        </p>
        <Link 
          href="/ingredient-check"
          className="inline-block bg-blue-600 text-white px-8 py-4 rounded-lg text-lg font-semibold hover:bg-blue-700 transition-colors"
        >
          Check an ingredient →
        </Link>
      </div>
    </div>
  );
}
```

---

### Step 6: Test Locally (Optional but Recommended)

If Lovable has a local dev option:

1. Run: `npm run dev`
2. Visit: `http://localhost:3000/ingredient-check`
3. Test with ingredient "retinol" + "cosmetics"
4. Verify it works

---

### Step 7: Deploy to Production

**Lovable automatically deploys when you push changes.**

1. Make sure all files are saved
2. Lovable will auto-deploy
3. Check the deployment status in Lovable dashboard

---

### Step 8: Test the Live Site

1. Visit your deployed Lovable site
2. Click "Check an ingredient"
3. Test the flow:
   - Select "Pregnant"
   - Enter "retinol"
   - Select "Skincare & Cosmetics"
   - Click "Check Safety"
4. Verify results appear

---

## Troubleshooting

### "Failed to check ingredient" Error

**Check:**
1. Environment variable is set correctly
2. API URL is correct (no trailing slash)
3. Backend API is deployed and running
4. CORS is enabled (should be by default)

**Debug:**
- Check Lovable logs in deployment tab
- Test API directly: `curl https://your-api.railway.app/`
- Check browser console for errors

### Results Not Showing

**Possible issues:**
- API is slow (PubMed search takes 30+ seconds)
- No papers found for that ingredient
- Backend error (check Railway logs)

**Solution:**
- Test with common ingredients: "parabens", "phthalates"
- Wait for full response (can take 30-60 seconds)
- Check backend logs

### Environment Variable Not Working

**Fix:**
1. Redeploy after setting env variable
2. Check spelling: `NEXT_PUBLIC_API_URL` (exact case)
3. Restart Lovable deployment

---

## Post-Launch Testing

### Test These Ingredients:
1. ✅ **Retinol** - skincare, should find pregnancy risks
2. ✅ **Parabens** - cosmetics, moderate concern
3. ✅ **BPA** - food/plastics, well-researched
4. ✅ **Salicylic acid** - skincare, pregnancy concern

### Expected Behavior:
- Loading state appears
- Results show within 30-60 seconds
- Risk level is clearly displayed
- Sources are clickable
- Mobile works well

---

## Quick Launch Checklist

- [ ] Backend API deployed and working
- [ ] Environment variable added to Lovable
- [ ] `app/ingredient-check/page.tsx` created
- [ ] `app/api/check-ingredient/route.ts` created
- [ ] Homepage updated with link
- [ ] Changes saved and deployed
- [ ] Live site tested
- [ ] Tested on mobile

---

## Next Steps After Launch

### Week 1: Monitor & Fix
- Monitor error rates
- Collect user feedback
- Fix any immediate bugs

### Week 2: Optimize
- Add loading skeletons
- Cache common searches
- Improve mobile UX

### Week 3: Enhance
- Add ingredient autocomplete
- Show common ingredients
- Add "recent searches" feature

---

## Going Live

**Once everything works:**
1. Share with beta users
2. Ask for feedback
3. Monitor performance
4. Iterate based on feedback

**Marketing tips:**
- Post on pregnancy/parenting forums
- Share on social media
- Partner with pregnancy influencers
- Add to product hunt

---

## Support

If issues arise:
1. Check Lovable deployment logs
2. Check Railway/Render logs
3. Test API directly with curl
4. Review browser console errors

**Common fixes:**
- Clear Lovable cache and redeploy
- Verify environment variables
- Check API is not rate-limited
- Ensure CORS headers are correct

Good luck with your launch! 🚀
