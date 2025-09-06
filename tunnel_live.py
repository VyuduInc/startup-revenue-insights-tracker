#!/usr/bin/env python3
"""
Make dashboard instantly accessible via public tunnel
"""

import subprocess
import time
import threading
import webbrowser

def run_streamlit():
    """Run Streamlit dashboard"""
    subprocess.run([
        "streamlit", "run", "dashboard.py",
        "--server.port", "8507",
        "--server.headless", "true"
    ])

def main():
    print("🚀 LAUNCHING LIVE DASHBOARD")
    print("=" * 40)
    
    # Start Streamlit in background
    print("📊 Starting dashboard...")
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)
    streamlit_thread.start()
    
    # Wait for Streamlit to start
    print("⏳ Waiting for dashboard to initialize...")
    time.sleep(8)
    
    try:
        from pyngrok import ngrok
        
        # Create public tunnel
        print("🌐 Creating public tunnel...")
        public_url = ngrok.connect(8507)
        
        print("\n" + "=" * 60)
        print("🎉 DASHBOARD IS NOW LIVE!")
        print("=" * 60)
        print(f"🌍 PUBLIC URL: {public_url}")
        print("📱 Share this URL with anyone worldwide!")
        print("💼 Professional Business Intelligence Platform")
        print("🎯 Top 20 Startup Opportunities with Tech Stacks")
        print("=" * 60)
        
        # Open in browser
        webbrowser.open(str(public_url))
        
        print("\n✅ Features Available:")
        print("   • Top 20 Business Opportunities")
        print("   • Complete Tech Stack Recommendations") 
        print("   • Revenue Projection Tools")
        print("   • Market Analysis Charts")
        print("   • Implementation Roadmaps")
        print("   • Professional Light Theme")
        
        print("\nPress Ctrl+C to stop the live dashboard")
        
        # Keep running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Stopping live dashboard...")
            ngrok.disconnect(public_url)
            print("✅ Dashboard stopped")
            
    except ImportError:
        print("❌ pyngrok not available. Dashboard running locally at:")
        print("🌐 http://localhost:8507")
        print("\nFor public access, install ngrok:")
        print("   brew install ngrok  # or")  
        print("   npm install -g ngrok")
        
        # Keep running locally
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Dashboard stopped")

if __name__ == "__main__":
    main()