# DataForSEO Skill

Use this skill when you need two fast SEO workflows from DataForSEO Labs:

1. Expand one or more seed keywords with `related_keywords/live`
2. Export one or more competitor domains' ranking keywords with `ranked_keywords/live`

Each keyword or domain produces its own CSV. The default export path is the skill's `output/` directory. Related keyword expansion defaults to English and United States, and can be overridden with language and region options.

## Install

Install the `dataforseo` skill folder into one of these locations:

- Claude Code: `~/.claude/skills/dataforseo`
- OpenCode: `~/.config/opencode/skills/dataforseo`
- Codex: `~/.codex/skills/dataforseo`

Then invoke it as:

```text
/dataforseo
```

## Configure

Create `dataforseo/.env` from `dataforseo/.env.example` and fill in your credentials:

```env
DATAFORSEO_LOGIN=
DATAFORSEO_PASSWORD=
```

## Use Cases

Use this skill when you want to:

- turn a seed keyword into a CSV of related keywords
- inspect which keywords competitor domains already rank for
- run both workflows in the same request and get separate CSV exports
- target a specific keyword market with language and region settings

## Commands

Expand seed keywords:

```bash
python3 scripts/related_keywords_live.py "seo tool" "rank tracker"
```

Expand keywords with language and region:

```bash
python3 scripts/related_keywords_live.py "seo tool" --language english --region us
```

Export competitor ranking keywords:

```bash
python3 scripts/ranked_keywords_live.py "ahrefs.com" "semrush.com"
```

## Output

Files are written to `dataforseo/output/` by default.

Examples:

```text
seo_tool_20260413.csv
ahrefs_com_20260413.csv
```

## Repo Layout

- `dataforseo/SKILL.md`: trigger description and usage instructions
- `dataforseo/scripts/`: Python exporters
- `dataforseo/references/`: endpoint notes and examples
- `dist/dataforseo.skill`: packaged release artifact
