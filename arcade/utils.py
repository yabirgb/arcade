from datetime import datetime
from typing import List, Dict, Union, Tuple
import os

import yaml
from jinja2 import BaseLoader, TemplateNotFound

from definitions import required_folders
from errors import MissingArcadeProject



def list_content(base_folder: str, contents: str = "contents") -> List[Tuple[str, str]]:

    """
    List al the files in a folder given the base path and the folder name
    Returns pais of file name and file pathbu
    """

    path = os.path.join(base_folder, contents)

    contents = []

    for root, folders, files in os.walk(path):

        for filen in files:
            contents.append((filen, os.path.join(root, filen)))

    return contents


def check_arcade_project(path):
    """
    Check if the current folder is an arcade project
    """

    pass


class Post:

    def __init__(self, path, html, meta, index=False):

        self.path = path
        self.html = html
        self.meta = meta
        self.date_human = meta.get('date')[0]
        self.date = datetime.strptime(self.date_human,"%d-%m-%Y")
        self.is_index = index
        
    def to_dict(self):

        return {
            'post': self.html,
            'title': self.meta.get('title')[0],
            'created': self.date,
            'created_human': self.date_human,
            'slug': self.meta.get('slug'),
            'social': {}
        }
