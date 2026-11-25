# Structured data

Structured data describes what a page already says, in a vocabulary machines
read. It can make a page eligible for some search features and helps search
engines connect entities: this person wrote this article and owns these
profiles. It never makes a weak page strong, and it never promises a rich
result.

## Contents

- Rules
- Which types, when
- Connecting entities
- Personal site patterns
- Validation
- Keeping it in sync

## Rules

- **Only what is visible.** Every property describes content a visitor can
  see on that page. No hidden facts, no ratings or reviews that do not exist
  on the page, no credentials the page does not state.
- **Accurate and current.** Dates, names, prices and URLs match the page.
- **Vocabulary from schema.org; features from Google's documentation.**
  Google's supported rich-result types change over time (HowTo results were
  retired, and FAQ results limited to a small set of authoritative sites, in
  2023). Check the current Google Search Gallery before telling the owner a
  feature is possible, and never promise one.
- **JSON-LD**, in the page's HTML, generated from the same data as the
  visible content where the framework allows.
- **Necessary only.** A type that no search feature uses and that adds no
  entity information is clutter.
- Misleading markup can lead to a manual action. When in doubt, leave it out.

## Which types, when

| Type | Use on | Worth it because |
| --- | --- | --- |
| `WebSite` | Homepage | `name` and `alternateName` inform the site name shown in results |
| `Person` | About page, as `mainEntity` of a `ProfilePage`; referenced as author elsewhere | Connects the owner's name, role, image and profiles (`sameAs`) |
| `ProfilePage` | A page mainly about one person or organization | A documented Google type for creator profiles; its `mainEntity` is the Person |
| `Organization` | A business or brand site's homepage or about page | Logo, name, profiles; not for a solo person's portfolio unless there is a real organization |
| `Article` / `BlogPosting` | Articles | Headline, dates, image and an `author` that points to the Person |
| `BreadcrumbList` | Pages with visible breadcrumbs | Describes the hierarchy |
| `SoftwareApplication` | A page for an app or tool the owner makes | Describes the software; Google's rich result for it needs genuine ratings or reviews, so never invent them |
| `Event` | Real upcoming events the site lists | Date, place, organizer |
| `Course` | Real courses | Check Google's current support before expecting a feature |

## Connecting entities

Give the person one stable identifier and reuse it, so every page talks
about the same entity:

- `"@id": "https://example.com/#person"` on the Person, declared once (the
  about page or the homepage) and referenced elsewhere as
  `"author": {"@id": "https://example.com/#person"}` alongside a visible byline.
- `sameAs`: profile URLs that unambiguously represent this same person and
  that the page links to or the person controls. Never a namesake's profile,
  never a page merely mentioning them.
- `url`: the canonical page about the person.

## Personal site patterns

About page:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": {
    "@type": "Person",
    "@id": "https://example.com/#person",
    "name": "Jane Doe",
    "jobTitle": "Data engineer",
    "description": "Data engineer who builds and writes about reliable Airflow pipelines.",
    "url": "https://example.com/about/",
    "image": "https://example.com/images/jane-doe.jpg",
    "sameAs": [
      "https://github.com/janedoe-example",
      "https://www.linkedin.com/in/janedoe-example"
    ]
  }
}
</script>
```

Homepage:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Jane Doe",
  "alternateName": "Jane Doe, data engineer",
  "url": "https://example.com/"
}
</script>
```

Article:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "Airflow retries, explained with real failures",
  "datePublished": "2026-10-02",
  "dateModified": "2026-11-20",
  "image": "https://example.com/images/retries.png",
  "author": { "@type": "Person", "@id": "https://example.com/#person", "name": "Jane Doe", "url": "https://example.com/about/" }
}
</script>
```

Every value above must come from the page itself. Job title, image and
profiles are the owner's facts.

## Validation

1. `seo_audit.py page` parses every JSON-LD block and lists types and
   parse errors. A block that does not parse is ignored entirely.
2. Compare each property with the visible content.
3. The owner, or a browser tool, runs Google's Rich Results Test for
   Google-supported features, and the Schema Markup Validator for general
   schema.org validity. Record the result and date.
4. After deployment, Search Console's enhancement reports show errors at
   scale, when the owner has access.

## Keeping it in sync

Generate structured data from the same source as the visible content
(front matter, the page's data, the site config) rather than hand-writing it
per page, so a changed title or date cannot drift. When content changes,
re-validate. Record the types in use per page in `content.md`.
