# Stage 3: Publish the handbook website (optional)

**Purpose:** turn `CLAUDE.md` and `handbook/` into a small website with a sidebar, one page per
handbook file, so anyone at the company can read how finance works without opening a folder of
markdown files. Rebuild it whenever the handbook changes.

**Check first:** if the Company at a glance section of `CLAUDE.md` is still mostly
placeholders, the site would be mostly empty. Say so and offer the interview (stage 1) before
publishing.

The site is plain HTML and CSS in a folder called `site/`. No installs, no build tools, no
external scripts. Open `site/index.html` in a browser to view it.

## Read first

- `skills/setup-finance-brain/site-template/page.html` (the page layout) and
  `skills/setup-finance-brain/site-template/style.css` (the look)
- `CLAUDE.md` and every file in `handbook/`
- The frontmatter `description` of every `skills/*/SKILL.md`, and the workflow groups in
  `skills/README.md`

## Pages to build

| Page | Built from | Notes |
| --- | --- | --- |
| `index.html` (Home) | `CLAUDE.md`: Company at a glance, Map, Open questions | Title it "{Company} Finance Handbook" and open with one line: "How {Company} does its accounting. Start with the page you need." Link each row of the Map to its page. |
| One page per handbook file | `handbook/{name}.md` | `company-overview.md` becomes `company-overview.html`, and so on. |
| `skills.html` | Every skill's name and `description` | Group by workflow, as `skills/README.md` does (Setup, Journal entries, Reconciliations, and so on). Don't link to the files; show each skill's folder as code. |
| `changelog.html` | The Changelog section of `CLAUDE.md` | |

Don't publish `handbook/sources/`, `testing/`, or anything in `skills/` beyond the descriptions.

## Steps

1. **Start clean.** Create `site/` if it doesn't exist. If it does, replace the pages you build;
   don't delete other files without asking.
2. **Convert each source to HTML** faithfully: headings, paragraphs, lists, tables, block quotes,
   inline code, code blocks, links, bold, and italics. Keep the wording exactly as written.
3. **Fix links.** A link to another handbook `.md` file points to its `.html` page. Mentions of a
   handbook file in backticks (for example `handbook/cash.md`) become links to that page. Leave
   everything else as plain code.
4. **Flag the gaps.** Wrap every `[PLACEHOLDER: ...]` in `<span class="placeholder">...</span>`
   so open items stand out. Don't remove or rewrite them.
5. **Fill the template** for each page:
   - `{{SITE_TITLE}}`: "{Company} Finance Handbook"
   - `{{PAGE_TITLE}}`: the page's first heading
   - `{{CONTENT}}`: the converted HTML
   - `{{BUILD_DATE}}`: today's date, YYYY-MM-DD
   - `{{NAV}}`: the sidebar, the same on every page, with `aria-current="page"` on the current link:

     ```html
     <ul>
       <li><a href="index.html">Home</a></li>
       <li class="group">Handbook</li>
       <li><a href="company-overview.html">Company overview</a></li>
       <li><a href="chart-of-accounts.html">Chart of accounts</a></li>
       <li><a href="accounting-policies.html">Accounting policies</a></li>
       <li><a href="close-process.html">Close process</a></li>
       <li><a href="cash.html">Cash</a></li>
       <li><a href="metrics-and-reporting.html">Metrics and reporting</a></li>
       <li><a href="systems-and-data.html">Systems and data</a></li>
       <li><a href="workpaper-standard.html">Workpaper standard</a></li>
       <li class="group">Reference</li>
       <li><a href="skills.html">Skills</a></li>
       <li><a href="changelog.html">Changelog</a></li>
     </ul>
     ```

     Add a link for any extra page the team has added to `handbook/`.
6. **Copy `skills/setup-finance-brain/site-template/style.css`** into `site/`.

## Checks before handoff

- Every page in the nav exists, and every internal link points to a page that exists.
- No page contains a full bank or card account number (anything that looks like a run of 8 or
  more digits gets a second look), a password, or a token.
- The placeholder count on the site matches the placeholder count in the source files.

Tell the user how many pages were built and how many placeholders are still open.

## Sharing it

This is an **internal** site. It describes how the company's money moves. Share it the way you'd
share any internal policy document:

- Put the `site/` folder on the company's shared drive and open `index.html`.
- Or host it somewhere access-controlled, like your company intranet. If you use GitHub Pages,
  check your plan: on most plans a Pages site is public even when the repository is private.

Never publish it to the open internet.

## Never

- Never write to a connected system. This stage reads only the files in this folder.
- Never fill in or guess at a placeholder while publishing. It appears on the site as it is.
- Never change the wording of a handbook page while building the site. Edit the markdown, then
  rebuild.
- Never include files from `handbook/sources/` or `testing/`.
