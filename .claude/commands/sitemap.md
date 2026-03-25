Update the sitemap.xml for the Stromation website.

Steps:
1. Read the current `sitemap.xml`
2. Scan all HTML files in root and `blog/` directories
3. Check for any pages that are missing from the sitemap
4. Check for any sitemap entries pointing to pages that no longer exist
5. Update `lastmod` dates for any files that have been recently modified (check git log)
6. Add any missing pages with today's date
7. Remove any stale entries
8. Report what was added, removed, or updated
