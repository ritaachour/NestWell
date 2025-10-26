# Setting Up Secrets in Lovable

## What You're Seeing

The "Add Secret" interface in Lovable lets you securely store sensitive information like API URLs and keys.

## How to Add Your API URL

### Step 1: Fill in the Secret Name

In the "Secret Name" field, enter:
```
NEXT_PUBLIC_API_URL
```

**Why this name?**
- In Next.js, environment variables that should be available in the browser must start with `NEXT_PUBLIC_`
- This makes it accessible in both client and server code

### Step 2: Enter Your API URL

Click the eye icon (👁️) to toggle visibility, then enter your Railway API URL:

```
https://your-railway-app.railway.app
```

Replace `your-railway-app` with your actual Railway app name.

### Step 3: Click Submit

The secret is now securely stored and will be available to your app.

---

## Important Notes

### ✅ DO:
- Store the API URL as a secret in Lovable
- Use the exact name: `NEXT_PUBLIC_API_URL`
- Use your actual Railway URL (not a placeholder)

### ❌ DON'T:
- Hardcode the URL in your code
- Share the URL publicly
- Use test credentials

---

## Example

**What you see in Lovable:**

```
Secret Name: NEXT_PUBLIC_API_URL
Secret Value: https://nestwell-api.railway.app
```

**How your code uses it:**

```typescript
// In your API route (app/api/check-ingredient/route.ts)
const API_URL = process.env.NEXT_PUBLIC_API_URL;

// Automatically gets: https://nestwell-api.railway.app
```

---

## Complete Setup

After adding the secret in Lovable:

1. ✅ Secret name: `NEXT_PUBLIC_API_URL`
2. ✅ Secret value: Your Railway URL
3. ✅ Saved and encrypted
4. ✅ Available to your app as `process.env.NEXT_PUBLIC_API_URL`

Your API URL is now secure and won't be exposed in your code! 🔒
