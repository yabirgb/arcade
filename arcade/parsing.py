import os
from typing import Dict, List, Tuple, Any
import markdown
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from utils import list_content, Post
from definitions import required_folders


def build_content(base_path: str) -> List[Post]:
    """
    Convert all the markdown files to html files. 
    Returns a list of:
    - destination file path
    - html transformed text
    - meta information
    """

    # Load markdown with the meta extension

    html_path = os.path.join(base_path, required_folders["public"])
    result = []
    for filen, file_path in list_content(base_path, required_folders["content"]):
        with open(file_path, "r") as f:
            md = markdown.Markdown(extensions = ['meta', 'tables', 'sane_lists'])
            data = f.read()
            html = md.convert(data)
            
            if 'index' in filen:
                result.append( Post(
                    os.path.join(html_path, "index.html"),
                    html,
                    md.Meta,
                    True
                    )
                )
            else:
                if 'slug' in md.Meta.keys():
                    slug= md.Meta['slug'][0]
                else:
                    slug = filen.split(".")[0]

                md.Meta['slug'] = slug

                result.append( Post(
                    os.path.join(html_path, slug, "index.html"),
                    html,
                    md.Meta,
                    )
                )
    return result

def render_content(base_path:str,
                   data:List[Post],
                   template_folder:str) -> None:

    env = Environment()
    env.loader = FileSystemLoader(os.path.join(base_path, template_folder))

    # Create the posts html files
    tmpl = env.get_template('post.html')

    for post in data:
        folder_path, filen = os.path.split(post.path) 
        
        post_data = post.to_dict()

        if post.is_index:

            index_tmpl = env.get_template('index.html')
            
            # TODO: Overwrite this hardcoded constant
            get = min(len(data), 10)
            post_data['posts'] = [x.to_dict() for x in data[:get] if not x.is_index]

            render = index_tmpl.render(post_data)
            
        else:
            render = tmpl.render(post_data)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        with open(post.path, 'w') as f:
            f.write(render)

    # Create the history of posts

    # Create the index page
