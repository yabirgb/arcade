import os
from markdown import markdown

from utils import list_content
from definitions import required_folders


def build_content(base_path: str) -> None:
    """
    Convert all the markdown files to html files. 
    This function has side effects on disk creating
    htmls files inside the public folder
    """

    html_path = os.path.join(base_path, required_folders["public"])

    for filen, file_path in list_content(base_path, required_folders["content"]):
        with open(file_path, "r") as f:
            data = f.read()
            html = markdown(data)

            with open(os.path.join(html_path, filen.split(".")[0] + ".html"), "w") as f:
                f.write(html)
