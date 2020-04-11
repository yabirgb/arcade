import os
import yaml
from typing import Dict, List, Union
from definitions import required_folders


def generate_folder_structure(
    base_path: str, folders=required_folders
) -> None:
    """
    Create folder structure of arcade in the
    user folder structure
    """

    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    for folder in folders.values():
        create_folder(os.path.join(base_path, folder))

    # create index file
    with open(os.path.join(base_path, folders["content"], 'index.md'), 'w') as f:
        f.write("# Welcome to the arcade")

    


def create_config_file(
    base_path: str,
    name: str = "arcade.yaml",
) -> None:
    config = {
        "page_name": '',
        "base_path": '',
        "author_name": '',
        "theme": 'themes/baseline',
        "social": {
            "twitter": None,
            "github": None,
            "email": None,
            "mastodon": None,
            "linkedin": None,
        },
    }

    # Convert configuration to yaml format
    config_yaml = yaml.dump(config)

    # Write to disc the configuration file
    with open(os.path.join(base_path, name), "w") as f:
        f.write(config_yaml)
