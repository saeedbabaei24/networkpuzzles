
import json
import re
from pathlib import Path
from urllib.request import Request, urlopen

from markdownify import markdownify as md

API = "https://networkpuzzles.com/wp-json/wp/v2/posts"
OUTPUT = Path("blog")
OUTPUT.mkdir(exist_ok=True)


def fetch_posts():
    page = 1

    while True:
        url = f"{API}?per_page=100&page={page}&status=publish"
        req = Request(
            url,
            headers={"User-Agent": "NetworkPuzzles-Sync/1.0"}
        )

        with urlopen(req, timeout=30) as response:
            posts = json.load(response)

        if not posts:
            break

        yield from posts

        if len(posts) < 100:
            break

        page += 1


for post in fetch_posts():
    post_id = post["id"]
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", post["slug"])

    title = md(post["title"]["rendered"]).strip()
    content = md(
        post["content"]["rendered"],
        heading_style="ATX"
    ).strip()

    frontmatter = "\n".join([
        "---",
        f"wordpress_id: {post_id}",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {json.dumps(post['date'])}",
        f"url: {json.dumps(post['link'])}",
        "---",
        "",
        "",
    ])

    filename = OUTPUT / f"{post_id}-{slug}.md"

    filename.write_text(
        frontmatter + content + "\n",
        encoding="utf-8"
    )

    print(f"Synced: {filename}")
