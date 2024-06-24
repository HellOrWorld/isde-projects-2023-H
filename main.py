import base64
from io import BytesIO
import io
import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import cv2
from uuid import uuid4
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.forms.histogram_form import HistogramForm
from app.ml.classification_utils import classify_image
from app.ml.histogram_utils import calculate_histogram, plot_histogram # type: ignore
from app.utils import list_images



app = FastAPI()
config = Configuration()

templates = Jinja2Templates(directory="app/templates")

os.makedirs("app/static/histograms", exist_ok = True)


@app.get("/info")
def info() -> Dict[str, List[str]]:
    """Returns a dictionary with the list of models and
    the list of available image files."""
    list_of_images = list_images()
    list_of_models = Configuration.models
    data = {"models": list_of_models, "images": list_of_images}
    return data



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """The home page of the service."""
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/classifications")
def create_classify(request: Request):
    return templates.TemplateResponse(
        "classification_select.html",
        {"request": request, "images": list_images(), "models": Configuration.models},
    )


@app.get("/histogram")
def create_histogram(request: Request):
    return templates.TemplateResponse(
        "histogram_select.html", {"request": request, "images": list_images()}
    )


@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    image_id = form.image_id
    model_id = form.model_id
    classification_scores = classify_image(model_id=model_id, img_id=image_id)
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )

@app.get("/histogram", response_class=HTMLResponse)
async def get_histogram_form(request: Request):
    images = os.listdir('static/imagenet_subset')
    return templates.TemplateResponse("histogram_select.html", {
        "request": request,
        "images": images
    })

@app.post("/histogram", response_class=HTMLResponse)
async def request_histogram(request: Request, image_id: str = Form(...)):
    # Supprimez les caractères indésirables du chemin d'accès à l'image
    image_id = image_id.strip()
    img_path = os.path.join('static', 'imagenet_subset', image_id)
    print(f"Debug: Image path - {img_path}")
    
    hist = calculate_histogram(img_path)
    hist_image = plot_histogram(hist)
    
    return templates.TemplateResponse("histogram_output.html", {
        "request": request,
        "image_id": image_id,
        "histogram_image": hist_image
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)