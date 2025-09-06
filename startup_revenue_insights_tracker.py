import modal
import subprocess
import os

# Create Modal app following vyuduinc workspace pattern
app = modal.App("startup-revenue-insights-tracker")

# Image with required dependencies (matching your other apps)
image = modal.Image.debian_slim(python_version="3.11").pip_install(
    "streamlit==1.49.1",
    "pandas==2.3.2", 
    "numpy==2.3.2",
    "plotly==6.3.0",
    "requests==2.32.5",
    "aiohttp==3.12.15"
)

# Mount the dashboard file
dashboard_mount = modal.Mount.from_local_file(
    "dashboard.py",
    remote_path="/root/dashboard.py"
)

# Streamlit config mount
config_mount = modal.Mount.from_local_file(
    ".streamlit/config.toml",
    remote_path="/root/.streamlit/config.toml"
)

@app.function(
    image=image,
    mounts=[dashboard_mount, config_mount],
    allow_concurrent_inputs=1000,
    memory=1024
)
@modal.web_server(8000, startup_timeout=120)
def run():
    """
    Startup Revenue Insights Tracker
    Professional Business Intelligence Platform - Top 20 Startup Opportunities
    """
    import time
    
    # Change to root directory
    os.chdir("/root")
    
    # Start Streamlit server (non-blocking)
    cmd = [
        "streamlit", "run", "dashboard.py",
        "--server.port", "8000",
        "--server.address", "0.0.0.0", 
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    # Use Popen instead of run to avoid blocking
    process = subprocess.Popen(cmd)
    
    # Keep the function alive
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        process.terminate()

if __name__ == "__main__":
    # For local testing
    app.serve()