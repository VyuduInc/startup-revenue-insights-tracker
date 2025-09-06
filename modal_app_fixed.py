import modal
import subprocess
import time
import os

app = modal.App("startup-insights-fixed")

# Simpler image setup
image = modal.Image.debian_slim().pip_install(
    "streamlit",
    "pandas", 
    "numpy",
    "plotly"
)

# Mount the dashboard
dashboard_mount = modal.Mount.from_local_file(
    "dashboard.py",
    remote_path="/app/dashboard.py"
)

@app.function(
    image=image,
    mounts=[dashboard_mount],
    allow_concurrent_inputs=100
)
@modal.web_server(8000, startup_timeout=300)
def web():
    os.chdir("/app")
    
    # Start streamlit in background
    proc = subprocess.Popen([
        "streamlit", "run", "dashboard.py",
        "--server.port=8000",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--server.enableCORS=false"
    ])
    
    # Keep running
    proc.wait()

if __name__ == "__main__":
    app.serve()