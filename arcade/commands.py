import click
import os
from livereload import Server, shell
from create_artifacts import create_config_file, generate_folder_structure
from parsing import build_content, render_content, copy_static_assets
from utils import load_config_file

@click.command()
def init() -> None:
    click.echo("Preparing your machine")
    calling_path = os.getcwd()

    # create side effects
    generate_folder_structure(calling_path)
    create_config_file(calling_path)
    click.echo("Project created! Modify the arcade.yaml configuration file")


@click.command()
def build() -> None:
    base_path = os.getcwd()
    theme = load_config_file(base_path)['theme']
    content = build_content(base_path)
    render_content(base_path, content, theme)
    copy_static_assets(base_path, theme)

@click.command()
def watch() -> None:
    """
    Start a developing server for your content
    """

    # Get where the execution is being made
    base_path = os.getcwd()
    theme = load_config_file(base_path)['theme']
    
    content_folder = os.path.join(base_path, 'content')

    # Initialize the dev server
    server = Server()

    # Build content
    content = build_content(base_path)
    render_content(base_path, content, theme)
    copy_static_assets(base_path, theme)
    
    server.watch(content_folder, shell("python arcade/main.py build", cwd=base_path))
    server.serve(root="public")
