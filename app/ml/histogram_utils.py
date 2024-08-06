import base64
import io

import numpy as np
import logging
import os
import torch
from PIL import Image
from torchvision import transforms

from app.config import Configuration
import cv2

conf = Configuration()

def calculate_histogram(image_id):
    # Here we extract and load the image from the specified image_id.
    image_path = os.path.join("app/static/imagenet_subset/", image_id)

    # Check if the image exists
    if not os.path.isfile(image_path):
        raise ValueError(f"Image path {image_path} does not exist")

    # Read the image thanks to the imread function from OpenCV
    image = cv2.imread(image_path)

    # Check if the image is correctly opened and not a NoneType
    if image is None:
        raise ValueError(f"Could not read image at {image_path}")

    # Split the image into its three channels: blue, green, and red
    chans = cv2.split(image)

    colors = ("blue", "green", "red")
    histo = []
    output = {}

    # Iterate over the channels and colors
    for (chan, color) in zip(chans, colors):
        hist_result = cv2.calcHist([chan], [0], None, [256], [0, 256])
        hist_result = [item[0] for item in hist_result]
        # Convert histogram to a simple list

        histo.append(hist_result)
        output[color] = hist_result
        # Use the first letter of each color as a key for the histogram
    return output