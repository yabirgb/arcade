from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Callable
import shutil
import logging

import tomllib

Config = dict[str, Any]
MetaData = dict[str, list[str]]
logger = logging.getLogger(__name__)


def list_content(base_folder: str | Path, contents: str = "contents") -> list[tuple[str, Path]]:

    """
    List al the files in a folder given the base path and the folder name
    Returns pais of file name and file pathbu
    """

    path = Path(base_folder) / contents

    contents: list[tuple[str, Path]] = []

    for item in path.rglob("*"):
        if item.is_file():
            contents.append((item.name, item))

    return contents


def check_arcade_project(path: str) -> None:
    """
    Check if the current folder is an arcade project
    """

    pass


class Post:

    def __init__(
        self,
        path: Path,
        html: str,
        meta: MetaData,
        config: Config | None = None,
        index: bool = False,
    ) -> None:

        self.path = path
        self.html = html
        self.meta = meta
        self.date_human: str | None = None
        self.date = None
        self.title = ''
        self.slug: str | None = None

        if date_list := meta.get('date'):
            self.date_human = date_list[0]
            self.date = datetime.strptime(self.date_human, "%d-%m-%Y")

        if title_list := self.meta.get('title'):
            self.title = title_list[0]

        if slug_list := self.meta.get('slug'):
            self.slug = slug_list[0]
            
        self.is_index = index
        self.config = config or {}
        
    def to_dict(self) -> dict[str, Any]:

        return {
            'post': self.html,
            'title': self.title,
            'created': self.date,
            'created_human': self.date_human,
            'slug': self.slug,
            'config': self.config
        }

    def __lt__(self, other: Post) -> bool:
        self_date = self.date or datetime.min
        other_date = other.date or datetime.min
        return self_date < other_date

    def __str__(self) -> str:
        return f'{self.title}'


def copytree(
    src: str | Path,
    dst: str | Path,
    symlinks: bool = False,
    ignore: Callable[[str, list[str]], list[str]] | None = None,
) -> None:
    src_path = Path(src)
    dst_path = Path(dst)
    for item in src_path.iterdir():
        s = src_path / item.name
        d = dst_path / item.name
        if s.is_dir():
            shutil.copytree(s, d, symlinks, ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

def load_config_file(base_path: str | Path) -> Config:
    """
    Load configuration for page creation
    """
    data: Config = {}
    config_path = Path(base_path) / 'arcade.toml'
    if cached := _CONFIG_CACHE.get(config_path):
        return cached

    with open(config_path, "rb") as f:
        data = tomllib.load(f)

    if data.get("social") is None:
        logger.warning("arcade.toml missing [social]; continuing with empty socials")
        data["social"] = {}

    _CONFIG_CACHE[config_path] = data
    return data


_CONFIG_CACHE: dict[Path, Config] = {}
