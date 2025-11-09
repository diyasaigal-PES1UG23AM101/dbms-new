# CI/CD Pipeline Implementation Guide

## Step-by-Step Implementation Instructions

### Prerequisites
- ✅ Git installed on your system
- ✅ GitHub account
- ✅ Python 3.10+ installed
- ✅ All project files ready

---

## Part 1: Local Setup & Testing

### Step 1: Verify Your Project Structure
Make sure you have these files:
```
SE PROJECT PERSONAL/
├── server.py
├── index.html
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── pytest.ini
├── .gitignore
├── .dockerignore
├── tests/
│   ├── __init__.py
│   ├── test_server.py
│   ├── test_integration.py
│   └── test_server_extended.py
└── .github/
    └── workflows/
        └── ci-cd.yml
```

### Step 2: Test Locally First
Before pushing to GitHub, test everything locally:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run tests
python -m pytest tests/ -v

# 3. Check coverage (should be >= 75%)
python -m pytest tests/ -v --cov=server --cov-report=term-missing --cov-fail-under=75

# 4. Test Docker build (optional)
docker build -t iims .
docker run -p 5000:5000 iims
```

---

## Part 2: GitHub Repository Setup

### Step 3: Initialize Git Repository (if not already done)

```bash
# Navigate to your project directory
cd "C:\Users\Bhanavi D\sem 4\SEM 5\SE\Project\SE PROJECT PERSONAL"

# Initialize git
git init

# Add all files
git add .

# Make initial commit
git commit -m "Initial commit: IIMS with CI/CD pipeline"
```

### Step 4: Create GitHub Repository

1. **Go to GitHub**: https://github.com
2. **Click "New Repository"** (or the "+" icon)
3. **Repository Settings**:
   - Name: `iims-project` (or your preferred name)
   - Description: "IT Infrastructure Management System with CI/CD"
   - Visibility: Public or Private (your choice)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. **Click "Create repository"**

### Step 5: Connect Local Repository to GitHub

```bash
# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/iims-project.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Alternative (if you already have a repo):**
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/iims-project.git
git push -u origin main
```

---

## Part 3: CI/CD Pipeline Activation

### Step 6: Verify Pipeline Files Are Pushed

After pushing, verify the workflow file exists:
- Go to your GitHub repository
- Navigate to: `.github/workflows/ci-cd.yml`
- The file should be visible

### Step 7: Trigger the Pipeline

The pipeline will **automatically run** when:
- ✅ You push code to `main`, `master`, or `develop` branches
- ✅ You create a Pull Request to `main` or `master`
- ✅ You manually trigger it (workflow_dispatch)

**To manually trigger:**
1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "CI/CD Pipeline" workflow
4. Click "Run workflow" button
5. Select branch and click "Run workflow"

---

## Part 4: Viewing Pipeline Results

### Step 8: Monitor Pipeline Execution

1. **Go to GitHub Repository**
2. **Click "Actions" tab** (top navigation)
3. **You'll see:**
   - List of all workflow runs
   - Status: ✅ (green check) = passed, ❌ (red X) = failed, 🟡 (yellow dot) = running
   - Click on any run to see details

### Step 9: View Individual Job Results

Click on a workflow run to see:

**5 Main Jobs:**
1. **Build Application** - Verifies code compiles
2. **Run Tests** - Executes all 37 tests
3. **Code Coverage Analysis** - Checks coverage >= 75%
4. **Code Linting** - Code quality checks
5. **Security Scanning** - Vulnerability checks

**Additional Jobs:**
- **Build Docker Image** - Creates deployment artifact
- **Deploy Application** - Deploys to production (main/master only)

### Step 10: Download Artifacts

After pipeline runs, you can download:
- **Coverage Report** (HTML): Click on "coverage-report" artifact
- **Docker Image**: Click on "docker-image" artifact

---

## Part 5: Understanding Pipeline Stages

### Stage 1: BUILD ✅
- **Purpose**: Verify application builds
- **What it does**:
  - Installs Python dependencies
  - Verifies imports work
  - Checks syntax
- **Success Criteria**: No errors

### Stage 2: TEST ✅
- **Purpose**: Run all tests
- **What it does**:
  - Runs 37 unit and integration tests
  - Validates all functionality
- **Success Criteria**: All 37 tests pass

### Stage 3: COVERAGE ✅
- **Purpose**: Ensure code coverage >= 75%
- **What it does**:
  - Generates coverage report
  - Checks threshold (currently 95%)
  - Creates HTML/XML reports
- **Success Criteria**: Coverage >= 75% (we have 95%)

### Stage 4: LINT ✅
- **Purpose**: Code quality checks
- **What it does**:
  - Runs flake8 (PEP 8 compliance)
  - Checks formatting with black
- **Success Criteria**: No critical errors

### Stage 5: SECURITY ✅
- **Purpose**: Vulnerability scanning
- **What it does**:
  - Scans dependencies for known vulnerabilities
  - Uses safety tool
- **Success Criteria**: No critical vulnerabilities

### Stage 6: BUILD-DOCKER (Deployment Artifact) ✅
- **Purpose**: Create deployable container
- **What it does**:
  - Builds Docker image
  - Saves as artifact
- **Success Criteria**: Image builds successfully

### Stage 7: DEPLOY (Optional) ✅
- **Purpose**: Automated deployment
- **What it does**:
  - Deploys to production server
  - Runs health checks
- **Success Criteria**: Deployment successful (requires secrets setup)

---

## Part 6: Optional Configuration

### Setting Up Deployment Secrets (Optional)

If you want automated deployment, add these secrets in GitHub:

1. **Go to Repository Settings**
2. **Click "Secrets and variables" → "Actions"**
3. **Add these secrets** (if deploying):

   - `DOCKER_USERNAME` - Your Docker Hub username
   - `DOCKER_PASSWORD` - Your Docker Hub password
   - `DEPLOY_HOST` - Your server IP/domain
   - `DEPLOY_USER` - SSH username
   - `DEPLOY_SSH_KEY` - SSH private key

**Note**: Deployment is optional. The pipeline works without it.

---

## Part 7: Daily Workflow

### Making Changes and Testing

```bash
# 1. Make your code changes
# Edit server.py, index.html, etc.

# 2. Test locally first
python -m pytest tests/ -v --cov=server --cov-fail-under=75

# 3. Commit changes
git add .
git commit -m "Description of changes"

# 4. Push to GitHub
git push origin main

# 5. Pipeline runs automatically!
# Check "Actions" tab to see results
```

### Creating Feature Branches

```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Make changes and commit
git add .
git commit -m "Add new feature"

# 3. Push branch
git push origin feature/new-feature

# 4. Create Pull Request on GitHub
# Pipeline will run automatically on PR
```

---

## Part 8: Troubleshooting

### Pipeline Fails - What to Check?

1. **Build Fails**:
   - Check Python syntax
   - Verify all imports work
   - Run: `python -m py_compile server.py`

2. **Tests Fail**:
   - Run tests locally: `python -m pytest tests/ -v`
   - Fix failing tests
   - Ensure all tests pass locally

3. **Coverage Fails**:
   - Check coverage: `python -m pytest tests/ --cov=server --cov-report=term-missing`
   - Add more tests if below 75%
   - Currently at 95%, so should pass

4. **Lint Fails**:
   - Run: `flake8 server.py`
   - Fix formatting issues
   - Or run: `black server.py` to auto-format

5. **Security Scan Fails**:
   - Update vulnerable packages
   - Check: `safety check --file requirements.txt`

### Common Issues

**Issue**: "Module not found"
- **Solution**: Ensure `requirements.txt` has all dependencies

**Issue**: "Tests fail in CI but pass locally"
- **Solution**: Reset auth state in tests (already done in setUp)

**Issue**: "Coverage below 75%"
- **Solution**: Add more tests (we have 95%, so not an issue)

---

## Part 9: Verification Checklist

Before submitting, verify:

- [ ] All files pushed to GitHub
- [ ] `.github/workflows/ci-cd.yml` exists
- [ ] Pipeline runs successfully (green checkmarks)
- [ ] All 5 stages pass (build, test, coverage, lint, security)
- [ ] Coverage >= 75% (we have 95%)
- [ ] All 37 tests pass
- [ ] Docker image builds successfully
- [ ] No critical errors in pipeline

---

## Quick Start Commands

```bash
# Complete setup in one go
cd "C:\Users\Bhanavi D\sem 4\SEM 5\SE\Project\SE PROJECT PERSONAL"

# Test everything locally
python -m pytest tests/ -v --cov=server --cov-fail-under=75

# Initialize git (if not done)
git init
git add .
git commit -m "Initial commit with CI/CD"

# Connect to GitHub (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/iims-project.git
git branch -M main
git push -u origin main

# Pipeline runs automatically!
```

---

## Summary

✅ **Your CI/CD pipeline is ready!**

1. **Push code to GitHub** → Pipeline runs automatically
2. **Check "Actions" tab** → See pipeline results
3. **All 5 stages execute** → Build, Test, Coverage, Lint, Security
4. **Deployment artifact created** → Docker image
5. **95% code coverage** → Exceeds 75% requirement

**The pipeline will run automatically on every push!**

