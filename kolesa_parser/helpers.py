#!/usr/bin/env python3
from pathlib import Path
from scrapy.downloadermiddlewares.retry import get_retry_request
from scrapy.utils.project import get_project_settings


def debug_save(body, page_id):
    html_file = Path.cwd() / f"debug/{page_id}.html"
    with open(html_file, "wb") as html_file:
        html_file.write(body)


def get_desktop_retry_request(request, spider):
    DOMAIN_NAME = get_project_settings().get("DOMAIN_NAME")

    desktop_url = request.url.replace(f"m.{DOMAIN_NAME}", DOMAIN_NAME)

    desktop_retry_request = get_retry_request(
        request.replace(url=desktop_url),
        spider=spider,
        reason="redirected to mobile version",
    )

    return desktop_retry_request
