#!/usr/bin/env python3
"""
Catch-up automatico: detecta posts que deveriam ter saido hoje mas nao sairam,
e publica como recuperacao. Roda diariamente 23:00 BRT (02:00 UTC).

Logica:
1. Carrega cronograma esperado do dia (instagram_posts.json + tabela de cron)
2. Lista posts realmente publicados nas ultimas 24h via Graph API
3. Compara: quais posts esperados hoje nao apareceram no IG?
4. Para cada gap: publica via post_to_instagram.py (com retry, pre-flight, etc.)
5. Salvaguardas:
   - Max 2 catch-ups por janela de 7 dias (evita inundacao)
   - Catch-up so re-tenta posts < 48h de atraso (alem disso, esquecer + alerta)
   - Idempotencia por hashtag de auditoria mantida

Output JSON (stdout):
  {"executed": [...], "skipped": [...], "errors": [...]}
"""

import argparse
import json
import os
import re
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
MAX_CATCHUPS_PER_WEEK = 2
MAX_LATE_HOURS = 48


def load_env() -> None:
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


# Cronograma esperado: (mes, dia, hora_utc) -> numero_post
# DEVE ser sincronizado com .github/workflows/instagram-scheduled-posts.yml
SCHEDULE = {
    (6, 1, 12): 3,
    (6, 1, 16): 4,
    (6, 1, 21): 5,
    (6, 2, 12): 7,
    (6, 2, 16): 8,
    (6, 2, 21): 9,
}


def expected_today(now_utc: datetime) -> list[tuple[int, datetime]]:
    """Retorna lista de (post_num, horario_esperado_utc) que deveriam ter saido hoje."""
    today = now_utc.date()
    out = []
    for (m, d, h), num in SCHEDULE.items():
        scheduled = datetime(now_utc.year, m, d, h, 0, tzinfo=timezone.utc)
        if scheduled.date() == today:
            out.append((num, scheduled))
    return out


def fetch_recent_media(token: str, user_id: str, hours: int = 36) -> list[dict]:
    """Lista posts publicados nas ultimas N horas."""
    url = (
        f"{GRAPH}/{user_id}/media"
        f"?fields=id,caption,timestamp&limit=25&access_token={urllib.parse.quote(token)}"
    )
    with urllib.request.urlopen(url, timeout=30) as resp:
        data = json.loads(resp.read()).get("data", [])
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=hours)
    out = []
    for p in data:
        raw = p["timestamp"].replace("Z", "+00:00")
        if len(raw) >= 5 and raw[-5] in "+-" and raw[-3] != ":":
            raw = raw[:-2] + ":" + raw[-2:]
        ts = datetime.fromisoformat(raw)
        if ts >= cutoff:
            out.append({"id": p["id"], "ts": ts, "caption": p.get("caption", "")})
    return out


def caption_signature(caption: str, length: int = 60) -> str:
    return caption[:length].strip()


def load_catchup_history() -> dict:
    if not CATCHUP_LOG.exists():
        return {"runs": []}
    try:
        return json.loads(CATCHUP_LOG.read_text())
    except Exception:
        return {"runs": []}


def save_catchup_history(hist: dict) -> None:
    CATCHUP_LOG.parent.mkdir(parents=True, exist_ok=True)
    CATCHUP_LOG.write_text(json.dumps(hist, indent=2, default=str))


def count_recent_catchups(hist: dict, days: int = 7) -> int:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
    return sum(
        1
        for run in hist.get("runs", [])
        if datetime.fromisoformat(run["timestamp"]) >= cutoff and run["executed"]
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="so detecta, nao publica")
    args = parser.parse_args()

    load_env()
    token = os.environ.get("IG_ACCESS_TOKEN")
    user_id = os.environ.get("IG_USER_ID")
    if not (token and user_id):
        print(json.dumps({"error": "credenciais ausentes", "executed": [], "skipped": [], "errors": ["IG_ACCESS_TOKEN/IG_USER_ID nao definidos"]}))
        sys.exit(1)

    now = datetime.now(tz=timezone.utc)
    posts = {p["number"]: p for p in json.loads(CONFIG.read_text())}

    expected = expected_today(now)
    if not expected:
        print(json.dumps({"executed": [], "skipped": ["sem posts esperados hoje"], "errors": []}))
        return

    recent = fetch_recent_media(token, user_id, hours=36)
    recent_sigs = {caption_signature(m["caption"]) for m in recent}

    hist = load_catchup_history()
    recent_catchups = count_recent_catchups(hist, days=7)

    executed: list[dict] = []
    skipped: list[dict] = []
    errors: list[dict] = []

    for num, scheduled_at in expected:
        post = posts.get(num)
        if not post:
            errors.append({"post": num, "reason": "ausente do JSON"})
            continue
        sig = caption_signature(post["caption"])
        if sig in recent_sigs:
            skipped.append({"post": num, "reason": "ja publicado"})
            continue
        late_hours = (now - scheduled_at).total_seconds() / 3600
        if late_hours > MAX_LATE_HOURS:
            errors.append({"post": num, "reason": f"atrasado {late_hours:.0f}h (> {MAX_LATE_HOURS}h) - desistir"})
            continue
        if late_hours < 0:
            skipped.append({"post": num, "reason": "ainda nao deu hora"})
            continue
        if recent_catchups >= MAX_CATCHUPS_PER_WEEK:
            errors.append({"post": num, "reason": f"limite {MAX_CATCHUPS_PER_WEEK} catchups/sem atingido"})
            continue

        if args.dry_run:
            executed.append({"post": num, "late_hours": late_hours, "would_run": True})
            continue

        try:
            r = subprocess.run(
                [sys.executable, str(ROOT / "post_to_instagram.py"), str(num), "--publish"],
                capture_output=True,
                text=True,
                timeout=600,
                cwd=str(ROOT.parent),
            )
            if r.returncode == 0:
                executed.append({"post": num, "late_hours": late_hours, "stdout_tail": r.stdout[-500:]})
                recent_catchups += 1
            else:
                errors.append({"post": num, "reason": f"exit {r.returncode}", "stderr_tail": r.stderr[-500:]})
        except subprocess.TimeoutExpired:
            errors.append({"post": num, "reason": "timeout 10min"})

    hist["runs"].append(
        {
            "timestamp": now.isoformat(),
            "executed": executed,
            "skipped": skipped,
            "errors": errors,
            "dry_run": args.dry_run,
        }
    )
    if not args.dry_run:
        save_catchup_history(hist)

    print(json.dumps({"executed": executed, "skipped": skipped, "errors": errors}, indent=2, default=str))

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
