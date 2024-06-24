import base64
import io
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import cv2 

from app.config import Configuration

conf = Configuration()

def calculate_histogram(image_path):
    # Nettoyer le chemin d'accès pour enlever les caractères indésirables
    image_path = image_path.replace('\n', '').replace('\r', '').strip()
    
    if not os.path.isfile(image_path):
        raise ValueError(f"Image path {image_path} does not exist")
    
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")
    
    chans = cv2.split(image)
    colors = ("b", "g", "r")
    features = []

    for (chan, color) in zip(chans, colors):
        hist = cv2.calcHist([chan], [0], None, [256], [0, 256])
        features.append(hist)

    return features

def plot_histogram(hist):
    plt.figure()
    plt.title("Color Histogram")
    plt.xlabel("Bins")
    plt.ylabel("# of Pixels")
    colors = ("b", "g", "r")

    for (h, color) in zip(hist, colors):
        plt.plot(h, color=color)
        plt.xlim([0, 256])

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')