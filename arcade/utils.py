from typing import List, Dict, Union, Tuple
import os
import yaml
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
