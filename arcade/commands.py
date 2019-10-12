import click
import os
from livereload import Server, shell
from create_artifacts import create_config_file, generate_folder_structure
from parsing import build_content, render_content


theme = 'themes/baseline'

@click.command()
def init() -> None:
    click.echo("Preparing your machine")
    calling_path = os.getcwd()
    user_name = click.prompt("How should I call you?")
    project = click.prompt("What is the name of your project?")
    mini_config = {"page_name": project, "user_name": user_name}

    # create side effects
    generate_folder_structure(calling_path)
    create_config_file(calling_path, mini_config)


@click.command()
def build() -> None:
    base_path = os.getcwd()
    content = build_content(base_path)
    render_content(base_path, content, theme)


@click.command()
def watch(content_folder) -> None:
    """
    Start a developing server for your content
    """

    # Get where the execution is being made
    calling_path = os.getcwd()

    # Initialize the dev server
    server = Server()
    server.watch(content_folder, shell("arcade build", cwd=calling_path))
    server.serve(root="public")
