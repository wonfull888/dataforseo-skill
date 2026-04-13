# DataForSEO Skill 使用说明

## 适合什么场景

这个 skill 适合两类常见 SEO 工作：

1. 用核心关键词扩展相关关键词
2. 用竞品域名导出它已经有排名的关键词

每个关键词或域名单独请求一次，并各自生成一个 CSV 文件。

## 目录说明

- Skill 目录：`dataforseo/`
- 配置文件：`dataforseo/.env`
- 打包产物：`dist/dataforseo.skill`
- 默认输出目录：`dataforseo/output/`

## 先配置凭证

仓库里已经带了一个空的 `.env` 文件，直接填写即可：

```env
DATAFORSEO_LOGIN=your_login
DATAFORSEO_PASSWORD=your_password
```

## 功能 1：扩展相关关键词

默认配置：

- 语言：英文 `en`
- 地区：美国 `US`，对应 `location_code=2840`

传入一个或多个核心关键词：

```bash
python3 scripts/related_keywords_live.py "seo tool" "rank tracker"
```

指定语言和地区：

```bash
python3 scripts/related_keywords_live.py "seo tool" --language english --region us
```

也可以直接传代码：

```bash
python3 scripts/related_keywords_live.py "seo tool" --language-code de --location-code 2826
```

当前支持的命名地区：`us`、`uk`、`ca`、`au`、`nz`、`sg`

当前支持的命名语言包括：`english`、`german`、`french`、`spanish`、`italian`、`japanese`、`korean`、`dutch`、`portuguese`、`russian`、`chinese`

## 功能 2：导出竞品域名有排名的关键词

传入一个或多个竞品域名：

```bash
python3 scripts/ranked_keywords_live.py "ahrefs.com" "semrush.com"
```

如果需要，也可以用代码指定语言和地区：

```bash
python3 scripts/ranked_keywords_live.py "example.com" --language-code en --location-code 2840
```

## 常用参数

- `--output-dir`：自定义输出目录
- `--limit`：控制每次请求的结果条数
- `--language-code`：用代码指定语言
- `--location-code`：用代码指定地区

关键词扩展脚本还支持：

- `--language`：用语言名称指定语言
- `--region`：用地区名称或数字代码指定地区

## 输出文件

默认输出到 `dataforseo/output/`。

文件命名格式：

- 关键词：`<keyword>_<YYYYMMDD>.csv`
- 域名：`<domain>_<YYYYMMDD>.csv`

示例：

```text
seo_tool_20260413.csv
ahrefs_com_20260413.csv
```

## 同时使用两类功能

如果一次同时给了核心关键词和竞品域名，就分别运行两个脚本。

```bash
python3 scripts/related_keywords_live.py "seo tool" "link building" --language english --region us
python3 scripts/ranked_keywords_live.py "ahrefs.com" "semrush.com"
```

## 说明

- 脚本会把嵌套字段扁平化后再写入 CSV。
- 如果凭证缺失，会立即报错。
- 如果目标地区不在命名映射里，直接传 `location_code` 即可。
