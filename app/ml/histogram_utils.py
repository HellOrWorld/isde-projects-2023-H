import base64
import io
import os
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.figure import Figure
import importlib
import json
import logging
import os
import torch
from PIL import Image
from torchvision import transforms

from app.config import Configuration
import cv2 

from app.config import Configuration

conf = Configuration()


def calculate_histogram(image_id):
    image_path = os.path.join("app/static/imagenet_subset/", image_id)

    if not os.path.isfile(image_path):
        raise ValueError(f"Image path {image_path} does not exist")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")

    chans = cv2.split(image)
    colors = ("blue", "green", "red")
    histo = []

    output={}


    for (chan, color) in zip(chans, colors):
        hist_result = cv2.calcHist([chan], [0], None, [256], [0, 256])
        hist_result = [item[0] for item in hist_result]  # Convert histogram to a simple list
        histo.append(hist_result)
        output[color] = hist_result
        # Use the first letter of each color as a key

    return output

