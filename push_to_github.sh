#!/bin/bash

echo "🚀 PUSHING STARTUP REVENUE INSIGHTS TRACKER TO GITHUB"
echo "=" * 60

# Ensure we're in the right directory
cd /Users/jeremywilliams/Workspace/startup_revenue_insights_tracker

# Check git status
echo "📋 Checking git repository status..."
git status

# Add any remaining files
echo "📦 Adding all files..."
git add .

# Check if there are any changes to commit
if git diff --staged --quiet; then
    echo "✅ No new changes to commit"
else
    echo "💾 Committing final changes..."
    git commit -m "Final commit before GitHub push - Ready for deployment"
fi

echo ""
echo "🎯 REPOSITORY READY FOR GITHUB PUSH"
echo ""
echo "📋 Repository Contents:"
ls -la

echo ""
echo "🔗 NEXT STEPS:"
echo "1. Go to: https://github.com/new"
echo "2. Repository name: startup-revenue-insights-tracker"
echo "3. Description: Professional Business Intelligence Platform - Top 20 Startup Opportunities with Complete Tech Stacks"
echo "4. Make it PUBLIC (required for Streamlit Cloud)"
echo "5. Don't initialize with README"
echo "6. Click 'Create repository'"
echo ""
echo "7. Then run these commands:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/startup-revenue-insights-tracker.git"
echo "   git push -u origin main"
echo ""
echo "🌐 After GitHub push, deploy on Streamlit Cloud:"
echo "   Visit: https://share.streamlit.io"
echo "   New app -> startup-revenue-insights-tracker -> dashboard.py -> Deploy"
echo ""
echo "✅ Your professional business intelligence platform will be live!"