# GitHub Setup Guide

## 🚀 Push Your Code to GitHub

Your local repository is ready! Now let's push it to GitHub.

---

## Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `nestwell-mvp` (or your preferred name)
3. Description: "Toxicity Assessment RAG System - FastAPI backend with PubMed integration"
4. **Keep it Private** (recommended for security)
5. **DO NOT** initialize with README, .gitignore, or license
6. Click "Create repository"

---

## Step 2: Add GitHub Remote

Copy the repository URL from GitHub, then run:

```bash
# Add GitHub remote (replace with your URL)
git remote add origin https://github.com/YOUR_USERNAME/nestwell-mvp.git

# Verify it was added
git remote -v
```

---

## Step 3: Push to GitHub

```bash
# Push main branch
git push -u origin main

# Push develop branch
git checkout develop
git push -u origin develop

# Go back to main
git checkout main
```

---

## Step 4: Set Up Branch Protection (Important!)

### Protect Main Branch:

1. Go to your repository on GitHub
2. Click **Settings** → **Branches**
3. Click **Add branch protection rule**
4. Branch name pattern: `main`
5. Enable these settings:
   - ✅ Require a pull request before merging
   - ✅ Require approvals (1)
   - ✅ Dismiss stale pull request approvals
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Require conversation resolution before merging
6. Click **Create**

---

## Step 5: Verify Security

Check that sensitive files are NOT on GitHub:

```bash
# Make sure .env is not tracked
git ls-files | grep .env
# Should output nothing or just .env.example

# Verify .gitignore is working
git check-ignore -v .env
# Should show: .gitignore:27:.env    .env
```

---

## 🎉 Done!

Your code is now on GitHub with:

✅ **Two branches:**
- `main` - Production ready
- `develop` - Development branch

✅ **Security:**
- `.env` file is ignored
- API keys protected
- `.env.example` template included

✅ **Git Flow:**
- Documented workflow
- Best practices implemented

---

## 📝 Next Steps

### Create a Feature Branch:

```bash
# Switch to develop
git checkout develop

# Create feature branch
git checkout -b feature/add-new-endpoint

# Make your changes...
git add .
git commit -m "feat: add new endpoint for batch processing"

# Push feature branch
git push origin feature/add-new-endpoint

# Create Pull Request on GitHub to merge into develop
```

---

## 🔒 Security Checklist

Before pushing any changes, verify:

- [ ] `.env` is in `.gitignore`
- [ ] `.env` is NOT tracked by Git
- [ ] `.env.example` exists (template)
- [ ] No API keys in code
- [ ] No passwords committed
- [ ] No database credentials exposed

---

## 🚨 If You Accidentally Committed Secrets

If you accidentally committed sensitive information:

```bash
# Remove from Git history (but keep local file)
git rm --cached .env

# Commit the removal
git commit -m "Remove .env from tracking"

# Push the fix
git push origin main

# Update .gitignore if needed
# Add .env to .gitignore
# Commit and push .gitignore changes
```

**Important:** If you pushed secrets to GitHub:
1. **Immediately revoke/regenerate the API keys**
2. Remove them from Git history (see above)
3. Never commit secrets again!

---

## 📚 Repository Settings on GitHub

Recommended repository settings:

1. **Settings** → **General**
   - ✅ Delete this repository: **ON** (for testing repos)
   - ✅ Features: Enable issues, wiki, etc.

2. **Settings** → **Secrets and variables** → **Actions**
   - Add your environment variables here if using GitHub Actions

3. **Settings** → **Pages**
   - Enable if you want to host documentation

---

## 🔄 Daily Workflow

```bash
# Morning: Update local branches
git checkout develop
git pull origin develop

# Work on feature
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature

# Create Pull Request on GitHub

# After PR is approved and merged:
git checkout develop
git pull origin develop
git branch -d feature/my-feature
```

---

## 📊 View Your Repository

After pushing, visit:
- `https://github.com/YOUR_USERNAME/nestwell-mvp`

You should see:
- ✅ README.md
- ✅ All code files
- ✅ Documentation files
- ✅ Two branches (main, develop)
- ❌ NO .env file (protected!)

---

## 🆘 Troubleshooting

### "Remote origin already exists"
```bash
git remote remove origin
git remote add origin YOUR_GITHUB_URL
```

### "Permission denied"
- Check you're authenticated to GitHub
- Use SSH keys or GitHub CLI

### "Branch 'main' is protected"
- Create a Pull Request instead
- Don't push directly to main

---

Your repository is now secure and follows best practices! 🎉
