"""Rebuild the example handbook site from docs/handbook-example/_source/.

This mirrors what the publish stage of the kit's setup-finance-brain skill
(templates/finance-brain/skills/setup-finance-brain/publish-site.md) asks Claude to do, so the
published example matches what a user's own build produces. Maintainers only; users never need it.

    uv run --with markdown --with pyyaml python3 docs/handbook-example/_build.py

Requires the `markdown` and `pyyaml` packages. Output: the .html files and style.css in this folder.
"""
from __future__ import annotations

import datetime as dt
import pathlib
import re
import shutil

import markdown
import yaml

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = HERE / "_source"
KIT = REPO / "templates" / "finance-brain"
SITE_TEMPLATE = KIT / "skills" / "setup-finance-brain" / "site-template"
TEMPLATE = (SITE_TEMPLATE / "page.html").read_text()

HANDBOOK_PAGES = [
    ("company-overview", "Company overview"),
    ("chart-of-accounts", "Chart of accounts"),
    ("accounting-policies", "Accounting policies"),
    ("close-process", "Close process"),
    ("cash", "Cash"),
    ("metrics-and-reporting", "Metrics and reporting"),
    ("systems-and-data", "Systems and data"),
    ("workpaper-standard", "Workpaper standard"),
]

# The skills page groups skills by workflow, in this order, as the kit's skills/README.md does.
SKILL_WORKFLOWS = [
    ("Setup", ["setup-finance-brain", "new-skill"]),
    ("Journal entries", ["prepaid-amortization", "usage-accrual"]),
    ("Reconciliations", ["bank-reconciliation"]),
    ("Level up", ["level-up"]),
]


def nav(current: str) -> str:
    def link(slug: str, label: str) -> str:
        cur = ' aria-current="page"' if slug == current else ""
        return f'<li><a href="{slug}.html"{cur}>{label}</a></li>'

    items = [link("index", "Home"), '<li class="group">Handbook</li>']
    items += [link(s, l) for s, l in HANDBOOK_PAGES]
    items += ['<li class="group">Reference</li>', link("skills", "Skills"), link("changelog", "Changelog")]
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


def skill_frontmatter(path: pathlib.Path) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    return yaml.safe_load(match.group(1)) if match else {}


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

    # Skills page: each skill's folder + description, grouped by workflow. Folders shown as code, not linked.
    skills = {}
    for path in sorted((KIT / "skills").glob("*/SKILL.md")):
        meta = skill_frontmatter(path)
        skills[meta.get("name", path.parent.name)] = meta.get("description", "")
    grouped = [name for _, names in SKILL_WORKFLOWS for name in names]
    workflows = SKILL_WORKFLOWS + [("Other", [name for name in skills if name not in grouped])]
    skills_md = ["# Skills", "Recurring tasks Claude runs the same way every month. Run them from the finance folder."]
    for workflow, names in workflows:
        rows = [f"| `skills/{name}/` | {skills[name]} |" for name in names if name in skills]
        if rows:
            skills_md += [f"## {workflow}", "| Skill | What it does |\n| --- | --- |\n" + "\n".join(rows)]
    render("skills", "Skills", site_title, to_html("\n\n".join(skills_md)), build_date)

    render("changelog", "Changelog", site_title, to_html("# Changelog\n\n" + sec["Changelog"]), build_date)

    shutil.copyfile(SITE_TEMPLATE / "style.css", HERE / "style.css")
    print(f"Built {len(HANDBOOK_PAGES) + 3} pages into {HERE}")


if __name__ == "__main__":
    main()
