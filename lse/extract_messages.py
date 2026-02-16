#!/usr/bin/env python3

import json
from pathlib import Path

from bs4 import BeautifulSoup

OUTPUT_FILE = "messages.json"

items = []

for page_num in range(1, 18):
    html_path = Path(f"{page_num}.html")
    if not html_path.exists():
        print(f"Skipping missing file: {html_path}")
        continue

    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    for message in soup.select("div.share-chat-message__message"):
        symbol = None
        posted_in = message.select_one("p.share-chat-message__details strong")
        if posted_in and posted_in.get_text(strip=True) == "Posted in:":
            link = posted_in.find_parent("p").find("a")
            if link:
                symbol = link.get_text(strip=True)
        else:
            link = message.select_one(
                "p.share-chat-message__details a.share-chat-message__link"
            )
            if link:
                symbol = link.get_text(strip=True)

        timestamp_tag = message.select_one(".share-chat-message__status-bar-time")
        timestamp = timestamp_tag.get_text(strip=True) if timestamp_tag else None

        message_tag = message.select_one("p.share-chat-message__message-text")
        message_html = None
        if message_tag:
            message_html = "".join(str(node) for node in message_tag.contents).strip()

        items.append(
            {
                "symbol": symbol,
                "timestamp": timestamp,
                "message": message_html,
            }
        )

Path(OUTPUT_FILE).write_text(json.dumps(items, indent=2), encoding="utf-8")
print(f"Saved {len(items)} messages to {OUTPUT_FILE}")
