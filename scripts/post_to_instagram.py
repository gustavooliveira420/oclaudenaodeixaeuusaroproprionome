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
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Optional

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


# Codigos de erro do Meta tratados como transitorios (vale retry):
#  - HTTP 5xx (backend Meta indisponivel)
#  - HTTP 429 (rate-limit)
#  - subcodigos 4, 17, 32, 613 (rate / temp lock)
#  - timeout
TRANSIENT_ERROR_CODES = {4, 17, 32, 613}
TRANSIENT_HTTP_CODES = {429, 500, 502, 503, 504}


class TransientAPIError(Exception):
    pass


class FatalAPIError(Exception):
    pass


def api_call(method: str, path: str, params: dict, retries: int = 3) -> dict:
    """Chama Graph API com retry exponencial em erros transitorios.

    Backoff: 30s -> 90s -> 180s (max).
    Erros fatais (token, payload, etc.) levantam FatalAPIError imediatamente.
    """
    url = f"{GRAPH}/{path}"
    body = urllib.parse.urlencode({**params, "access_token": TOKEN}).encode()
    if method == "GET":
        url_full = f"{url}?{body.decode()}"
        req = urllib.request.Request(url_full, method="GET")
    else:
        req = urllib.request.Request(url, data=body, method=method)

    attempt = 0
    last_exc: Optional[Exception] = None
    while attempt <= retries:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            payload = e.read().decode()
            try:
                err = json.loads(payload).get("error", {})
                code = err.get("code")
                sub = err.get("error_subcode")
            except json.JSONDecodeError:
                code, sub = None, None
            transient = (
                e.code in TRANSIENT_HTTP_CODES
                or code in TRANSIENT_ERROR_CODES
                or sub in TRANSIENT_ERROR_CODES
            )
            if transient and attempt <= retries:
                wait = 30 * (3 ** (attempt - 1))
                print(f"  [retry {attempt}/{retries}] erro transitorio HTTP {e.code} code={code} sub={sub} - aguardando {wait}s...")
                time.sleep(wait)
                last_exc = TransientAPIError(f"HTTP {e.code} code={code}: {payload[:200]}")
                continue
            raise FatalAPIError(f"API {method} {path} - HTTP {e.code}: {payload}") from e
        except (urllib.error.URLError, TimeoutError) as e:
            if attempt <= retries:
                wait = 30 * (3 ** (attempt - 1))
                print(f"  [retry {attempt}/{retries}] erro de rede ({e}) - aguardando {wait}s...")
                time.sleep(wait)
                last_exc = TransientAPIError(str(e))
                continue
            raise FatalAPIError(f"Rede falhou apos {retries} tentativas: {e}") from e
    raise FatalAPIError(f"Esgotou retries: {last_exc}")


def wait_until_ready(container_id: str, timeout: int = 180) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        data = api_call("GET", container_id, {"fields": "status_code"})
        status = data.get("status_code")
        if status == "FINISHED":
            return
        if status == "ERROR":
            raise FatalAPIError(f"container {container_id} falhou no processamento (status=ERROR)")
        time.sleep(3)
    raise FatalAPIError(f"container {container_id} nao ficou pronto em {timeout}s")


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
