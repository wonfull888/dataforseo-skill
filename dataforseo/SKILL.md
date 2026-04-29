---
name: dataforseo
description: Expand SEO keyword lists and export competitor ranking keywords with DataForSEO Labs. Use when Claude needs to call DataForSEO `keyword_suggestions/live` for deep long-tail expansion of seed keywords, call `related_keywords/live` for semantic related keywords, call `ranked_keywords/live` for one or more competitor domains, generate CSV outputs named by keyword or domain plus date, or run both workflows together from the same request.
---

# DataForSEO

## Overview

Use the bundled Python scripts to export DataForSEO keyword datasets into CSV files.
Keep credentials in the local `.env` file, never in prompts or committed code.
All keyword expansion defaults to English and United States.

## Cost-First Rule

**ALWAYS use API-side filtering. NEVER fetch all data and filter locally.**

DataForSEO charges per result row returned. Fetching thousands of rows and discarding most of them wastes money. Pass `filters`, `order_by`, and `limit` in the API request so the server returns only the rows you need. This is the only acceptable approach when the user specifies any filtering criteria.

## Workflow

1. Open `.env` and fill `DATAFORSEO_LOGIN` plus `DATAFORSEO_PASSWORD`.
2. Identify any filtering requirements from the user (KD range, position range, intent, search volume, etc.).
3. Choose the script that matches the request:
   - `scripts/keyword_suggestions_live.py` for deep long-tail expansion from seed keywords (recommended, returns hundreds to thousands of keywords with depth 1-4).
   - `scripts/related_keywords_live.py` for semantic related keywords (fewer results, ~7-10 per keyword).
   - `scripts/ranked_keywords_live.py` for one or more competitor domains.
4. If filters are required, write a short Python script that passes `filters` and `order_by` directly in the API payload — do not use the bundled scripts for filtered requests.
5. If the user provides both keywords and domains, run both scripts separately in the same session.
6. Return the generated CSV paths.

## Commands

Run deep keyword suggestion expansion (recommended for long-tail research):

```bash
python3 scripts/keyword_suggestions_live.py "seo tool" "rank tracker"
```

Run with explicit language, region, and depth:

```bash
python3 scripts/keyword_suggestions_live.py "seo tool" --language english --region us --depth 4
```

Run semantic related keyword expansion (lighter, fewer results):

```bash
python3 scripts/related_keywords_live.py "seo tool" "rank tracker"
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
- `--depth` (keyword_suggestions only) to set expansion depth from 1 to 4 (default: 4).

## API-Side Filtering

When the user specifies any filter criteria, add `filters`, `order_by`, and `limit` directly to the API request payload. The bundled scripts do not support filters — write a direct API call instead.

### Filter syntax

```json
"filters": [
  ["field_name", "operator", value],
  "and",
  ["field_name", "operator", value]
]
```

Supported operators: `=`, `<>`, `<`, `<=`, `>`, `>=`, `in`, `not_in`, `like`, `not_like`, `match`, `not_match`  
Maximum 8 filter conditions per request.

### Filterable fields for `ranked_keywords/live`

| Field | Type | Description |
|-------|------|-------------|
| `keyword_data.keyword_properties.keyword_difficulty` | num | Keyword difficulty score (0-100) |
| `ranked_serp_element.serp_item.rank_absolute` | num | Competitor's absolute SERP position |
| `keyword_data.search_intent_info.main_intent` | str | Main search intent: `informational`, `navigational`, `commercial`, `transactional` |
| `keyword_data.search_intent_info.foreign_intent` | array.str | Secondary intents |
| `keyword_data.keyword_info.search_volume` | num | Monthly search volume |
| `keyword_data.keyword_info.cpc` | num | Cost per click |
| `keyword_data.keyword_info.competition` | num | Ad competition (0-1) |
| `keyword_data.keyword_properties.core_keyword` | str | Core/head keyword |
| `ranked_serp_element.serp_item.rank_group` | num | Position within rank group |
| `ranked_serp_element.keyword_difficulty` | num | KD shortcut on SERP element |

### Sortable fields for `order_by`

```json
"order_by": ["keyword_data.keyword_info.search_volume,desc"]
```

### Example: filtered ranked keywords request

```python
resp = post_json("ranked_keywords/live", [{
    "target": "example.com",
    "location_code": 2840,
    "language_code": "en",
    "filters": [
        ["keyword_data.keyword_properties.keyword_difficulty", "<", 60],
        "and",
        ["ranked_serp_element.serp_item.rank_absolute", ">=", 11],
        "and",
        ["ranked_serp_element.serp_item.rank_absolute", "<=", 40],
        "and",
        ["keyword_data.search_intent_info.main_intent", "<>", "navigational"]
    ],
    "order_by": ["keyword_data.keyword_info.search_volume,desc"],
    "limit": 1000,
}])
```

### Filterable fields for `keyword_suggestions/live` and `related_keywords/live`

| Field | Type | Description |
|-------|------|-------------|
| `keyword_data.keyword_properties.keyword_difficulty` | num | Keyword difficulty score (0-100) |
| `keyword_data.keyword_info.search_volume` | num | Monthly search volume |
| `keyword_data.keyword_info.cpc` | num | Cost per click |
| `keyword_data.search_intent_info.main_intent` | str | Main search intent |
| `keyword_data.keyword_properties.core_keyword` | str | Core keyword |

## Output

Each input creates one CSV file.

- Keyword suggestions: `<keyword>_<YYYYMMDD>.csv`
- Related keywords: `<keyword>_<YYYYMMDD>.csv`
- Ranked keywords: `<domain>_<YYYYMMDD>.csv`

The scripts flatten nested API fields so the CSV keeps useful columns without requiring manual schema updates.

## Resources

- Read `references/api_reference.md` for endpoint details, environment variables, and example invocations.
- Use `scripts/_common.py` only as the shared helper module for both export scripts.
