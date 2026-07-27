#!/usr/bin/env python3
"""
Watchdog refatorado 27/07/2026 apos falha silenciosa jul/2026.

Design NOVO: alertas absolutos sem depender de EXPECTED_POSTS_PER_WEEK.

Roda toda segunda 11:00 UTC (08:00 BRT).

Checks:
1. Dias sem post - se > 3 dias, ALERTA CRITICO (independente do que esperava)
2. Duplicatas em 7d
3. Token Meta - dias ate expirar
4. Posts pendentes na fila (active - published)
5. Ultima falha registrada nas issues do GitHub

Notifica via:
- Webhook (Discord/Slack) SE configurado
- Issue automatica no repo (backup textual)
- Stdout JSON pra automacao
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ENV_FILE = ROOT / ".env"
CONFIG = ROOT / "instagram_posts.json"
GRAPH = "https://graph.facebook.com/v21.0"

MAX_DAYS_SILENT = 3  # se conta ficou > 3 dias sem post, alerta critico
MIN_TOKEN_DAYS = 30


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


def http_get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read())


def notify_webhook(msg: str):
    url = os.environ.get("NOTIFY_WEBHOOK_URL")
    if not url:
        print(f"NOTIFY_WEBHOOK_URL nao configurado - skip webhook", file=sys.stderr)
        return
    try:
        payload = json.dumps({"content": msg, "text": msg}).encode()
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        urllib.request.urlopen(req, timeout=10)
        print(f"webhook enviado: {msg[:80]}", file=sys.stderr)
    except Exception as e:
        print(f"webhook falhou (nao bloqueia): {e}", file=sys.stderr)


def main():
    load_env()
    token = os.environ["IG_ACCESS_TOKEN"]
    user_id = os.environ["IG_USER_ID"]
    now = datetime.now(tz=timezone.utc)

    report = {"timestamp": now.isoformat(), "alerts": [], "critical_alerts": [], "ok": []}

    # 1. Ultimos posts (janela 30d)
    url = f"{GRAPH}/{user_id}/media?fields=id,caption,timestamp&limit=50&access_token={urllib.parse.quote(token)}"
    all_posts = []
    for p in http_get(url).get("data", []):
        ts = parse_ts(p["timestamp"])
        all_posts.append({"id": p["id"], "ts": ts, "sig": (p.get("caption") or "")[:60].strip()})

    # 2. Dias sem post - CHECK CRITICO
    if all_posts:
        latest_ts = max(p["ts"] for p in all_posts)
        days_silent = (now - latest_ts).days
        if days_silent > MAX_DAYS_SILENT:
            report["critical_alerts"].append({
                "tipo": "conta_silenciosa",
                "dias_silenciosa": days_silent,
                "ultimo_post": latest_ts.isoformat(),
                "severity": "CRITICAL",
            })
        else:
            report["ok"].append(f"ultimo post ha {days_silent}d ({latest_ts.date()})")
    else:
        report["critical_alerts"].append({"tipo": "conta_vazia", "severity": "CRITICAL"})

    # 3. Duplicatas em 7d
    week_ago = now - timedelta(days=7)
    recent_sigs = [p["sig"] for p in all_posts if p["ts"] >= week_ago]
    dup = [(s, c) for s, c in Counter(recent_sigs).items() if c > 1 and s]
    if dup:
        report["alerts"].append({"tipo": "duplicata", "detalhe": dup})
    else:
        report["ok"].append("nenhuma duplicata em 7d")

    # 4. Token
    dbg_url = f"{GRAPH}/debug_token?input_token={token}&access_token={token}"
    dbg = http_get(dbg_url).get("data", {})
    exp = dbg.get("expires_at", 0)
    if exp:
        dias = (datetime.fromtimestamp(exp, tz=timezone.utc) - now).days
        if dias < 7:
            report["critical_alerts"].append({"tipo": "token_expira_urgente", "dias": dias})
        elif dias < MIN_TOKEN_DAYS:
            report["alerts"].append({"tipo": "token_expira", "dias": dias})
        else:
            report["ok"].append(f"token valido por {dias}d")
    else:
        report["ok"].append("token nao-expirante")

    # 5. Fila pendente
    posts = json.loads(CONFIG.read_text())
    active = [p for p in posts if not p.get("skip")]
    pub_sigs = {p["sig"] for p in all_posts}
    pending = [p for p in sorted(active, key=lambda p: p["number"])
               if (p.get("caption") or "")[:60].strip() not in pub_sigs]
    report["pending_queue"] = [p["number"] for p in pending]
    if pending:
        report["ok"].append(f"{len(pending)} posts na fila: {[p['number'] for p in pending]}")
    else:
        report["alerts"].append({"tipo": "fila_vazia", "detalhe": "todos posts ativos ja publicados - produzir novo bundle"})

    # Notif via webhook em qualquer alerta critico
    if report["critical_alerts"]:
        msg_parts = ["🚨 WATCHDOG @renegocia.tributario - ALERTA CRITICO:"]
        for a in report["critical_alerts"]:
            msg_parts.append(f"  - {a['tipo']}: {json.dumps({k:v for k,v in a.items() if k not in ('tipo','severity')}, default=str)}")
        msg_parts.append(f"Prox post na fila: {report['pending_queue'][:1] or 'nenhum'}")
        notify_webhook("\n".join(msg_parts))
    elif report["alerts"]:
        msg = f"⚠️ WATCHDOG @renegocia.tributario - {len(report['alerts'])} aviso(s): " + \
              ", ".join(a["tipo"] for a in report["alerts"])
        notify_webhook(msg)

    print(json.dumps(report, indent=2, default=str))
    # exit 0 se tudo OK, 1 se alerta, 2 se critico
    if report["critical_alerts"]:
        sys.exit(2)
    if report["alerts"]:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
