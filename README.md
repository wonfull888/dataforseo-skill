# DataForSEO Skill

A Claude skill for expanding keyword lists and exporting competitor ranking keywords via DataForSEO Labs API. Tell Claude what you need in plain language — the skill handles the API calls and delivers CSV files.

## Install

Copy the `dataforseo/` skill folder into the skills directory for your AI coding assistant:

| Assistant | Path |
|-----------|------|
| Claude Code | `~/.claude/skills/dataforseo` |
| OpenCode | `~/.config/opencode/skills/dataforseo` |
| Codex | `~/.codex/skills/dataforseo` |

## Configure

Fill in your DataForSEO credentials in `dataforseo/.env`:

```env
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
```

Get credentials at [dataforseo.com](https://dataforseo.com).

## Activate

Load the skill in your session:

```text
/dataforseo
```

## What You Can Ask

Once the skill is active, describe your goal in natural language.

### Expand a seed keyword

> "用 dataforseo 帮我扩展 'seo tool' 这个关键词"

> "Get related keywords for 'rank tracker' and 'backlink checker'"

The skill calls `related_keywords/live`, collects all related terms, and saves a CSV named after the keyword with today's date.

Defaults: English language, United States market, depth 4.

### Change language or market

> "扩展 'seo 工具' 关键词，目标市场是中国，语言中文"

> "Related keywords for 'référencement' in French, target market France"

Supported named regions: `us`, `uk`, `ca`, `au`, `nz`, `sg`  
Supported named languages: `english`, `german`, `french`, `spanish`, `japanese`, `chinese`

### Export a competitor's ranking keywords

> "导出 ahrefs.com 的排名关键词"

> "Get ranking keywords for semrush.com and moz.com"

The skill calls `ranked_keywords/live` and saves one CSV per domain.

### Run both workflows together

> "扩展 'seo tool' 关键词，同时导出 ahrefs.com 的排名词"

The skill runs both exports in the same session and returns both CSV paths.

## Output

CSV files are saved to `dataforseo/output/` by default.

| Input | Output filename |
|-------|----------------|
| keyword: `seo tool` | `seo_tool_20260429.csv` |
| domain: `ahrefs.com` | `ahrefs_com_20260429.csv` |

Each CSV includes all useful fields from the API response, flattened — no post-processing needed.

## Example Session

```
User:  /dataforseo

User:  帮我扩展这几个关键词：keyword research, rank tracking, backlink analysis

Claude: 好的，我将为这 3 个关键词调用 DataForSEO related_keywords/live...
        输出文件：
        - output/keyword_research_20260429.csv
        - output/rank_tracking_20260429.csv
        - output/backlink_analysis_20260429.csv

User:  再帮我导出 ahrefs.com 和 semrush.com 的排名词

Claude: 正在调用 ranked_keywords/live...
        输出文件：
        - output/ahrefs_com_20260429.csv
        - output/semrush_com_20260429.csv
```

## Repo Layout

```
dataforseo/          ← skill folder (install this)
  SKILL.md           ← skill trigger description
  scripts/           ← API scripts called by the skill
  references/        ← endpoint notes and field reference
  output/            ← CSV exports land here
  .env               ← credentials (fill in, never commit)
docs/
  usage.zh-CN.md     ← Chinese usage guide
dist/
  dataforseo.skill   ← packaged release artifact
```
