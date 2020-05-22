import cv2
import os
import json
from PIL import Image
import numpy as np


class UnsupportedImageFormatError(Exception):

    def __init__(self, *args):
        self.args = args

    def __str__(self):
        message = "UnsupportedImageFormatError has been raised"
        if self.args:
            return message + ": " + " ".join(self.args)
        else:
            return message


class Picture:

    with open("../src/extensions.json", "r") as f:
        supported_image_extensions = json.load(f)

    def __init__(self, filename):
        self.filename = filename
        self.format = None

    @staticmethod
    def get_image_reader(format):
        if format in Picture.supported_image_extensions["opencv-imread"]:
            return lambda filename: cv2.imread(filename)[:, :, ::-1]
        elif format in Picture.supported_image_extensions["PIL-Image-open"]:
            return lambda filename: np.array(Image.open(filename, 'r'))
        else:
            raise UnsupportedImageFormatError

    def __str__(self):
        return f'{self.filename}'

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.filename == other
        else:
            return self.filename == other.filename

    def __getattribute__(self, item):
        if item == 'format':
            if self.format is None:
                self.format = os.path.splitext(self.filename)[-1]

        return super(Picture, self).__getattribute__(item)

    def read(self, reader=None):
        if reader is None:
            reader = Picture.get_image_reader(self.format)
        return reader(self.filename)
