#!/usr/bin/env python3

from __future__ import annotations

import argparse
import base64
import csv
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from urllib import error, request


API_BASE = "https://api.dataforseo.com/v3/dataforseo_labs/google"
DEFAULT_LOCATION_CODE = 2840
DEFAULT_LANGUAGE_CODE = "en"
DEFAULT_LIMIT = 1000

LANGUAGE_ALIASES = {
    "en": "en",
    "english": "en",
    "de": "de",
    "german": "de",
    "es": "es",
    "spanish": "es",
    "fr": "fr",
    "french": "fr",
    "it": "it",
    "italian": "it",
    "ja": "ja",
    "japanese": "ja",
    "ko": "ko",
    "korean": "ko",
    "nl": "nl",
    "dutch": "nl",
    "pt": "pt",
    "portuguese": "pt",
    "ru": "ru",
    "russian": "ru",
    "zh": "zh",
    "chinese": "zh",
}

REGION_ALIASES = {
    "us": DEFAULT_LOCATION_CODE,
    "usa": DEFAULT_LOCATION_CODE,
    "united states": DEFAULT_LOCATION_CODE,
    "united states of america": DEFAULT_LOCATION_CODE,
    "uk": 2826,
    "gb": 2826,
    "united kingdom": 2826,
    "ca": 2124,
    "canada": 2124,
    "au": 2036,
    "australia": 2036,
    "nz": 2554,
    "new zealand": 2554,
    "sg": 2702,
    "singapore": 2702,
}


def parse_args(description: str, input_label: str, include_locale_names: bool = False) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(input_label, nargs="+", help=f"One or more {input_label.replace('_', ' ')} values")
    parser.add_argument("--output-dir", help="Directory for generated CSV files")
    parser.add_argument("--location-code", type=int, default=DEFAULT_LOCATION_CODE, help="DataForSEO location_code")
    parser.add_argument("--language-code", default=DEFAULT_LANGUAGE_CODE, help="DataForSEO language_code")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Maximum rows per API request")
    if include_locale_names:
        parser.add_argument("--region", help="Region name, country code, or DataForSEO location code")
        parser.add_argument("--language", help="Language name or language code")
    return parser.parse_args()


def resolve_language_code(language: str | None, fallback: str) -> str:
    if not language:
        return fallback
    normalized = language.strip().lower()
    return LANGUAGE_ALIASES.get(normalized, normalized)


def resolve_location_code(region: str | None, fallback: int) -> int:
    if not region:
        return fallback
    normalized = region.strip().lower()
    if normalized.isdigit():
        return int(normalized)
    if normalized in REGION_ALIASES:
        return REGION_ALIASES[normalized]
    raise SystemExit(
        "Unsupported region value. Use a known region like us, uk, ca, au, nz, sg or pass a numeric DataForSEO location code."
    )


def load_env(skill_root: Path) -> None:
    env_path = skill_root / ".env"
    if not env_path.exists():
        raise SystemExit(f"Missing credentials file: {env_path}")

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())

    missing = [name for name in ("DATAFORSEO_LOGIN", "DATAFORSEO_PASSWORD") if not os.environ.get(name)]
    if missing:
        raise SystemExit(f"Missing required credentials in {env_path}: {', '.join(missing)}")


def auth_header() -> str:
    token = f"{os.environ['DATAFORSEO_LOGIN']}:{os.environ['DATAFORSEO_PASSWORD']}"
    encoded = base64.b64encode(token.encode("utf-8")).decode("ascii")
    return f"Basic {encoded}"


def post_json(endpoint: str, payload: list[dict[str, Any]]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url=f"{API_BASE}/{endpoint}",
        data=body,
        headers={
            "Authorization": auth_header(),
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"DataForSEO request failed: HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise SystemExit(f"DataForSEO request failed: {exc.reason}") from exc


def extract_items(response: dict[str, Any]) -> list[dict[str, Any]]:
    tasks = response.get("tasks") or []
    items: list[dict[str, Any]] = []
    for task in tasks:
        for result in task.get("result") or []:
            for item in result.get("items") or []:
                if isinstance(item, dict):
                    items.append(item)
    return items


def flatten_dict(value: Any, prefix: str = "") -> dict[str, Any]:
    rows: dict[str, Any] = {}
    if isinstance(value, dict):
        for key, nested in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            rows.update(flatten_dict(nested, next_prefix))
        return rows
    if isinstance(value, list):
        rows[prefix] = json.dumps(value, ensure_ascii=True)
        return rows
    rows[prefix] = value
    return rows


def ensure_output_dir(skill_root: Path, path: str | None) -> Path:
    output_dir = Path(path) if path else skill_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "export"


def today_stamp() -> str:
    return datetime.now().strftime("%Y%m%d")


def build_output_path(output_dir: Path, prefix: str, source_value: str) -> Path:
    del prefix
    return output_dir / f"{safe_slug(source_value)}_{today_stamp()}.csv"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row.keys():
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)

    if not fieldnames:
        fieldnames = ["source", "fetched_at"]

    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def rows_from_items(source_label: str, source_value: str, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fetched_at = datetime.now().isoformat(timespec="seconds")
    rows: list[dict[str, Any]] = []
    for item in items:
        row = {
            source_label: source_value,
            "fetched_at": fetched_at,
        }
        row.update(flatten_dict(item))
        rows.append(row)
    return rows


def print_created(path: Path, count: int) -> None:
    sys.stdout.write(f"Created {path} with {count} rows\n")
