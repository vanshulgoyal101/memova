#!/bin/bash

# Memova - GitHub Deployment Helper
# This script helps you push your code to GitHub

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║          🚀 Push Memova to GitHub                          ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Get GitHub username
echo "Enter your GitHub username:"
read github_username

if [ -z "$github_username" ]; then
    echo "❌ GitHub username cannot be empty!"
    exit 1
fi

echo ""
echo "Repository will be created at:"
echo "  https://github.com/${github_username}/memova"
echo ""
echo "Have you created the repository on GitHub yet?"
echo "  1. Go to: https://github.com/new"
echo "  2. Repository name: memova"
echo "  3. Public ✓"
echo "  4. DO NOT add README, .gitignore, or license"
echo "  5. Click 'Create repository'"
echo ""
read -p "Press Enter when repository is created..."

echo ""
echo "Setting up Git remote..."
cd "/Volumes/Extreme SSD/code/sql schema"

# Check if origin already exists
if git remote get-url origin &> /dev/null; then
    echo "⚠️  Remote 'origin' already exists. Removing it..."
    git remote remove origin
fi

# Add new remote
git remote add origin "https://github.com/${github_username}/memova.git"
echo "✅ Remote added: https://github.com/${github_username}/memova.git"

echo ""
echo "Renaming branch to 'main'..."
git branch -M main
echo "✅ Branch renamed to 'main'"

echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║              ✅ Successfully pushed to GitHub!             ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "Your code is now at:"
echo "  https://github.com/${github_username}/memova"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Next Step: Deploy to Vercel"
echo ""
echo "1. Go to: https://vercel.com/new"
echo "2. Click 'Import Git Repository'"
echo "3. Select: ${github_username}/memova"
echo "4. Add environment variables:"
echo "     GROQ_API_KEY=your_groq_key"
echo "     GOOGLE_API_KEY=your_gemini_key"
echo "5. Click 'Deploy'"
echo ""
echo "Your app will be live at: https://memova.vercel.app"
echo ""
echo "Full instructions: See DEPLOY_NOW.md"
echo ""
