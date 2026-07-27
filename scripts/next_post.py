#!/usr/bin/env python3
"""next_post.py - determina qual e o proximo post da fila a publicar.

Logica robusta a atrasos:
1. Le instagram_posts.json (queue completa)
2. Consulta Graph API - ultimos 20 posts da conta
3. Compara caption prefix (60 chars) pra identificar quais posts do JSON ja foram publicados
4. Retorna o menor numero de post ainda nao publicado (ordem crescente)
5. Se todos ja foram publicados -> exit 2 (silent skip)
6. Se algum ja saiu HOJE (< 20h atras) -> exit 3 (rate-limit prudente, so 1/dia)

Exit codes:
  0 - proximo post identificado, retorna via GITHUB_OUTPUT ou stdout
  1 - erro fatal
  2 - fila vazia (todos publicados)
  3 - ja publicou hoje (skip, evita 2 posts no mesmo dia)

Usage:
  python3 scripts/next_post.py            # stdout apenas
  python3 scripts/next_post.py --gha      # tambem escreve em GITHUB_OUTPUT
  python3 scripts/next_post.py --allow-same-day  # permite publicar mesmo se ja saiu 1 hoje
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG = ROOT / "instagram_posts.json"
GRAPH = "https://graph.facebook.com/v21.0"
SIG_LEN = 60


def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def sig(caption: str) -> str:
    return (caption or "")[:SIG_LEN].strip()


def parse_ts(raw: str) -> datetime:
    raw = raw.replace("Z", "+00:00")
    if len(raw) >= 5 and raw[-5] in "+-" and raw[-3] != ":":
        raw = raw[:-2] + ":" + raw[-2:]
    return datetime.fromisoformat(raw)


def fetch_published(token: str, user_id: str, max_pages: int = 3) -> list[dict]:
    """Historico completo da conta com paginacao (ate max_pages * 100 = 300 posts)."""
    out = []
    url = f"{GRAPH}/{user_id}/media?fields=id,caption,timestamp&limit=100&access_token={urllib.parse.quote(token)}"
    for _ in range(max_pages):
        with urllib.request.urlopen(url, timeout=30) as r:
            resp = json.loads(r.read())
        data = resp.get("data", [])
        for p in data:
            out.append({"id": p["id"], "sig": sig(p.get("caption", "")), "ts": parse_ts(p["timestamp"])})
        next_url = resp.get("paging", {}).get("next")
        if not next_url:
            break
        url = next_url
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gha", action="store_true", help="escreve tambem em GITHUB_OUTPUT")
    parser.add_argument("--allow-same-day", action="store_true", help="permite publicar mesmo se ja saiu 1 hoje")
    parser.add_argument("--dry-run", action="store_true", help="so mostra qual seria, sem afetar exit codes de skip")
    args = parser.parse_args()

    load_env()
    token = os.environ.get("IG_ACCESS_TOKEN")
    user_id = os.environ.get("IG_USER_ID")
    if not (token and user_id):
        print("FATAL: IG_ACCESS_TOKEN ou IG_USER_ID ausente", file=sys.stderr)
        sys.exit(1)

    try:
        posts = json.loads(CONFIG.read_text())
    except Exception as e:
        print(f"FATAL: JSON invalido: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        published = fetch_published(token, user_id)
    except Exception as e:
        print(f"FATAL: Graph API falhou: {e}", file=sys.stderr)
        sys.exit(1)

    published_sigs = {p["sig"] for p in published}
    now = datetime.now(tz=timezone.utc)

    # Verifica se ja publicou algum post nas ultimas 20h
    if not args.allow_same_day and not args.dry_run:
        recent = [p for p in published if p["ts"] > now - timedelta(hours=20)]
        if recent:
            print(f"SKIP: ja publicou {len(recent)} post(s) nas ultimas 20h. Ultimo: {recent[0]['ts'].isoformat()}", file=sys.stderr)
            sys.exit(3)

    # Ordena JSON por 'number' ascendente, ignora posts com "skip": true
    for post in sorted(posts, key=lambda p: p["number"]):
        if post.get("skip"):
            continue
        s = sig(post.get("caption", ""))
        if s not in published_sigs:
            # Encontrou o proximo nao-publicado
            num = post["number"]
            title = post.get("title", "?")
            print(f"proximo post: {num} ({title})", file=sys.stderr)
            print(num)  # stdout limpo pra facil captura
            if args.gha and "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                    f.write(f"post_number={num}\n")
                    f.write(f"post_title={title}\n")
            sys.exit(0)

    # Se chegou aqui, todos ja foram publicados
    print("FILA VAZIA: todos os posts do JSON ja foram publicados", file=sys.stderr)
    sys.exit(2)


if __name__ == "__main__":
    main()
