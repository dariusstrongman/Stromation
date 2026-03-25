Check for broken internal links across the entire Stromation website.

Steps:
1. Scan all HTML files (root and blog/) for `href` and `src` attributes
2. For each internal link (not starting with http/https/mailto/tel/#):
   - Resolve the path relative to the file it's in
   - Check if the target file actually exists on disk
3. Also check for:
   - Links to anchors (e.g., `services.html#pricing`) where the target file exists but the anchor ID doesn't
   - Empty href attributes
   - Duplicate links that could be consolidated
4. Report all broken links with the source file, line number, and the broken href/src value
5. Give a summary count at the end
