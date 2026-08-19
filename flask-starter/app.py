import os
import sys
from pathlib import Path

from flask import Flask

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root / "logic"))
sys.path.insert(0, str(project_root / "routes"))

from routes.agent import agent_bp

app = Flask(__name__)
app.register_blueprint(agent_bp, url_prefix="/api")

@app.route("/")
def hello():
    return "Hello, Railway!"

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)