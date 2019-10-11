from typing import List, Dict, Union
import os
import yaml


def list_content(base_folder:str, contents:str='contents') -> List[str]:
    
    path = os.path.join(base_folder, contents)


    contents = []
    
    for root, folders, files in os.walk(path):

        for filen in files:
            contents.append(os.paht.join(root, filen))

    return contents

def generate_folder_structure(base_path:str) -> None:
    """
    Create folder structure of arcade in the
    user folder structure
    """
    def create_folder(path):
        if not os.path.exists(path):
            os.makedirs(path)

    required_folders = ['contents', 'static', 'public']

    for folder in required_folders:
        create_folder(os.path.join(base_path, folder))

def create_config_file(base_path:str,
                       config:Dict[str, Union[Dict, str, int]
                       name:str='arcade.yaml') -> None:

    {
        page_name = config['page_name'],
        base_path = '',
        author_name = '',
        social = {
            twitter = None,
            github = None,
            email = None,
            mastodon = None,
            linkedin = None,
        }
        
    }
    
    # Convert configuration to yaml format
    config_yaml = yaml.dump(config)

    # Write to disc the configuration file
    with open(os.path.join(base_path,name), 'w') as f:
        f.write(config_yaml)
