# Git Workflow

## Branch Structure

- `main` - Production ready code
- `develop` - Development branch
- `feature/name` - New features (from develop)
- `fix/name` - Bug fixes (from develop)
- `hotfix/name` - Critical fixes (from main)

## Workflows

### Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/my-feature
# Make changes
git commit -m "feat: add new feature"
git push origin feature/my-feature
# Create Pull Request to develop
```

### Bug Fix

```bash
git checkout develop
git checkout -b fix/bug-description
# Make changes
git commit -m "fix: resolve issue"
git push origin fix/bug-description
```

### Release to Production

```bash
git checkout main
git merge develop
git push origin main
# Deploy
```

## Commit Messages

Format: `<type>: <subject>`

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `refactor` - Code refactoring
- `test` - Tests

## Protected Branches

- Do not push directly to `main`
- Use Pull Requests for code review
- Require approvals before merging
