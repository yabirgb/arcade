from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast
import xml.etree.ElementTree as ET
import markdown
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import shutil

from .utils import list_content, copytree, load_config_file, Post
from .definitions import required_folders

def build_content(base_path: str | Path) -> list[Post]:
    """
    Convert all the markdown files to html files. 
    Returns a list of:
    - destination file path
    - html transformed text
    - meta information
    """

    # Load markdown with the meta extension

    base = Path(base_path)
    configuration = load_config_file(base)

    html_path = base / required_folders["public"]
    posts_path = html_path / "posts"
    result = []

    # iterate over pairs file name and file path
    for filen, file_path in list_content(base, required_folders["content"]):
        # Open the file
        with file_path.open("r") as f:
            # load markdown
            md = markdown.Markdown(extensions=['meta', 'tables', 'sane_lists', 'attr_list'])
            # Read document
            data = f.read()
            # Convert markdown to html
            html = md.convert(data)
            meta = cast(dict[str, list[str]], getattr(md, "Meta", {}))

            # Get file extension
            extension = file_path.suffix

            # If it's not md skip file
            if extension != '.md':
                continue
            
            if 'index' in filen:
                result.append(
                    Post(
                        path=html_path / "index.html",
                        html=html,
                        meta=meta,
                        config=configuration,
                        index=True,
                    )
                )
            else:
                if slug_list := meta.get('slug'):
                    slug_value = slug_list[0]
                else:
                    slug_value = file_path.stem

                slug_path = slug_value.strip("/").split("/")[-1]
                slug_url = f"posts/{slug_path}"
                meta['slug'] = [slug_url]

                result.append(
                    Post(
                        path=posts_path / slug_path / "index.html",
                        html=html,
                        meta=meta,
                        config=configuration,
                    )
                )
    return result

def render_content(
    base_path: str | Path,
    data: list[Post],
    template_folder: str,
) -> None:

    base = Path(base_path)
    env = Environment()
    env.loader = FileSystemLoader(str(base / template_folder))

    index_folder: Path | None = None
    index_config = load_config_file(base)

    # Create the posts html files
    tmpl = env.get_template('post.html')

    for post in data:
        folder_path = post.path.parent
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

        folder_path.mkdir(parents=True, exist_ok=True)
        post.path.write_text(render)

    # Create the history of posts

    history = env.get_template("full_list.html")
    content=dict()
    content['posts'] = list(
        map(
            lambda x: x.to_dict(),
            sorted([x for x in data if not x.is_index], reverse=True))
    )

    content['config'] = index_config
    render = history.render(content)

    if index_folder is None:
        render_atom_feed(base, data, index_config)
        return

    history_folder = index_folder / 'history'
    history_folder.mkdir(parents=True, exist_ok=True)
    (history_folder / 'index.html').write_text(render)

    render_atom_feed(base, data, index_config)


def _atom_text(value: Any) -> str:
    if isinstance(value, list):
        return value[0] if value else ""
    return value or ""


def _atom_entry_id(base_url: str, slug: str) -> str:
    if base_url:
        return f"{base_url.rstrip('/')}/{slug.strip('/')}/"
    return f"urn:arcade:post:{slug}"


def render_atom_feed(base_path: str | Path, data: list[Post], config: dict[str, Any]) -> None:
    posts = [post for post in data if not post.is_index]
    if not posts:
        return

    base_url = _atom_text(config.get("base_path", ""))
    feed_title = _atom_text(config.get("page_name", "arcade"))
    now = datetime.now(timezone.utc)

    def post_date(post: Post) -> datetime:
        if post.date:
            return post.date.replace(tzinfo=timezone.utc)
        return now

    latest = max(post_date(post) for post in posts)

    feed = ET.Element("feed", attrib={"xmlns": "http://www.w3.org/2005/Atom"})
    ET.SubElement(feed, "title").text = feed_title
    ET.SubElement(feed, "id").text = base_url or "urn:arcade:feed"
    if base_url:
        ET.SubElement(feed, "link", attrib={"href": base_url})
        ET.SubElement(
            feed,
            "link",
            attrib={"href": f"{base_url.rstrip('/')}/atom.xml", "rel": "self"},
        )
    ET.SubElement(feed, "updated").text = latest.isoformat()

    for post in sorted(posts, reverse=True):
        slug = post.slug or "post"
        entry = ET.SubElement(feed, "entry")
        ET.SubElement(entry, "title").text = post.title or slug
        ET.SubElement(entry, "id").text = _atom_entry_id(base_url, slug)
        ET.SubElement(entry, "updated").text = post_date(post).isoformat()
        if base_url:
            ET.SubElement(entry, "link", attrib={"href": _atom_entry_id(base_url, slug)})
        ET.SubElement(entry, "content", attrib={"type": "html"}).text = post.html

    atom_path = Path(base_path) / required_folders["public"] / "posts" / "atom.xml"
    atom_path.parent.mkdir(parents=True, exist_ok=True)
    atom_path.write_bytes(ET.tostring(feed, encoding="utf-8", xml_declaration=True))
        
def copy_static_assets(base_path: str | Path, theme_folder: str) -> None:

    # copy files from theme folder
    base = Path(base_path)
    dest = base / 'public' / 'static'
    orig = base / theme_folder / 'static'
    dest.mkdir(parents=True, exist_ok=True)

    copytree(orig, dest)
    # copy files from static folder
    orig = base / 'static'
    if orig.exists():
        shutil.copytree(orig, dest, dirs_exist_ok=True)
    
        
