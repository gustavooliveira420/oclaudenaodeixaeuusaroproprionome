#!/usr/bin/env python3
"""
Pre-flight para publicacao IG. Roda ANTES de qualquer chamada de publish.

Falha rapido (sem consumir slot de API) se algo do basico estiver errado.

Usage:
  python3 scripts/preflight.py <post_number>
  python3 scripts/preflight.py --all-pending     # valida todos os posts do JSON

Exit codes:
  0 - tudo OK
  1 - erro fatal (token invalido, imagem 404, caption acima do limite, etc.)
  2 - aviso (token expira em < 30 dias, hashtag de auditoria ausente, etc.) - nao bloqueia
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG = ROOT / "instagram_posts.json"
GRAPH = "https://graph.facebook.com/v21.0"
CAPTION_MAX = 2200
AUDIT_HASHTAG_RE = re.compile(r"#rngc-\d{4}W\d{2}-\d", re.IGNORECASE)


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
    v = os.environ.get(name)
    if not v:
        print(f"FATAL: var {name} ausente do ambiente")
        sys.exit(1)
    return v


def http_get(url: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read())


def head_check(url: str, timeout: int = 15) -> tuple[bool, str]:
    """Tenta HEAD primeiro; alguns CDNs nao aceitam, fallback pra GET com Range."""
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code == 405:
            req = urllib.request.Request(url, method="GET", headers={"Range": "bytes=0-1023"})
            try:
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.status in (200, 206), f"HTTP {resp.status} (GET range)"
            except Exception as ee:
                return False, f"GET range falhou: {ee}"
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def check_token(token: str) -> tuple[bool, dict, list[str]]:
    """Valida token via debug_token. Retorna (ok, info, avisos)."""
    avisos: list[str] = []
    url = f"{GRAPH}/debug_token?{urllib.parse.urlencode({'input_token': token, 'access_token': token})}"
    try:
        data = http_get(url).get("data", {})
    except Exception as e:
        return False, {}, [f"debug_token falhou: {e}"]
    if not data.get("is_valid"):
        return False, data, [f"Token invalido: {data.get('error', {})}"]
    expires_at = data.get("expires_at", 0)
    if expires_at:
        days_left = (datetime.fromtimestamp(expires_at, tz=timezone.utc) - datetime.now(tz=timezone.utc)).days
        if days_left < 7:
            return False, data, [f"Token expira em {days_left} dias - CRITICO"]
        if days_left < 30:
            avisos.append(f"Token expira em {days_left} dias - renovar em breve")
    return True, data, avisos


def check_ig_user(token: str, user_id: str) -> tuple[bool, str]:
    """Tenta fields ricos (username, account_type); fallback pra 'id' so."""
    rich = f"{GRAPH}/{user_id}?fields=username,account_type&access_token={urllib.parse.quote(token)}"
    try:
        data = http_get(rich)
        if "error" in data:
            raise RuntimeError(str(data["error"]))
        return True, f"@{data.get('username', '?')} ({data.get('account_type', '?')})"
    except Exception:
        # fallback: confirmar so que o ID responde
        minimal = f"{GRAPH}/{user_id}/media?fields=id&limit=1&access_token={urllib.parse.quote(token)}"
        try:
            data = http_get(minimal)
            if "error" in data:
                return False, f"IG user invalido: {data['error']}"
            return True, f"IG user OK (minimal: {len(data.get('data', []))} media listadas)"
        except Exception as e:
            return False, f"GET IG user falhou (rico+minimal): {e}"


def validate_caption(caption: str) -> list[str]:
    erros = []
    if len(caption) > CAPTION_MAX:
        erros.append(f"caption {len(caption)} chars > limite {CAPTION_MAX}")
    if caption.count("@") > 5:
        erros.append(f"caption tem {caption.count('@')} mencoes @ - Meta pode bloquear (>20)")
    if caption.count("#") > 30:
        erros.append(f"caption tem {caption.count('#')} hashtags - limite IG 30")
    return erros


def validate_post(post: dict, base_url: str, token: str, user_id: str) -> tuple[bool, list[str], list[str]]:
    erros: list[str] = []
    avisos: list[str] = []
    label = f"Post {post.get('number')} - {post.get('title', '?')}"

    cap = post.get("caption", "")
    erros.extend(f"[{label}] {e}" for e in validate_caption(cap))
    if not AUDIT_HASHTAG_RE.search(cap):
        avisos.append(f"[{label}] sem hashtag de auditoria (#rngc-AAAAWNN-D) - idempotencia menos robusta")

    images = post.get("images", [])
    if not images:
        erros.append(f"[{label}] sem imagens no JSON")
    folder = post.get("folder", "")
    for img in images:
        url = f"{base_url.rstrip('/')}/{folder}/{img}"
        ok, detail = head_check(url)
        if not ok:
            erros.append(f"[{label}] imagem inacessivel: {url} -> {detail}")

    return len(erros) == 0, erros, avisos


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("post_number", type=int, nargs="?")
    parser.add_argument("--all-pending", action="store_true", help="valida todos do JSON")
    args = parser.parse_args()

    load_env()
    token = require("IG_ACCESS_TOKEN")
    user_id = require("IG_USER_ID")
    base_url = require("IG_IMAGE_BASE_URL").rstrip("/")

    erros: list[str] = []
    avisos: list[str] = []

    print("=== PRE-FLIGHT ===")
    print(f"timestamp UTC: {datetime.now(timezone.utc).isoformat()}")

    print("\n[1/4] Validando token Meta...")
    ok, info, w = check_token(token)
    avisos.extend(w)
    if not ok:
        erros.extend(w)
        print(f"  X token: {w}")
    else:
        print(f"  OK token (expires_at={info.get('expires_at', 0)})")

    print("\n[2/4] Validando IG user...")
    ok, detail = check_ig_user(token, user_id)
    if not ok:
        erros.append(detail)
        print(f"  X {detail}")
    else:
        print(f"  OK {detail}")

    print("\n[3/4] Validando instagram_posts.json...")
    try:
        posts = json.loads(CONFIG.read_text())
    except Exception as e:
        print(f"  X JSON invalido: {e}")
        sys.exit(1)
    print(f"  OK {len(posts)} posts no JSON")

    print("\n[4/4] Validando posts...")
    if args.all_pending:
        targets = posts
    elif args.post_number:
        targets = [p for p in posts if p["number"] == args.post_number]
        if not targets:
            print(f"  X post {args.post_number} nao existe no JSON")
            sys.exit(1)
    else:
        print("  (nada para validar - passe post_number ou --all-pending)")
        targets = []

    if erros:
        print("\n=== RESULTADO: FATAL ===")
        for e in erros:
            print(f"  X {e}")
        sys.exit(1)

    for p in targets:
        ok, e, w = validate_post(p, base_url, token, user_id)
        erros.extend(e)
        avisos.extend(w)
        label = f"post {p['number']}"
        print(f"  {'OK' if ok else 'X'} {label} ({len(p['images'])} img, {len(p['caption'])} chars)")
        for ee in e:
            print(f"     X {ee}")

    print("\n=== RESULTADO ===")
    if erros:
        print(f"FATAL - {len(erros)} erro(s):")
        for e in erros:
            print(f"  X {e}")
        sys.exit(1)
    if avisos:
        print(f"AVISO - {len(avisos)} aviso(s):")
        for w in avisos:
            print(f"  ! {w}")
        sys.exit(2)
    print("OK - tudo pronto pra publicar")
    sys.exit(0)


if __name__ == "__main__":
    main()
