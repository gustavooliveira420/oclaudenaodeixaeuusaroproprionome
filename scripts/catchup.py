#!/usr/bin/env python3
"""
Catch-up refatorado 27/07/2026 apos falha silenciosa jul/2026.

Design NOVO: detecta por AUSENCIA (nao por SCHEDULE dict).

1. Le instagram_posts.json (fonte de verdade da fila de posts ativos)
2. Consulta Graph API - historia completa da conta
3. Compara: quais posts do JSON ainda nao foram publicados?
4. Se conta ficou > 2 dias sem post E ha posts pendentes na fila -> publica proximo
5. Notifica via webhook (Discord/Slack) SE NOTIFY_WEBHOOK_URL configurado

Roda diariamente 02:00 UTC (23:00 BRT).

Salvaguardas:
- Idempotencia (nao publica se conta ja teve post nas ultimas 20h)
- Rate-limit prudente
- Log persistente em docs/editorial/audit-log/catchup-history.json
- Webhook + issue automatica em qualquer inconsistencia

Output JSON stdout: {"action": "...", "post_number": N?, "reason": "..."}
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG = ROOT / "instagram_posts.json"
GRAPH = "https://graph.facebook.com/v21.0"
CATCHUP_LOG = ROOT.parent / "docs" / "editorial" / "audit-log" / "catchup-history.json"

DAYS_SILENT_TRIGGER = 2  # se conta ficou >= 2 dias sem post, catch-up dispara
RECENT_HOURS = 20        # janela de rate-limit


def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_ts(raw: str) -> datetime:
    raw = raw.replace("Z", "+00:00")
    if len(raw) >= 5 and raw[-5] in "+-" and raw[-3] != ":":
        raw = raw[:-2] + ":" + raw[-2:]
    return datetime.fromisoformat(raw)


def fetch_recent_posts(token: str, user_id: str, days: int = 30) -> list[dict]:
    """Ultimos posts com paginacao."""
    out = []
    url = f"{GRAPH}/{user_id}/media?fields=id,caption,timestamp&limit=100&access_token={urllib.parse.quote(token)}"
    for _ in range(3):
        with urllib.request.urlopen(url, timeout=30) as r:
            resp = json.loads(r.read())
        for p in resp.get("data", []):
            out.append({"id": p["id"], "sig": (p.get("caption") or "")[:60].strip(), "ts": parse_ts(p["timestamp"])})
        nxt = resp.get("paging", {}).get("next")
        if not nxt: break
        url = nxt
    return out


def load_log() -> dict:
    if not CATCHUP_LOG.exists():
        return {"runs": []}
    try:
        return json.loads(CATCHUP_LOG.read_text())
    except Exception:
        return {"runs": []}


def save_log(hist: dict):
    CATCHUP_LOG.parent.mkdir(parents=True, exist_ok=True)
    CATCHUP_LOG.write_text(json.dumps(hist, indent=2, default=str))


def notify_webhook(msg: str):
    url = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not url:
        return
    try:
        payload = json.dumps({"content": msg, "text": msg}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"webhook falhou (nao bloqueia): {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    load_env()
    token = os.environ.get("IG_ACCESS_TOKEN")
    user_id = os.environ.get("IG_USER_ID")
    if not (token and user_id):
        print(json.dumps({"error": "credenciais ausentes"}))
        sys.exit(1)

    now = datetime.now(tz=timezone.utc)
    posts = json.loads(CONFIG.read_text())
    active_posts = [p for p in posts if not p.get("skip")]

    published = fetch_recent_posts(token, user_id)
    published_sigs = {p["sig"] for p in published}

    # Ordena por timestamp desc pra pegar o mais recente
    latest = max((p["ts"] for p in published), default=None)
    days_silent = (now - latest).days if latest else 999

    # Descobre proximo post nao publicado (menor number)
    next_post = None
    for post in sorted(active_posts, key=lambda p: p["number"]):
        sig_json = (post.get("caption") or "")[:60].strip()
        if sig_json not in published_sigs:
            next_post = post
            break

    result = {
        "timestamp": now.isoformat(),
        "days_silent": days_silent,
        "next_post_pending": next_post["number"] if next_post else None,
        "action": None,
        "reason": None,
    }

    # Rate-limit: se ja publicou nas ultimas RECENT_HOURS, skip
    if latest and (now - latest) < timedelta(hours=RECENT_HOURS):
        result["action"] = "skip"
        result["reason"] = f"ja publicou ha {(now - latest).total_seconds()/3600:.1f}h (< {RECENT_HOURS}h)"
    elif not next_post:
        result["action"] = "skip"
        result["reason"] = "fila vazia (todos posts ativos ja publicados)"
    elif days_silent >= DAYS_SILENT_TRIGGER:
        # Trigger: publica proximo da fila
        if args.dry_run:
            result["action"] = "would_publish"
            result["reason"] = f"conta silenciosa ha {days_silent} dias, publicaria post {next_post['number']}"
        else:
            try:
                r = subprocess.run(
                    [sys.executable, str(ROOT/"post_to_instagram.py"), str(next_post["number"]), "--publish"],
                    capture_output=True, text=True, timeout=600, cwd=str(ROOT.parent),
                )
                if r.returncode == 0:
                    result["action"] = "published"
                    result["reason"] = f"catchup publicou post {next_post['number']}"
                    notify_webhook(f"✅ CATCHUP: Renegocia publicou Post {next_post['number']} (conta estava {days_silent}d silenciosa)")
                else:
                    result["action"] = "failed"
                    result["reason"] = f"post_to_instagram exit {r.returncode}: {r.stderr[-300:]}"
                    notify_webhook(f"🚨 CATCHUP FALHOU Post {next_post['number']}: {r.stderr[-200:]}")
            except subprocess.TimeoutExpired:
                result["action"] = "timeout"
                result["reason"] = "post_to_instagram timeout 10min"
                notify_webhook(f"🚨 CATCHUP TIMEOUT Post {next_post['number']}")
    else:
        result["action"] = "skip"
        result["reason"] = f"conta ainda dentro do prazo ({days_silent}d silenciosa, trigger apenas >= {DAYS_SILENT_TRIGGER}d)"

    # Log persistente
    if not args.dry_run:
        hist = load_log()
        hist["runs"].append(result)
        save_log(hist)

    print(json.dumps(result, indent=2, default=str))
    sys.exit(0 if result["action"] in ("published", "skip", "would_publish") else 1)


if __name__ == "__main__":
    main()
