---
name: dataforseo
description: Expand SEO keyword lists and export competitor ranking keywords with DataForSEO Labs. Use when Claude needs to call DataForSEO `related_keywords/live` for one or more seed keywords, call `ranked_keywords/live` for one or more competitor domains, generate CSV outputs named by keyword or domain plus date, or run both workflows together from the same request.
---

# DataForSEO

## Overview

Use the bundled Python scripts to export DataForSEO keyword datasets into CSV files.
Keep credentials in the local `.env` file, never in prompts or committed code.
Related keyword expansion defaults to English and United States.

## Workflow

1. Open `.env` and fill `DATAFORSEO_LOGIN` plus `DATAFORSEO_PASSWORD`.
2. Choose the script that matches the request:
   - `scripts/related_keywords_live.py` for one or more seed keywords.
   - `scripts/ranked_keywords_live.py` for one or more competitor domains.
3. If the user provides both keywords and domains, run both scripts separately in the same session.
4. Return the generated CSV paths.

## Commands

Run related keyword expansion:

```bash
python3 scripts/related_keywords_live.py "seo tool" "rank tracker"
```

Run related keyword expansion with explicit language and region:

```bash
python3 scripts/related_keywords_live.py "seo tool" --language english --region us
```

Run competitor ranked keyword export:

```bash
python3 scripts/ranked_keywords_live.py "ahrefs.com" "semrush.com"
```

Optional flags:

- `--output-dir` to override the default export folder. By default, CSV files go to the skill's `output/` directory.
- `--location-code` to change the target market by DataForSEO code.
- `--language-code` to change the target language by code.
- `--region` to set a named region for keyword expansion, such as `us`, `uk`, `ca`, `au`, `nz`, or `sg`.
- `--language` to set a named language for keyword expansion, such as `english`, `german`, `french`, `spanish`, `japanese`, or `chinese`.
- `--limit` to control the number of rows requested per API call.

## Output

Each input creates one CSV file.

- Related keywords: `<keyword>_<YYYYMMDD>.csv`
- Ranked keywords: `<domain>_<YYYYMMDD>.csv`

The scripts flatten nested API fields so the CSV keeps useful columns without requiring manual schema updates.

## Resources

- Read `references/api_reference.md` for endpoint details, environment variables, and example invocations.
- Use `scripts/_common.py` only as the shared helper module for both export scripts.
