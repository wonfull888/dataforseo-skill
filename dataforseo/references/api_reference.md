# DataForSEO Reference

## Environment

The scripts read credentials from `.env` in the skill root.

Required keys:

- `DATAFORSEO_LOGIN`
- `DATAFORSEO_PASSWORD`

## Endpoints

Related keyword expansion uses:

```text
POST https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live
```

Competitor ranked keyword export uses:

```text
POST https://api.dataforseo.com/v3/dataforseo_labs/google/ranked_keywords/live
```

## Default request fields

- `location_code=2840`
- `language_code=en`
- `limit=1000`

For `related_keywords_live.py`, the default market is English plus United States.
You can override it with either explicit codes or named flags.

The scripts send one API task per keyword or domain so each input gets its own CSV.

## Output naming

- `<keyword>_<YYYYMMDD>.csv`
- `<domain>_<YYYYMMDD>.csv`

Keywords and domains are sanitized so filenames remain safe across filesystems.

## Example commands

```bash
python3 scripts/related_keywords_live.py "keyword clustering" "seo audit"
python3 scripts/related_keywords_live.py "keyword clustering" --language english --region us
python3 scripts/related_keywords_live.py "seo agency" --language german --region de
python3 scripts/ranked_keywords_live.py "ahrefs.com" "semrush.com"
python3 scripts/related_keywords_live.py "link building" --location-code 2826 --language-code en --limit 500
python3 scripts/ranked_keywords_live.py "example.com" --output-dir output/ranked
```

## Notes

- The scripts flatten nested response fields before writing CSV rows.
- If the API returns no items for one input, the script still creates an empty CSV with only headers when possible.
- If the user gives both keywords and domains in one request, run both scripts and return both output sets.
- Named region support for keyword expansion currently includes `us`, `uk`, `ca`, `au`, `nz`, and `sg`. Pass `--location-code` or a numeric `--region` value for other markets.
