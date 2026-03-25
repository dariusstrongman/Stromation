Update the navigation bar across ALL pages of the Stromation website.

What to change: $ARGUMENTS

Steps:
1. Read the current nav from `index.html` as the reference
2. Apply the requested change to the nav HTML
3. Update the nav in ALL root-level HTML files (index.html, about.html, services.html, industries.html, case-studies.html, contact.html, audit.html, blog.html, privacy.html, terms.html, 404.html)
4. Update the nav in ALL blog post HTML files in `blog/` (note: blog posts use `../` prefix for relative paths like `../index.html`, `../logo.svg`, etc.)
5. Make sure the correct `active` class is preserved on each page's own nav link
6. Report how many files were updated
