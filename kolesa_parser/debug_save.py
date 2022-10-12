#!/usr/bin/env python3
from pathlib import Path


def debug_save(body, page_id):
    html_file = Path.cwd() / f"debug/{page_id}.html"
    with open(html_file, "wb") as html_file:
        html_file.write(body)
