#!/usr/bin/env python3

from __future__ import annotations

from pathlib import Path

from _common import ensure_output_dir, extract_items, load_env, parse_args, post_json, print_created, rows_from_items, build_output_path, write_csv


def main() -> None:
    args = parse_args(
        description="Export DataForSEO ranked keywords into per-domain CSV files",
        input_label="domains",
    )
    skill_root = Path(__file__).resolve().parent.parent
    load_env(skill_root)
    output_dir = ensure_output_dir(skill_root, args.output_dir)

    for domain in args.domains:
        response = post_json(
            "ranked_keywords/live",
            [{
                "target": domain,
                "location_code": args.location_code,
                "language_code": args.language_code,
                "limit": args.limit,
            }],
        )
        items = extract_items(response)
        rows = rows_from_items("target_domain", domain, items)
        output_path = build_output_path(output_dir, "ranked_keywords", domain)
        write_csv(output_path, rows)
        print_created(output_path, len(rows))


if __name__ == "__main__":
    main()
