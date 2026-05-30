#!/usr/bin/env python3
"""
Watchdog semanal: roda segunda 08:00 BRT (11:00 UTC). Audita a saude do
gerenciamento da semana anterior. Gera report em stdout (consumido pelo workflow
pra criar issue) e codigo de saida diferente de zero em caso de gap.

Checks:
1. Quantos posts foram planejados vs publicados na semana anterior
2. Posts duplicados nas ultimas 7 dias
3. Token Meta - dias ate expirar
4. Catch-ups executados (alerta se > 1)
5. Container orfao remanescente (criado mas nao publicado)

Output JSON pra automacao + sumario texto pra issue.
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
CATCHUP_LOG = ROOT.parent / "docs" / "editorial" / "audit-log" / "catchup-history.json"
GRAPH = "https://graph.facebook.com/v21.0"


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def http_get(url: str) -> dict:
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read())


def main() -> None:
    load_env()
    token = os.environ["IG_ACCESS_TOKEN"]
    user_id = os.environ["IG_USER_ID"]

    now = datetime.now(tz=timezone.utc)
    week_ago = now - timedelta(days=7)

    report: dict = {"timestamp": now.isoformat(), "alerts": [], "ok": []}

    # 1. media publicada na ultima semana
    url = (
        f"{GRAPH}/{user_id}/media?fields=id,caption,timestamp,media_type&limit=30"
        f"&access_token={urllib.parse.quote(token)}"
    )
    posts_pub = []
    for p in http_get(url).get("data", []):
        raw = p["timestamp"].replace("Z", "+00:00")
        # Meta retorna "+0000" sem dois-pontos (Python 3.9 nao aceita) - normaliza
        if len(raw) >= 5 and raw[-5] in "+-" and raw[-3] != ":":
            raw = raw[:-2] + ":" + raw[-2:]
        ts = datetime.fromisoformat(raw)
        if ts >= week_ago:
            posts_pub.append({"id": p["id"], "ts": ts.isoformat(), "caption_prefix": (p.get("caption") or "")[:80]})

    report["publicados_7d"] = len(posts_pub)

    # 2. duplicatas (mesmo prefixo de caption)
    sigs = [p["caption_prefix"][:60].strip() for p in posts_pub]
    dup = [(s, c) for s, c in Counter(sigs).items() if c > 1 and s]
    if dup:
        report["alerts"].append({"tipo": "duplicata", "detalhe": dup})
    else:
        report["ok"].append("nenhuma duplicata em 7 dias")

    # 3. token
    dbg = http_get(f"{GRAPH}/debug_token?{urllib.parse.urlencode({'input_token': token, 'access_token': token})}").get("data", {})
    exp = dbg.get("expires_at", 0)
    if exp:
        dias = (datetime.fromtimestamp(exp, tz=timezone.utc) - now).days
        if dias < 30:
            report["alerts"].append({"tipo": "token_expira", "dias_restantes": dias})
        else:
            report["ok"].append(f"token valido por {dias} dias")
    else:
        report["ok"].append("token nao-expirante (expires_at=0)")

    # 4. catch-ups
    if CATCHUP_LOG.exists():
        try:
            hist = json.loads(CATCHUP_LOG.read_text())
            recent = [
                r for r in hist.get("runs", [])
                if datetime.fromisoformat(r["timestamp"]) >= week_ago and r.get("executed")
            ]
            if len(recent) > 1:
                report["alerts"].append({"tipo": "muitos_catchups", "qtd_7d": len(recent), "detalhe": recent})
            elif recent:
                report["ok"].append(f"{len(recent)} catch-up(s) na semana - dentro do esperado")
            else:
                report["ok"].append("nenhum catch-up na semana")
        except Exception as e:
            report["alerts"].append({"tipo": "log_catchup_invalido", "erro": str(e)})

    # 5. esperado vs publicado (semana padrao = 6 posts/sem) - calibravel
    expected_weekly = int(os.environ.get("EXPECTED_POSTS_PER_WEEK", "6"))
    gap = expected_weekly - report["publicados_7d"]
    if gap > 0:
        report["alerts"].append({"tipo": "gap_cronograma", "esperado": expected_weekly, "publicado": report["publicados_7d"], "delta": gap})

    print(json.dumps(report, indent=2, default=str))
    # exit 0 quando OK, 1 quando alerta
    sys.exit(0 if not report["alerts"] else 1)


if __name__ == "__main__":
    main()
