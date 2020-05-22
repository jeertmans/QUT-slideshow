import os
import glob
import json
from pathlib import Path


class FilesManager:

    def __init__(self, pictures):

        self.pictures = pictures
        self.directories = set()

        for picture in self.pictures:
            directory = os.path.dirname(os.path.abspath(picture.filename))
            self.directories.add(directory)

    @staticmethod
    def get_src_directory():
        dirname = os.path.dirname(__file__)
        parent_directory = Path(dirname).parent

        return os.path.join(parent_directory, "src")

    @staticmethod
    def get_src_filename(filename):
        return os.path.join(FilesManager.get_src_directory(), filename)

    @staticmethod
    def get_all_supported_extensions():
        extensions = set()

        extensions_filename = FilesManager.get_src_filename("extensions.json")

        with open(extensions_filename, "r") as f:
            supported_image_extensions = json.load(f)

        for reader_extensions in supported_image_extensions.values():
            extensions.update(reader_extensions)

        return extensions

    @staticmethod
    def load_directory(directory, extensions=None, recursive=False):
        pathnames = []
        if extensions is None:
            extensions = FilesManager.get_all_supported_extensions()

        for extension in extensions:
            ext = f"*{extension}"
            path = os.path.join(directory, ext)
            pathnames.extend(glob.glob(path, recursive=recursive))

        return pathnames

