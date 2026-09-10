#!/usr/bin/env python3
"""
Sports Medicine Training — static site builder
==============================================
Combines src/partials/ + src/templates/base.html with each fragment in
src/pages/ and writes finished HTML into the PROJECT ROOT, so index.html
sits at the top level — ready for Netlify / Vercel / any static host with
zero configuration.

USAGE
-----
    cd src
    python3 build.py

Add a page: create src/pages/your-page.html, add an entry to PAGES below,
add a nav link in src/partials/header.html, re-run.
"""
import re
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
BASE_URL = "https://www.sportsmedicinetraining.com"

PAGES = [
    dict(slug="index", nav="home", schema="org",
         title="Sports Medicine Training | CPD Courses in MRI & MSK Ultrasound",
         desc="CPD-accredited sports medicine training for the whole MDT: clinical assessment, evidence-based treatment, MRI interpretation and hands-on MSK ultrasound, taught by the MSK Playbook faculty."),
    dict(slug="courses", nav="courses", schema="list",
         title="Courses | Live, Core, Advanced & Free MSK Training",
         desc="Browse every course by category: live in-person ultrasound masterclasses, core on-demand MSK Playbook programmes, advanced deep-dives, and free resources. All CPD accredited."),
    dict(slug="partnership", nav="partnership", schema="none",
         title="For Institutions | Bulk CPD Training for Trusts & Clinics",
         desc="Tiered bulk-purchase CPD discounts and institutional training partnerships for NHS Trusts, hospitals, sports medicine clinics and physiotherapy practices."),
    dict(slug="about-us", nav="about", schema="about",
         title="About Us | Sports Medicine Training",
         desc="Sports Medicine Training brings together Radiology Seminars, the MSK Playbook and the Advanced MSK Ultrasound Centre to deliver structured, evidence-based CPD."),
    dict(slug="blog", nav="blog", schema="blog",
         title="Resources | The MSK Playbook Reading List",
         desc="Curated MSK Playbook pre-course reading from the British Journal of Sports Medicine blog — practical reference for the whole MDT."),
    dict(slug="contact-us", nav="contact", schema="contact",
         title="Contact Us | Sports Medicine Training",
         desc="Get in touch about individual course enrolment, institutional partnerships or live in-person training. We reply within one working day."),
    dict(slug="terms-of-service", nav="", schema="none",
         title="Terms of Service | Sports Medicine Training",
         desc="The terms and conditions governing your use of Sports Medicine Training's website, courses and webinars."),
    dict(slug="privacy-policy", nav="", schema="none",
         title="Privacy Policy | Sports Medicine Training",
         desc="How Sports Medicine Training collects, uses and protects your personal data across our website, courses and webinars."),
    dict(slug="404", nav="", schema="none",
         title="Page Not Found | Sports Medicine Training",
         desc="The page you're looking for could not be found."),
]

SCHEMAS = {
    "org": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"EducationalOrganization","name":"Sports Medicine Training","url":"%(b)s/","logo":"%(b)s/assets/img/logo-full.png","description":"CPD-accredited sports medicine training covering clinical assessment, MRI interpretation and hands-on MSK ultrasound.","email":"info@radiologyseminars.co.uk","address":{"@type":"PostalAddress","streetAddress":"1 Market Hill","addressLocality":"Calne","addressRegion":"Wiltshire","postalCode":"SN11 0BT","addressCountry":"GB"}}
</script>""",
    "list": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ItemList","name":"Sports Medicine Training Course Catalogue","url":"%(b)s/courses.html"}
</script>""",
    "about": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"AboutPage","name":"About Sports Medicine Training","url":"%(b)s/about-us.html"}
</script>""",
    "contact": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"ContactPage","name":"Contact Sports Medicine Training","url":"%(b)s/contact-us.html"}
</script>""",
    "blog": """<script type="application/ld+json">
{"@context":"https://schema.org","@type":"CollectionPage","name":"The MSK Playbook Reading List","url":"%(b)s/blog.html"}
</script>""",
    "none": "",
}


def mark_active(header, nav_key):
    if not nav_key:
        return header
    pat = re.compile(r'<a ([^>]*data-nav="%s"[^>]*)>' % re.escape(nav_key))
    return pat.sub(lambda m: '<a class="is-active" %s>' % m.group(1), header, count=1)


def build():
    header = (SRC / "partials" / "header.html").read_text(encoding="utf-8")
    footer = (SRC / "partials" / "footer.html").read_text(encoding="utf-8")
    tpl = (SRC / "templates" / "base.html").read_text(encoding="utf-8")

    for p in PAGES:
        frag = SRC / "pages" / f"{p['slug']}.html"
        if not frag.exists():
            print(f"  ! skipped {p['slug']}")
            continue
        canonical = f"{BASE_URL}/" if p["slug"] == "index" else f"{BASE_URL}/{p['slug']}.html"
        s = SCHEMAS.get(p["schema"], "")
        html = (tpl
                .replace("{{TITLE}}", p["title"])
                .replace("{{DESCRIPTION}}", p["desc"])
                .replace("{{CANONICAL}}", canonical)
                .replace("{{SCHEMA}}", s % {"b": BASE_URL} if s else "")
                .replace("{{HEADER}}", mark_active(header, p["nav"]))
                .replace("{{FOOTER}}", footer)
                .replace("{{CONTENT}}", frag.read_text(encoding="utf-8")))
        (ROOT / f"{p['slug']}.html").write_text(html, encoding="utf-8")
        print(f"  built {p['slug']}.html")

    print(f"\nDone — {len(PAGES)} pages written to the project root.")


if __name__ == "__main__":
    build()
