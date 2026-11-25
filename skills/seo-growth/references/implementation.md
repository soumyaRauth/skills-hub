# Changing website code safely

SEO changes live in templates and config that every page shares. A wrong
canonical in a layout is wrong on every page at once. Understand how the site
is built before changing it, change as little as possible, and prove the
result.

## Contents

- Before the first change
- Where SEO lives, by framework
- Making the change
- Validating
- Recording
- When the code is not here

## Before the first change

1. **Identify the stack**: `package.json`, `astro.config.*`, `next.config.*`,
   `nuxt.config.*`, `svelte.config.*`, `gatsby-config.*`, `hugo.toml` or
   `config.toml`, `_config.yml`, `mkdocs.yml`, `docusaurus.config.*`,
   `.vitepress/`, a CMS export, or plain HTML.
2. **Identify the build and deployment**: the build command, the output
   folder, and the host (`CNAME`, `vercel.json`, `netlify.toml`, a GitHub
   Pages workflow, `.htaccess`, `_redirects`, server config). Redirects and
   headers often live there, not in the code.
3. **Find where each SEO element comes from**: the title and description
   template, the canonical, robots meta, the sitemap and `robots.txt`
   generators, structured data, the site URL setting.
4. **Read the conventions**: how pages declare front matter, how components
   are composed, the formatting style, existing tests.
5. **Build once before changing anything**, and record whether it passes.
   A site that does not build before the change is reported, not blamed on
   the change.
6. **Capture a before snapshot**: `seo_audit.py page` on the pages to change,
   or a crawl of the built output.

## Where SEO lives, by framework

Check the project's installed version and its docs; these are starting
points, not guarantees.

| Stack | Titles and meta | Sitemap and robots | Site URL |
| --- | --- | --- | --- |
| Plain HTML | Each file's `<head>` | Hand-written `sitemap.xml`, `robots.txt` | Absolute URLs in the files |
| Next.js (App Router) | `metadata` export or `generateMetadata` in `layout`/`page` files | `app/sitemap.*`, `app/robots.*` | `metadataBase` |
| Next.js (Pages Router) | `next/head` in pages or a shared component | Often a package such as `next-sitemap`, or files in `public/` | Config or environment |
| Astro | Layout component `<head>`, page props | `@astrojs/sitemap` integration; `public/robots.txt` | `site` in `astro.config` |
| Hugo | `layouts/partials/head.html` or the theme's; page front matter | Built-in sitemap; `enableRobotsTXT` | `baseURL` |
| Jekyll | Layout `<head>`; `jekyll-seo-tag` (`{% seo %}`) | `jekyll-sitemap`; `robots.txt` file | `url` in `_config.yml` |
| Gatsby | Head API or a SEO component | `gatsby-plugin-sitemap` | `siteMetadata.siteUrl` |
| Nuxt | `useHead`, `useSeoMeta`, `app.head` | Sitemap and robots modules | Site config |
| SvelteKit | `<svelte:head>` per route | An endpoint or prerendered file | Config or environment |
| Docusaurus, VitePress, MkDocs | Front matter and theme config | Built-in or config-driven sitemap | `url`, `sitemap.hostname`, `site_url` |
| WordPress and hosted CMSs | Theme and an SEO plugin, in the admin | The plugin or the CMS | Settings |

For a hosted CMS, changes happen in its admin, not in this repository. Write
exact instructions for the owner, or act through an authorized integration.

## Making the change

- **Smallest diff that fixes the cause.** Fix the template once, not every
  generated page.
- **Single source of truth.** Titles, descriptions and structured data come
  from the same data as the visible content (front matter, config).
- **Follow the conventions** of the codebase, its formatting and its
  component patterns.
- **No new dependency** without approval; hand the choice to
  `dependency-guard` when a package is proposed.
- **Never change URLs, redirects, robots, canonicals, sitemaps, hosts or
  rendering** without approval (`SKILL.md`, approval boundaries).
- **Content changes** to the owner's words, bio or claims are proposed, not
  made silently.
- **Larger changes** (a new section, a template overhaul, a migration) go
  through `proof-driven-dev`, with `impact-map` when routes or shared
  components are renamed.
- **No commits or pushes** unless the owner asked or `profile.md` authorizes
  them. Leave changes in the working tree, or on a branch if the project works
  that way, and say which.

## Validating

After every change, as far as the environment allows:

1. Build the site. A failing build is a failed change.
2. Run the project's tests and linters.
3. Serve the output locally (`python3 -m http.server -d <output folder>`, or
   the framework's preview) and run `seo_audit.py page` on each changed page.
   Use `--map-origin https://example.com=http://localhost:8000` on a crawl so
   sitemap and canonical URLs pointing at production are checked locally.
4. Compare with the before snapshot: only the intended differences.
5. Parse structured data and compare it with the visible content.
6. Check links: no new broken internal links, no links to redirects.
7. Look at the page, or a rendered screenshot when a browser tool exists,
   when visible content or layout changed.
8. After deployment (by the owner or the authorized workflow), fetch the live
   page once and confirm.

If something could not be validated, say exactly what and why.

## Recording

For each change: the task ID, the files changed, what changed, how it was
validated, where it lives (working tree, branch, commit), and whether it is
deployed. Update `content.md` for affected pages and start an experiment when
the change should be measured.

## When the code is not here

When the site is live but its source is elsewhere:

- Give the owner a patch, or exact instructions per file or per CMS screen.
- Validate against the live site after the owner deploys, and record the
  date the change actually went live.
- Mark the task `Blocked` on deployment until then, not `Completed`.
