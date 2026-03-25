Audit the Stromation website for performance issues.

Check all HTML, CSS, and JS files for:
1. **Images**: Missing width/height attributes (causes layout shift), oversized images, missing lazy loading on below-fold images, images without modern format alternatives
2. **CSS**: Unused CSS rules, render-blocking concerns, overly specific selectors
3. **JavaScript**: Render-blocking scripts, unnecessary dependencies, opportunities to defer/async
4. **HTML**: Excessive DOM depth, inline styles that could be classes, missing preconnect/preload hints
5. **Fonts**: Font loading strategy, unused font weights being loaded
6. **General**: Missing compression hints, caching headers (check if any meta tags or server config exists), accessibility issues that also impact Core Web Vitals

Report findings with severity (critical/warning/info) and specific file locations. Suggest fixes for each issue.
