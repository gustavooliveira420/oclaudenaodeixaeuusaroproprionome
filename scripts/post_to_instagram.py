#!/usr/bin/env python3
"""
Publica posts do @renegocia.tributario via Instagram Graph API.

Uso:
  python3 scripts/post_to_instagram.py            # dry-run de todos
  python3 scripts/post_to_instagram.py 1          # dry-run só do post 1
  python3 scripts/post_to_instagram.py 1 --publish   # publica o post 1
  python3 scripts/post_to_instagram.py --day 1 --publish  # publica os 3 do dia 1

Variáveis em scripts/.env (ver scripts/.env.example):
  IG_USER_ID            ID do IG Business Account
  IG_ACCESS_TOKEN       long-lived Page Access Token
  IG_IMAGE_BASE_URL     URL pública onde estão as pastas instagram-posts/post-N-.../
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

GRAPH = "https://graph.facebook.com/v21.0"
ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG = ROOT / "instagram_posts.json"


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        sys.exit(f"ERRO: variável {name} não definida (ver scripts/.env.example)")
    return value


def api_call(method: str, path: str, params: dict) -> dict:
    url = f"{GRAPH}/{path}"
    body = urllib.parse.urlencode({**params, "access_token": TOKEN}).encode()
    if method == "GET":
        url = f"{url}?{body.decode()}"
        req = urllib.request.Request(url, method="GET")
    else:
        req = urllib.request.Request(url, data=body, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        sys.exit(f"ERRO API ({e.code}) em {method} {path}: {e.read().decode()}")


def wait_until_ready(container_id: str, timeout: int = 180) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = api_call("GET", container_id, {"fields": "status_code"})
        status = data.get("status_code")
        if status == "FINISHED":
            return
        if status == "ERROR":
            sys.exit(f"ERRO: container {container_id} falhou no processamento")
        time.sleep(3)
    sys.exit(f"ERRO: container {container_id} não ficou pronto em {timeout}s")


def publish(post: dict, dry_run: bool) -> None:
    images = [f"{BASE_URL}/{post['folder']}/{img}" for img in post["images"]]
    label = f"Post {post['number']} — {post['title']}"

    if dry_run:
        print(f"[DRY-RUN] {label}")
        for img in images:
            print(f"  imagem: {img}")
        print(f"  caption ({len(post['caption'])} chars): {post['caption'][:120]}...")
        if post.get("pin"):
            print("  → marcar 'Fixar no perfil' manualmente após publicar")
        print()
        return

    print(f"→ Publicando {label}...")

    if len(images) == 1:
        res = api_call("POST", f"{IG_USER}/media", {
            "image_url": images[0],
            "caption": post["caption"],
        })
        container = res["id"]
    else:
        children = []
        for img in images:
            res = api_call("POST", f"{IG_USER}/media", {
                "image_url": img,
                "is_carousel_item": "true",
            })
            children.append(res["id"])
            wait_until_ready(res["id"])

        res = api_call("POST", f"{IG_USER}/media", {
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": post["caption"],
        })
        container = res["id"]

    wait_until_ready(container)
    res = api_call("POST", f"{IG_USER}/media_publish", {"creation_id": container})
    print(f"✅ {label} publicado — media_id={res['id']}")
    if post.get("pin"):
        print(f"   ⚠ ABRIR O APP E FIXAR ESSE POST NO TOPO DO PERFIL")
    print()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_number", type=int, nargs="?", help="número do post (1-9)")
    parser.add_argument("--day", type=int, choices=[1, 2, 3], help="publica todos do dia 1, 2 ou 3")
    parser.add_argument("--publish", action="store_true", help="publica de verdade (default: dry-run)")
    args = parser.parse_args()

    load_env()
    global TOKEN, IG_USER, BASE_URL
    TOKEN = require("IG_ACCESS_TOKEN")
    IG_USER = require("IG_USER_ID")
    BASE_URL = require("IG_IMAGE_BASE_URL").rstrip("/")

    posts = json.loads(CONFIG.read_text())

    if args.post_number:
        targets = [p for p in posts if p["number"] == args.post_number]
    elif args.day:
        targets = [p for p in posts if p["day"] == args.day]
    else:
        targets = posts

    if not targets:
        sys.exit("Nenhum post bate com o filtro.")

    for post in targets:
        publish(post, dry_run=not args.publish)


if __name__ == "__main__":
    main()
