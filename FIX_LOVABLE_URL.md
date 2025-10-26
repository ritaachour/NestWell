# Fix: Lovable Can't Reach Railway API

## The Issue

Your Railway API is working perfectly! ✅
- API responds at: `https://web-production-b9b9.up.railway.app`
- Endpoints are functional
- Returns data correctly

But Lovable is getting a 404. This means the URL in Lovable settings is wrong.

---

## Quick Fix

### Step 1: Check Lovable Secret

In Lovable:
1. Go to **Settings** → **Environment Variables** (or Secrets)
2. Find `NEXT_PUBLIC_API_URL`
3. Check the value

### Step 2: Update to Correct URL

**The correct URL is:**
```
https://web-production-b9b9.up.railway.app
```

**Make sure:**
- ✅ No trailing slash
- ✅ Full URL with `https://`
- ✅ No extra spaces

**Common mistakes:**
- ❌ `https://web-production-b9b9.up.railway.app/` (trailing slash)
- ❌ `http://web-production-b9b9.up.railway.app` (http instead of https)
- ❌ Placeholder like `https://your-railway-app.railway.app`

### Step 3: Save and Redeploy

1. Save the environment variable
2. Lovable should auto-redeploy
3. Wait for deployment to finish

### Step 4: Test

Try the ingredient checker again with "parabens"

---

## Verify the Fix

After updating, test:

```bash
# This should work from your machine
curl https://web-production-b9b9.up.railway.app/
```

If you can curl it, Lovable should be able to reach it too once the URL is set correctly.

---

## Still Getting 404?

### Debug Steps:

1. **Check Lovable logs:**
   - Open Lovable edge function logs
   - Look for the actual URL being called
   - Compare with correct URL

2. **Verify secret name:**
   - Must be exactly: `NEXT_PUBLIC_API_URL`
   - Case-sensitive

3. **Check for typos:**
   - Extra spaces?
   - Missing characters?
   - Wrong subdomain?

4. **Redeploy Lovable:**
   - Sometimes needs redeploy after env change
   - Check Lovable deployment logs

---

## Quick Checklist

- [ ] Lovable secret name: `NEXT_PUBLIC_API_URL`
- [ ] Secret value: `https://web-production-b9b9.up.railway.app`
- [ ] No trailing slash
- [ ] Using `https://` not `http://`
- [ ] Saved the secret
- [ ] Lovable redeployed
- [ ] Tested ingredient checker

---

## Expected Flow After Fix

1. User enters "parabens" in Lovable
2. Lovable calls `/api/check-ingredient`
3. Edge function calls: `https://web-production-b9b9.up.railway.app/load-papers`
4. Railway returns papers
5. User sees results ✅

Right now step 3 is probably using a wrong URL!

Good luck! 🚀
