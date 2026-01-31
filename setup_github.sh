#!/bin/bash
#
# Automated GitHub Setup Script
# For: Tanzanian Rent Invoice Processor
# Repository: http://github.com/jmaccoe/tanzanian-rent-processor
#
# Usage: bash setup_github.sh
#

set -e  # Exit on error

echo "=================================================="
echo "GitHub Setup - Tanzanian Rent Invoice Processor"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
GITHUB_USER="jmaccoe"
REPO_NAME="tanzanian-rent-processor"
REPO_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "ℹ $1"
}

# Check if git is installed
echo "Checking prerequisites..."
if ! command -v git &> /dev/null; then
    print_error "Git is not installed!"
    echo "Please install Git first:"
    echo "  Ubuntu/Debian: sudo apt-get install git"
    echo "  macOS: brew install git"
    echo "  Windows: Download from https://git-scm.com/"
    exit 1
fi
print_success "Git is installed"

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    print_error "app.py not found!"
    echo "Please run this script from the project directory"
    exit 1
fi
print_success "Project files found"

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    print_info "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
else
    print_warning "Git repository already exists"
fi

# Configure git user if not set
if [ -z "$(git config user.name)" ]; then
    echo ""
    read -p "Enter your Git username: " git_username
    git config user.name "$git_username"
    print_success "Git username configured"
fi

if [ -z "$(git config user.email)" ]; then
    read -p "Enter your Git email: " git_email
    git config user.email "$git_email"
    print_success "Git email configured"
fi

# Rename README_GITHUB.md to README.md for GitHub display
if [ -f "README_GITHUB.md" ]; then
    print_info "Using GitHub-optimized README..."
    mv README.md README_DETAILED.md 2>/dev/null || true
    cp README_GITHUB.md README.md
    print_success "README prepared for GitHub"
fi

# Add all files
print_info "Adding files to Git..."
git add .
print_success "Files staged"

# Create initial commit
if [ -z "$(git log --oneline 2>/dev/null)" ]; then
    print_info "Creating initial commit..."
    git commit -m "Initial commit: Tanzanian rent invoice processor with WHT calculations

- Streamlit web app for invoice processing
- OCR support for images and PDFs
- Automatic WHT (10%) and VAT (18%) calculations
- Payment split calculations (landlord vs TRA)
- Compliance warnings and documentation
- Complete test suite
- Comprehensive documentation"
    print_success "Initial commit created"
else
    print_warning "Repository already has commits"
    read -p "Create a new commit with current changes? (y/n): " create_commit
    if [ "$create_commit" = "y" ]; then
        read -p "Enter commit message: " commit_msg
        git commit -m "$commit_msg" || print_warning "No changes to commit"
    fi
fi

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    print_warning "Remote 'origin' already exists"
    current_url=$(git remote get-url origin)
    echo "Current URL: $current_url"
    read -p "Do you want to update it to $REPO_URL? (y/n): " update_remote
    if [ "$update_remote" = "y" ]; then
        git remote set-url origin "$REPO_URL"
        print_success "Remote URL updated"
    fi
else
    print_info "Adding GitHub remote..."
    git remote add origin "$REPO_URL"
    print_success "Remote added: $REPO_URL"
fi

# Set main branch
print_info "Setting up main branch..."
git branch -M main
print_success "Branch set to 'main'"

# Display remote info
echo ""
echo "Remote repository:"
git remote -v
echo ""

# Ask before pushing
echo "=================================================="
echo "Ready to push to GitHub!"
echo "=================================================="
echo "Repository: $REPO_URL"
echo ""
print_warning "Make sure you have created the repository on GitHub first!"
echo "If not, go to: https://github.com/new"
echo "Repository name: $REPO_NAME"
echo ""
read -p "Push to GitHub now? (y/n): " do_push

if [ "$do_push" = "y" ]; then
    print_info "Pushing to GitHub..."
    echo ""
    echo "If prompted, use your GitHub username and Personal Access Token"
    echo "Create token at: https://github.com/settings/tokens"
    echo ""
    
    if git push -u origin main; then
        echo ""
        print_success "Successfully pushed to GitHub!"
        echo ""
        echo "Your repository is now available at:"
        echo "🔗 https://github.com/${GITHUB_USER}/${REPO_NAME}"
        echo ""
        echo "Next steps:"
        echo "1. Visit your repository on GitHub"
        echo "2. Add topics/tags (tanzania, tax-calculator, streamlit, etc.)"
        echo "3. Update repository description"
        echo "4. Consider adding a screenshot"
        echo ""
    else
        print_error "Push failed!"
        echo ""
        echo "Common issues and solutions:"
        echo "1. Repository doesn't exist on GitHub"
        echo "   → Create it at: https://github.com/new"
        echo ""
        echo "2. Authentication failed"
        echo "   → Use Personal Access Token instead of password"
        echo "   → Create at: https://github.com/settings/tokens"
        echo ""
        echo "3. Permission denied"
        echo "   → Verify you own the repository"
        echo "   → Check your username is correct: $GITHUB_USER"
        echo ""
        exit 1
    fi
else
    print_info "Push cancelled"
    echo "You can push manually later with:"
    echo "  git push -u origin main"
fi

echo ""
echo "=================================================="
echo "Setup Complete!"
echo "=================================================="
echo ""

# Cleanup: restore original README if needed
# (Uncomment if you want to keep both versions)
# if [ -f "README_DETAILED.md" ]; then
#     mv README_DETAILED.md README_FULL.md
#     print_info "Original README saved as README_FULL.md"
# fi
