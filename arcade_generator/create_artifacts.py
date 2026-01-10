from __future__ import annotations

from pathlib import Path

from .definitions import required_folders


def generate_folder_structure(
    base_path: str | Path,
    folders: dict[str, str] = required_folders,
) -> None:
    """
    Create folder structure of arcade in the
    user folder structure
    """

    base = Path(base_path)

    def create_folder(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)

    for folder in folders.values():
        create_folder(base / folder)

    # create index file
    (base / folders["content"] / 'index.md').write_text("# Welcome to the arcade")

    


def create_config_file(
    base_path: str | Path,
    name: str = "arcade.toml",
) -> None:
    config_toml = "\n".join(
        [
            'page_name = ""',
            'base_path = ""',
            'author_name = ""',
            'theme = "themes/baseline"',
            "",
            "[social]",
            'email = { icon = "", url = "" }',
            'github = { icon = "", url = "" }',
            'linkedin = { icon = "", url = "" }',
            'mastodon = { icon = "", url = "" }',
            'twitter = { icon = "", url = "" }',
            "",
        ]
    )

    # Write to disc the configuration file
    (Path(base_path) / name).write_text(config_toml)
