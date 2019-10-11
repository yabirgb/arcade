import click
from livereload import Server, shell
from utils import create_config_file, generate_folder_structure, generate_html


def init():
    click.echo("Preparing your machine")
    calling_path = os.getcwd()
    user_name = click.prompt("How should I call you?")
    project = click.prompt("What is the name of your project?")
    mini_config = {"page_name": project, "user_name": user_name}

    # create side effects
    generate_folder_structure(calling_path)
    create_config_file(calling_path, mini_config)


def build():
    pass


def watch(content_folder):
    server = Server()
    server.watch(content_folder, shell("arcade build"))
    server.serve(root="public")
