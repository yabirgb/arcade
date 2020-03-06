from datetime import datetime
from typing import List, Dict, Union, Tuple
import os
import shutil

import yaml
from jinja2 import BaseLoader, TemplateNotFound

from definitions import required_folders
from errors import MissingArcadeProject
import distutils.dir_util



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

    def __init__(self, path, html, meta, config={}, index=False):

        self.path = path
        self.html = html
        self.meta = meta
        self.date_human = meta.get('date')
        self.date = None

        if self.date_human:
            self.date_human = self.date_human[0]
            self.date = datetime.strptime(self.date_human,"%d-%m-%Y")

        if self.meta.get('title'):
            self.title = self.meta.get('title')[0]
        else:
            self.title = ''
            
        self.is_index = index
        self.config = config
        
    def to_dict(self):

        return {
            'post': self.html,
            'title': self.title,
            'created': self.date,
            'created_human': self.date_human,
            'slug': self.meta.get('slug'),
            'config': self.config
        }

    def __lt__(self, x):
        return self.date < x.date

    def __str__(self):
        return f'{self.title}'


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def load_config_file(base_path) -> Dict:
    """
    Load configuration for page creation
    """
    
    data = {}
    with open(os.path.join(base_path, 'arcade.yaml')) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)

    return data
