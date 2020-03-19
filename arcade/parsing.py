import os
from typing import Dict, List, Tuple, Any
import markdown
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
from utils import list_content, copytree, load_config_file, Post
from definitions import required_folders
import shutil
import distutils.dir_util

def build_content(base_path: str) -> List[Post]:
    """
    Convert all the markdown files to html files. 
    Returns a list of:
    - destination file path
    - html transformed text
    - meta information
    """

    # Load markdown with the meta extension

    configuration = load_config_file(base_path)

    html_path = os.path.join(base_path, required_folders["public"])
    result = []

    # iterate over pairs file name and file path
    for filen, file_path in list_content(base_path, required_folders["content"]):
        # Open the file
        with open(file_path, "r") as f:
            # load markdown
            md = markdown.Markdown(extensions = ['meta', 'tables', 'sane_lists', 'attr_list'])
            # Read document
            data = f.read()
            # Convert markdown to html
            html = md.convert(data)

            # Get file extension
            filenn, extension = os.path.splitext(filen)

            # If it's not md skip file
            if extension != '.md':
                continue
            
            if 'index' in filen:
                result.append( Post(
                    path = os.path.join(html_path, "index.html"),
                    html = html,
                    meta = md.Meta,
                    config = configuration,
                    index = True
                )
                )
            else:
                if 'slug' in md.Meta.keys():
                    slug= md.Meta['slug'][0]
                else:
                    slug = filen.split(".")[0]

                md.Meta['slug'] = slug

                result.append( Post(
                    path = os.path.join(html_path, slug, "index.html"),
                    html = html,
                    meta = md.Meta,
                    config = configuration
                )
                )
    return result

def render_content(base_path:str,
                   data:List[Post],
                   template_folder:str) -> None:

    env = Environment()
    env.loader = FileSystemLoader(os.path.join(base_path, template_folder))

    index_folder = None
    index_config = dict()

    # Create the posts html files
    tmpl = env.get_template('post.html')

    for post in data:
        folder_path, filen = os.path.split(post.path)
        post_data = post.to_dict()

        if post.is_index:

            index_tmpl = env.get_template('index.html')
            
            # TODO: Overwrite this hardcoded constant
            get = min(len(data), 10)
            post_data['posts'] = [x.to_dict() for x in
                                  sorted([x for x in data if not x.is_index][:get], reverse=True) if not x.is_index]

            render = index_tmpl.render(post_data)
            
            index_folder = folder_path
            index_config = post.config
            
        else:
            render = tmpl.render(post_data)

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        with open(post.path, 'w') as f:
            f.write(render)

    # Create the history of posts

    history = env.get_template("full_list.html")
    content=dict()
    content['posts'] = list(map(lambda x: x.to_dict(), reversed([x for x in data if not x.is_index])))
    content['config'] = index_config
    render = history.render(content)

    if not os.path.exists(os.path.join(index_folder, 'history')):
        os.makedirs(os.path.join(index_folder, 'history'))

    with open(os.path.join(os.path.join(index_folder, 'history'), 'index.html'), 'w') as f:
        f.write(render)
        
def copy_static_assets(base_path, theme_folder):

    # copy files from theme folder
    dest = os.path.join(base_path, 'public', 'static')
    orig = os.path.join(base_path, theme_folder, 'static')
    if not os.path.exists(dest):
        os.makedirs(dest)
    else:
        pass
        #shutil.rmtree(dest)

    copytree(orig,dest)
    # copy files from static folder
    orig = os.path.join(base_path, 'static')
    distutils.dir_util.copy_tree(orig,dest)
    
        

