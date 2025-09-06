import modal

app = modal.App("startup-tracker-final")

# Minimal dependencies
image = (
    modal.Image.debian_slim()
    .pip_install("streamlit", "pandas", "numpy", "plotly", "requests", "aiohttp")
)

@app.function(
    image=image,
    mounts=[modal.Mount.from_local_file("dashboard.py", remote_path="/app/dashboard.py")],
    allow_concurrent_inputs=50
)
@modal.web_server(port=8000)
def serve():
    import subprocess
    import os
    os.chdir("/app")
    
    cmd = ["streamlit", "run", "dashboard.py", "--server.port", "8000", "--server.address", "0.0.0.0", "--server.headless", "true"]
    subprocess.run(cmd)

if __name__ == "__main__":
    app.serve()