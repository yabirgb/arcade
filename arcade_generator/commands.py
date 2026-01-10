from __future__ import annotations

import click
from pathlib import Path
from typing import TYPE_CHECKING
from livereload import Server, shell
from .create_artifacts import create_config_file, generate_folder_structure
from .parsing import build_content, render_content, copy_static_assets
from .utils import load_config_file

if TYPE_CHECKING:
    from .utils import Post

@click.command()
def init() -> None:
    click.echo("Preparing your machine")
    calling_path = Path.cwd()

    # create side effects
    generate_folder_structure(calling_path)
    create_config_file(calling_path)

    click.echo("Project created! Modify the arcade.toml configuration file")
    click.echo("Don't forget to download a theme for your blog before starting. Visit https://github.com/yabirgb/arcade for more info")


@click.command()
def build() -> None:
    base_path = Path.cwd()
    theme: str = load_config_file(base_path)['theme']
    content: list[Post] = build_content(base_path)
    render_content(base_path, content, theme)
    copy_static_assets(base_path, theme)

@click.command()
def watch() -> None:
    """
    Start a developing server for your content
    """

    # Get where the execution is being made
    base_path = Path.cwd()
    theme: str = load_config_file(base_path)['theme']
    
    content_folder = base_path / 'content'
    theme_folder = base_path / 'themes'

    # Initialize the dev server
    server = Server()

    # Build content
    content: list[Post] = build_content(base_path)
    render_content(base_path, content, theme)
    copy_static_assets(base_path, theme)
    
    server.watch(str(content_folder / "**" / "*"), shell("arcade build", cwd=str(base_path)))
    server.watch(str(theme_folder / "**" / "*"), shell("arcade build", cwd=str(base_path)))
    server.serve(root="public")
