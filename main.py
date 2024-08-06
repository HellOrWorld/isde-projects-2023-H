import json
from typing import Dict, List

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

from app.config import Configuration
from app.forms.classification_form import ClassificationForm
from app.forms.histogram_form import HistogramForm
from app.ml.classification_utils import classify_image
from app.ml.histogram_utils import calculate_histogram
from app.utils import list_images

app = FastAPI()
config = Configuration()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


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
# This is the get request for the classification form
def create_classify(request: Request):
    return templates.TemplateResponse(
        "classification_select.html",
        {
            "request": request,
            "images": list_images(),
            "models": Configuration.models},
    )


@app.post("/classifications")
async def request_classification(request: Request):
    form = ClassificationForm(request)
    await form.load_data()
    # We retrieve the image id and model id from the form
    image_id = form.image_id
    model_id = form.model_id

    # We classify the image using the model
    classification_scores = classify_image(model_id=model_id, img_id=image_id)

    # We save the classification scores to the classification_scores.json file
    with open('app/static/classification_scores.json', 'w') as f:
        json.dump(classification_scores, f)

    # We return the classification_output.html template with the image_id and classification_scores
    return templates.TemplateResponse(
        "classification_output.html",
        {
            "request": request,
            "image_id": image_id,
            "classification_scores": json.dumps(classification_scores),
        },
    )


@app.get("/histogram")
# This is the get request for the histogram form
async def get_histogram_form(request: Request):
    return templates.TemplateResponse(
        "histogram_select.html",
        {
            "request": request,
            "images": list_images()
        }
    )


@app.post("/histogram")
# This is the post request for the histogram form
async def request_histogram(request: Request):
    form = HistogramForm(request)
    await form.load_data()
    # We retrieve the image id from the form
    image_id = form.image_id

    # We calculate the histogram scores for the image
    histogram_scores = calculate_histogram(image_id)

    # We save the histogram scores to the histogram_scores.txt file
    with open('app/static/histogram_scores.txt', 'w') as f:
        f.write(str(histogram_scores))

    # We return the histogram_output.html template with the image_id and histogram_scores
    return templates.TemplateResponse(
        "histogram_output.html",
        {
            "request": request,
            "image_id": image_id,
            "histogram_scores": histogram_scores,

        })


@app.get("/classifications_scores")
async def get_classification_scores(request: Request):
    return FileResponse('app/static/classification_scores.json')
# This is the api command for the txt downaload link for the classification scores as json file

@app.get("/histogram_scores_txt")
async def get_histogram_scores(request: Request):
    return FileResponse('app/static/histogram_scores.txt')
# This the api command for the txt downaload link for the histogram scores



