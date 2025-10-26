# Git Workflow & Branching Strategy

## 🌳 Branch Structure

We use a **Git Flow** workflow with the following branches:

### **Main Branches**

- **`main`** - Production-ready code
  - Only stable, tested code
  - Always deployable
  - Protected branch (no direct pushes)
  - Deployed to production

- **`develop`** - Development branch
  - Integration branch for features
  - All feature branches merge here
  - Testing branch before production

### **Supporting Branches**

- **`feature/feature-name`** - New features
  - Created from `develop`
  - Merged back to `develop`
  - Deleted after merge

- **`fix/bug-name`** - Bug fixes
  - Created from `develop`
  - Merged back to `develop`
  - Deleted after merge

- **`hotfix/critical-fix`** - Urgent production fixes
  - Created from `main`
  - Merged to both `main` and `develop`
  - Deleted after merge

---

## 🚀 Common Workflows

### Starting a New Feature

```bash
# Switch to develop
git checkout develop

# Pull latest changes
git pull origin develop

# Create feature branch
git checkout -b feature/add-user-authentication

# Make your changes...
git add .
git commit -m "Add user authentication feature"

# Push to GitHub
git push origin feature/add-user-authentication

# Create Pull Request on GitHub to merge into develop
```

### Fixing a Bug

```bash
# Switch to develop
git checkout develop

# Pull latest changes
git pull origin develop

# Create fix branch
git checkout -b fix/login-page-error

# Make your changes...
git add .
git commit -m "Fix login page error"

# Push to GitHub
git push origin fix/login-page-error

# Create Pull Request to merge into develop
```

### Hotfix Production Issue

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull origin main

# Create hotfix branch
git checkout -b hotfix/security-patch

# Make your changes...
git add .
git commit -m "Apply critical security patch"

# Push to GitHub
git push origin hotfix/security-patch

# Create Pull Request to merge into main AND develop
```

### Release to Production

```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Merge develop into main
git checkout main
git merge develop

# Push to main
git push origin main

# Deploy to production
# (e.g., Railway, Render, etc.)
```

---

## 📋 Commit Message Guidelines

### Format
```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good commit messages
git commit -m "feat: add Google Gemini integration"
git commit -m "fix: resolve PubMed API timeout error"
git commit -m "docs: update deployment instructions"
git commit -m "refactor: simplify quality scoring algorithm"

# Bad commit messages
git commit -m "update code"
git commit -m "fixed stuff"
git commit -m "changes"
```

---

## 🔒 Protected Branches

### Main Branch Protection Rules:
1. ✅ Require pull request reviews
2. ✅ No direct pushes (only via PR)
3. ✅ Require status checks to pass
4. ✅ Require branches to be up to date

### Steps to Merge to Main:
1. Create feature branch from `develop`
2. Make changes and commit
3. Push to GitHub
4. Create Pull Request to `develop`
5. Get code review and approval
6. Merge to `develop`
7. Test on `develop` branch
8. Create Pull Request from `develop` to `main`
9. Merge to `main` after final approval

---

## 🌐 GitHub Setup

### Initial Setup

```bash
# Add GitHub remote (replace with your repo URL)
git remote add origin https://github.com/yourusername/nestwell-mvp.git

# Push to GitHub
git push -u origin main

# Push develop branch
git checkout develop
git push -u origin develop
```

### Daily Workflow

```bash
# Start of day - update local branches
git checkout develop
git pull origin develop

# Work on feature
git checkout -b feature/my-feature
# ... make changes ...
git push origin feature/my-feature

# End of day - update develop
git checkout develop
git pull origin develop
```

---

## 🚨 Important Security Rules

### ✅ DO:
- ✅ Commit `.env.example` (template file)
- ✅ Keep `.env` in `.gitignore`
- ✅ Never commit API keys or secrets
- ✅ Use Pull Requests for code review
- ✅ Test before merging to main

### ❌ DON'T:
- ❌ Commit `.env` file
- ❌ Push API keys to GitHub
- ❌ Commit database files
- ❌ Push directly to main
- ❌ Merge without testing

---

## 📝 Branch Naming Conventions

### Format: `type/short-description`

**Types:**
- `feature/` - New features
- `fix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring

**Examples:**
```bash
feature/add-quality-scoring
fix/pubmed-api-error
hotfix/security-vulnerability
docs/update-api-documentation
refactor/cleanup-database-code
```

---

## 🔄 Pull Request Workflow

### Creating a Pull Request:

1. **Push your branch to GitHub**
   ```bash
   git push origin feature/my-feature
   ```

2. **Go to GitHub repository**
   - Click "Pull requests"
   - Click "New pull request"
   - Select your feature branch → target branch

3. **Fill out PR template**
   - Title: Clear, descriptive
   - Description: What changed and why
   - Reviewers: Tag team members
   - Labels: Add relevant labels

4. **Wait for review**
   - Address feedback
   - Push updates if needed

5. **Merge after approval**
   - Squash and merge (recommended)
   - Delete branch after merge

---

## 🎯 Quick Reference

```bash
# View branches
git branch -a

# Create branch
git checkout -b feature/new-feature

# Switch branch
git checkout develop

# Delete branch
git branch -d feature/old-feature

# View commit history
git log --oneline --graph

# Undo last commit (keep changes)
git reset HEAD~1

# Stash changes temporarily
git stash
git stash pop
```

---

## 🆘 Troubleshooting

### "Cannot push to main"
- Main is protected, use Pull Requests

### "Branch diverged"
```bash
git pull origin branch-name --rebase
```

### "Undo a merge"
```bash
git revert -m 1 HEAD
```

### "Lose uncommitted changes"
```bash
git stash  # Save for later
git reset --hard  # Discard
```

---

## 📚 Additional Resources

- [Git Flow Documentation](https://nvie.com/posts/a-successful-git-branching-model/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

Happy coding! 🚀
