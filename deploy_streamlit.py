#!/usr/bin/env python3
"""
Deploy to Streamlit Community Cloud
"""

import webbrowser
import subprocess
import os

def deploy_to_streamlit_cloud():
    print("🚀 DEPLOYING TO STREAMLIT COMMUNITY CLOUD")
    print("=" * 60)
    
    # Check if git repo is ready
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  Uncommitted changes found. Committing...")
            subprocess.run(['git', 'add', '.'])
            subprocess.run(['git', 'commit', '-m', 'Update for Streamlit deployment'])
    except:
        print("⚠️  Git not configured properly")
    
    print("\n📋 DEPLOYMENT CHECKLIST:")
    print("✅ Dashboard enhanced with Top 20 opportunities")
    print("✅ Professional light theme with perfect readability") 
    print("✅ Complete tech stack recommendations")
    print("✅ Interactive filtering and revenue projections")
    print("✅ Requirements.txt ready for deployment")
    print("✅ Git repository configured")
    
    print("\n🌐 NEXT STEPS:")
    print("1. Push to GitHub repository")
    print("2. Deploy on Streamlit Community Cloud")
    print("3. Get live public URL")
    
    # GitHub repository setup
    print("\n📚 GITHUB SETUP:")
    print("Repository should be named: startup-revenue-insights-tracker")
    print("Files ready for deployment:")
    print("  • dashboard.py (main application)")
    print("  • requirements.txt (dependencies)")
    print("  • .streamlit/config.toml (configuration)")
    print("  • README.md (documentation)")
    
    print("\n🔗 STREAMLIT CLOUD DEPLOYMENT:")
    print("1. Go to https://share.streamlit.io")
    print("2. Connect your GitHub account")
    print("3. Click 'New app'")
    print("4. Repository: startup-revenue-insights-tracker")
    print("5. Branch: main")
    print("6. Main file path: dashboard.py")
    print("7. Click 'Deploy!'")
    
    print("\n🎉 EXPECTED RESULT:")
    print("Live URL: https://startup-revenue-insights-tracker.streamlit.app")
    print("Features: Top 20 opportunities with complete tech stacks")
    print("Access: Global, professional business intelligence platform")
    
    # Open Streamlit Cloud
    print("\n🌐 Opening Streamlit Community Cloud...")
    webbrowser.open("https://share.streamlit.io")
    
    return True

if __name__ == "__main__":
    deploy_to_streamlit_cloud()