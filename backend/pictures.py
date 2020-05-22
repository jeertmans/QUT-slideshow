import cv2
import os
import json
from PIL import Image as PILImage
import numpy as np
from backend.filesutility import FilesManager
import warnings


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
    extensions_filename = FilesManager.get_src_filename("extensions.json")

    with open(extensions_filename, "r") as f:
        supported_image_extensions = json.load(f)

    def __init__(self, filename):
        if not os.path.exists(filename):
            warnings.warn(f"{filename} does not exist!")

        self.filename = filename

    @staticmethod
    def get_image_reader(extension):
        if extension in Picture.supported_image_extensions["opencv-imread"]:
            return lambda filename: cv2.imread(filename)[:, :, ::-1]
        elif extension in Picture.supported_image_extensions["PIL-Image-open"]:
            return lambda filename: np.array(PILImage.open(filename, 'r'))
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
        if item == 'extension':
            return os.path.splitext(self.filename)[-1]
        else:
            return super(Picture, self).__getattribute__(item)

    def read(self, reader=None):
        if reader is None:
            reader = Picture.get_image_reader(self.extension)
        return reader(self.filename).view(ImageRGB)


class Image(np.ndarray):

    def get_corners(self):
        top = 0
        right = self.shape[1]
        bottom = self.shape[0]
        left = 0
        return top, right, bottom, left

    def resize(self, fx=.25, fy=.25):
        return cv2.resize(self, (0, 0), fx=fx, fy=fy).view(type(self))


class ImageRGB(Image):

    def asBGR(self):
        return self[:, :, ::-1].view(ImageBGR)

    def show(self, title='image'):
        return self.asBGR().show(title)

    def write(self, filename):
        self.asBGR().write(filename)

    def draw_named_rectangle(self, top, right, bottom, left, name, color_rect=(255, 0, 0), color_text=(255, 255, 255)):
        self.asBGR().draw_named_rectangle(top, right, bottom, left, name,
                                          color_rect=color_rect[::-1], color_text=color_text[::-1])


class ImageBGR(Image):

    def asRGB(self):
        return self[:, :, ::-1].view(ImageRGB)

    def show(self, title='image'):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)
        cv2.imshow(title, self)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        return key

    def write(self, filename):
        cv2.imwrite(filename, self)

    def draw_named_rectangle(self, top, right, bottom, left, name, color_rect=(0, 0, 255), color_text=(255, 255, 255)):
        # Draw a box
        cv2.rectangle(self, (left, top), (right, bottom), color_rect, 2)

        # Draw a label with a name below the rectangle
        cv2.rectangle(self, (left, bottom - 35), (right, bottom), color_rect, cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(self, name, (left + 6, bottom - 6), font, 1, color_text, 1)