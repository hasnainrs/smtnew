# Sports Medicine Training — Website

Navy & powder-blue, gradient-led design. Site files sit **directly at the
project root**, so this folder deploys as-is with zero host configuration.

---

## 1. Structure

```
sports-medicine-training/
├── index.html            ← the live site — deploy this folder as-is
├── courses.html          ← the course catalogue (filterable by category)
├── partnership.html
├── about-us.html
├── blog.html
├── contact-us.html
├── terms-of-service.html
├── privacy-policy.html
├── 404.html
├── robots.txt · sitemap.xml · netlify.toml
├── assets/
│   ├── css/style.css     ← all styling, driven by CSS variables
│   ├── js/main.js        ← nav, filters, accordion, forms
│   └── img/              ← logo + SVG icon sprite
│
├── src/                  ← EDIT HERE, then rebuild
│   ├── partials/header.html · footer.html
│   ├── templates/base.html
│   ├── pages/*.html      ← each page's content only
│   └── build.py
└── README.md
```

`src/` has no index.html, so no host will mistake it for the site.

## 2. Deploying

**Netlify** — push the contents of this folder to a repo and import it.
`netlify.toml` sets publish to `.` with no build command; leave defaults alone.

**Vercel** — import the repo, Framework Preset → **Other**, leave Root
Directory and Output Directory at their defaults. Do *not* enter `dist` —
there is no dist folder.

> Uploading to GitHub: open the extracted folder first and drag the files
> *inside* it. Dragging the outer folder creates a nested path and 404s.

**Anywhere else** — upload everything except `src/` to your web root.

## 3. The course catalogue

`courses.html` is organised into four categories, each with its own band:

| Category | Anchor | Treatment |
|---|---|---|
| Live & in person | `#live` | Gold banner cards |
| Core on-demand | `#core` | Navy banner cards |
| **Advanced** | `#advanced` | **Its own navy gradient panel — visually separated from everything else** |
| Free | `#free` | Blue banner card |

The filter chips at the top show/hide whole category bands (`data-filter` →
`data-cat` in `main.js`). Adding a course means copying an `<article class="course">`
block into the right band — no JS changes needed.

## 4. Design system

Brand colours sampled from the logo, defined once at the top of
`assets/css/style.css`:

```css
--navy-700:#1C3973;   /* brand navy */
--navy-600:#24499A;   /* mid navy — buttons, accents */
--gold:#F9C300;       /* accent, used sparingly */
--powder-200:#DEE9F9; /* section backgrounds */
--g-hero / --g-band / --g-powder   /* the gradients */
```

Sections alternate white → powder gradient → navy gradient, so the page
has rhythm without any one screen being too light or too dark.

## 5. Editing

Never hand-edit the root `.html` files — they're regenerated on every build.

| To change | Edit |
|---|---|
| Nav / logo (all pages) | `src/partials/header.html` |
| Footer (all pages) | `src/partials/footer.html` |
| One page's copy | `src/pages/<page>.html` |
| Colours, gradients, type | `assets/css/style.css` |
| Meta tags / fonts | `src/templates/base.html` |
| Titles & descriptions | the `PAGES` list in `src/build.py` |

Rebuild:

```bash
cd src
python3 build.py
```

Python 3, no dependencies. Output lands in the project root.

## 6. Before launch

1. **Wire up the form.** The enquiry form simulates success in the browser
   (see `[data-form]` in `assets/js/main.js`). Point it at Formspree,
   Netlify Forms, or your CRM. On Netlify: add `data-netlify="true"` to the
   `<form>` tag.
2. **Add course prices.** Cards currently show format and date only. Adding
   a price to each `.course-meta` would reduce drop-off to the checkout.
3. **Consider a Faculty page.** "Expert faculty" is claimed in several
   places but no clinicians are named. Real names, roles and the MSK
   Playbook / BJSM connection would be the strongest credibility asset on
   the site.
4. **Check course dates** in `src/pages/courses.html` are current.
5. **Social share image** — OG tags point at the logo; a 1200×630 PNG will
   look better on LinkedIn.

## 7. Built in

- Filterable course catalogue with Advanced as its own visual category
- Unique title + meta description per page, canonical URLs, OG/Twitter cards
- JSON-LD (EducationalOrganization, ItemList, ContactPage, CollectionPage)
- `robots.txt` + `sitemap.xml`
- One `<h1>` per page, semantic landmarks, skip link
- Keyboard-accessible nav (ESC to close), visible focus rings
- Content visible without JavaScript — animation is enhancement only
- Respects `prefers-reduced-motion`
- All icons/illustrations inline SVG — no image-hosting dependency
- Verified in Chromium at 1440px and 390px across all 9 pages: no
  horizontal overflow, no broken links, no missing assets
