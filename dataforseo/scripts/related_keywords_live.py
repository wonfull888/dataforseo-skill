#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from _common import build_output_path, ensure_output_dir, extract_items, load_env, parse_args, post_json, print_created, resolve_language_code, resolve_location_code, rows_from_items, write_csv


def main() -> None:
    args = parse_args(
        description="Export DataForSEO related keywords into per-keyword CSV files",
        input_label="keywords",
        include_locale_names=True,
    )
    skill_root = Path(__file__).resolve().parent.parent
    load_env(skill_root)
    output_dir = ensure_output_dir(skill_root, args.output_dir)
    language_code = resolve_language_code(args.language, args.language_code)
    location_code = resolve_location_code(args.region, args.location_code)

    for keyword in args.keywords:
        response = post_json(
            "related_keywords/live",
            [{
                "keyword": keyword,
                "location_code": location_code,
                "language_code": language_code,
                "limit": args.limit,
            }],
        )
        items = extract_items(response)
        rows = rows_from_items("seed_keyword", keyword, items)
        output_path = build_output_path(output_dir, "related_keywords", keyword)
        write_csv(output_path, rows)
        print_created(output_path, len(rows))


if __name__ == "__main__":
    main()
