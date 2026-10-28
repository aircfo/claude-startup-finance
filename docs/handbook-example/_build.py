"""Rebuild the example handbook site from docs/handbook-example/_source/.

This mirrors what commands/publish/build-handbook-site.md asks Claude to do, so the published
example matches what a user's own build produces. Maintainers only; users never need it.

    python3 docs/handbook-example/_build.py

Requires the `markdown` package. Output: the .html files and style.css in this folder.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import shutil

import markdown

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = HERE / "_source"
KIT = REPO / "templates" / "finance-brain"
TEMPLATE = (KIT / "site-template" / "page.html").read_text()

HANDBOOK_PAGES = [
    ("company-overview", "Company overview"),
    ("chart-of-accounts", "Chart of accounts"),
    ("accounting-policies", "Accounting policies"),
    ("close-process", "Close process"),
    ("cash", "Cash"),
    ("metrics-and-reporting", "Metrics and reporting"),
    ("systems-and-data", "Systems and data"),
]


def nav(current: str) -> str:
    def link(slug: str, label: str) -> str:
        cur = ' aria-current="page"' if slug == current else ""
        return f'<li><a href="{slug}.html"{cur}>{label}</a></li>'

    items = [link("index", "Home"), '<li class="group">Handbook</li>']
    items += [link(s, l) for s, l in HANDBOOK_PAGES]
    items += ['<li class="group">Reference</li>', link("commands", "Commands"), link("changelog", "Changelog")]
    return "<ul>\n" + "\n".join(items) + "\n</ul>"


def to_html(md_text: str) -> str:
    md_text = md_text.replace("- [x] ", "- ☑ ").replace("- [ ] ", "- ☐ ")
    html = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])
    html = re.sub(r"\[PLACEHOLDER:(.*?)\]", r'<span class="placeholder">[PLACEHOLDER:\1]</span>', html)
    # Backticked handbook paths become links to their pages.
    html = re.sub(
        r"<code>handbook/([a-z0-9-]+)\.md</code>",
        lambda m: f'<a href="{m.group(1)}.html"><code>handbook/{m.group(1)}.md</code></a>',
        html,
    )
    return html


def sections(md_text: str) -> dict[str, str]:
    out, name, buf = {}, "_head", []
    for line in md_text.splitlines():
        if line.startswith("## "):
            out[name] = "\n".join(buf).strip()
            name, buf = line[3:].strip(), []
        else:
            buf.append(line)
    out[name] = "\n".join(buf).strip()
    return out


def frontmatter_description(path: pathlib.Path) -> str:
    m = re.search(r"^description:\s*(.+)$", path.read_text(), re.M)
    return m.group(1).strip() if m else ""


def render(slug: str, title: str, site_title: str, body_html: str, build_date: str) -> None:
    page = (
        TEMPLATE.replace("{{PAGE_TITLE}}", title)
        .replace("{{SITE_TITLE}}", site_title)
        .replace("{{NAV}}", nav(slug))
        .replace("{{CONTENT}}", body_html)
        .replace("{{BUILD_DATE}}", build_date)
    )
    (HERE / f"{slug}.html").write_text(page)


def main() -> None:
    build_date = dt.date.today().isoformat()
    claude = (SOURCE / "CLAUDE.md").read_text()
    company = re.match(r"# Finance Brain:\s*(.+)", claude).group(1).strip()
    site_title = f"{company} Finance Handbook"
    sec = sections(claude)

    # Home: a short intro, company at a glance, the map (linked), and open questions.
    quotes = "\n".join(l for l in sec["_head"].splitlines() if l.startswith(">"))
    intro = f"How {company} does its accounting. Start with the page you need.\n\n{quotes}"
    home_md = "\n\n".join(
        [
            f"# {site_title}",
            intro,
            "## Company at a glance",
            sec["Company at a glance"],
            "## Where to find what",
            sec["Map: where to find more detail"],
            "## Open questions",
            sec["Open questions"],
        ]
    )
    render("index", "Home", site_title, to_html(home_md), build_date)

    for slug, label in HANDBOOK_PAGES:
        md_text = (SOURCE / "handbook" / f"{slug}.md").read_text()
        render(slug, label, site_title, to_html(md_text), build_date)

    # Commands page: path + description, grouped by folder. Paths shown as code, not linked.
    groups: dict[str, list[str]] = {}
    for path in sorted((KIT / "commands").rglob("*.md")):
        rel = path.relative_to(KIT)
        if rel.parts[1] in ("_templates",) or rel.name == "README.md":
            continue
        groups.setdefault(rel.parts[1], []).append(f"| `{rel.as_posix()}` | {frontmatter_description(path)} |")
    cmd_md = ["# Commands", "Recurring tasks Claude runs the same way every month. Run them from the finance folder."]
    labels = {"setup": "Setup", "jes": "Journal entries", "recs": "Reconciliations", "publish": "Publishing"}
    for folder in ("setup", "jes", "recs", "publish"):
        if folder in groups:
            cmd_md += [f"## {labels[folder]}", "| Command | What it does |\n| --- | --- |\n" + "\n".join(groups[folder])]
    render("commands", "Commands", site_title, to_html("\n\n".join(cmd_md)), build_date)

    render("changelog", "Changelog", site_title, to_html("# Changelog\n\n" + sec["Changelog"]), build_date)

    shutil.copyfile(KIT / "site-template" / "style.css", HERE / "style.css")
    print(f"Built {len(HANDBOOK_PAGES) + 3} pages into {HERE}")


if __name__ == "__main__":
    main()
