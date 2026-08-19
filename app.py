import sys
from pathlib import Path

from flask import Flask, render_template

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root / "logic"))
sys.path.insert(0, str(project_root / "routes"))

from routes.agent import agent_bp

app = Flask(__name__, template_folder=str(project_root / "flask-starter" / "templates"))
app.register_blueprint(agent_bp, url_prefix="/api")


@app.get("/")
@app.get("/plan_trip")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"status": "ok"}