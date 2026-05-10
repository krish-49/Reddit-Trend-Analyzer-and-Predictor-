from fastapi import FastAPI
from pydantic import BaseModel
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import json
import os
import tempfile
from fastapi.middleware.cors import CORSMiddleware
import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
NOTEBOOK_PATH = r"C:\Users\krish\OneDrive\Desktop\RedditTrendPredictor\notebook\notebookb09ce3759c.ipynb"

class PredictRequest(BaseModel):
    title: str
    selftext: str
    hour: int
    dayofweek: str


def run_notebook(input_data: dict):
    with open(NOTEBOOK_PATH, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Inject INPUT_DATA + SAFE FALLBACK
    injected_code = f"""
INPUT_DATA = {json.dumps(input_data)}

# Safe access (prevents NameError)
title = INPUT_DATA.get("title", "Sample title")
selftext = INPUT_DATA.get("selftext", "Sample text")
hour = INPUT_DATA.get("hour", 12)
dayofweek = INPUT_DATA.get("dayofweek", "Monday")
"""

    nb.cells.insert(0, nbformat.v4.new_code_cell(injected_code))

    ep = ExecutePreprocessor(timeout=300, kernel_name="python3")

    with tempfile.TemporaryDirectory() as tmpdir:
        ep.preprocess(nb, {"metadata": {"path": tmpdir}})

    # Extract JSON output safely
    for cell in reversed(nb.cells):
        if cell.cell_type == "code":
            for out in cell.get("outputs", []):
                if "text" in out:
                    text_output = out["text"].strip()
                    try:
                        return json.loads(text_output)
                    except:
                        continue

    raise RuntimeError("Notebook did not return valid JSON output")


@app.post("/predict")
def predict(req: PredictRequest):
    result = run_notebook({
        "title": req.title,
        "selftext": req.selftext,
        "hour": req.hour,
        "dayofweek": req.dayofweek
    })
    return result
