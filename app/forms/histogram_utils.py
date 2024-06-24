import os
import numpy as np
from PIL import Image
from matplotlib.figure import Figure # type: ignore
import matplotlib.pyplot as plt # type: ignore
from io import BytesIO
import base64

from app.config import Configuration

conf = Configuration()

def fetch_image(image_id):
    image_path = os.path.join(conf.image_folder_path, image_id)
    img = Image.open(image_path)
    return img

def calculate_histogram(image_id):
    img = fetch_image(image_id)
    img = img.convert("RGB")
    
    # Calculate histogram
    histogram = img.histogram()

    # Separate the histogram for R, G, B channels
    r_hist = histogram[0:256]
    g_hist = histogram[256:512]
    b_hist = histogram[512:768]

    return r_hist, g_hist, b_hist

def plot_histogram(r_hist, g_hist, b_hist):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(r_hist, color='red')
    axis.plot(g_hist, color='green')
    axis.plot(b_hist, color='blue')
    axis.set_title('Histogram')
    axis.set_xlabel('Pixel value')
    axis.set_ylabel('Frequency')

    buf = BytesIO()
    fig.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return img_base64
