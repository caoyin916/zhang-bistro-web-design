import re

PAGES = ['index.html', 'menu.html', 'story.html', 'visit.html']
MAPS_URL = 'https://maps.google.com/?cid=12278787416581285066'
MAPS_EMBED = 'https://maps.google.com/maps?cid=12278787416581285066&amp;output=embed'
ORDER_URL = 'https://order.mealkeyway.com/customer/release/index?mid=464632736e67496e446a6e6770706831645a4e5344513d3d#/main'

FAVICON = (
    '<link rel="icon" type="image/png" href="assets/img/favicon.png" />\n'
    '<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png" />'
)

OLD_BRAND = '''      <span class="brand-mark cn">张</span>
      <span class="brand-word">
        <strong>Zhang's Bistro</strong>
        <span class="cn">川味张 · Carrollton, TX</span>
      </span>'''

NEW_BRAND = '''      <img src="assets/img/logo-mark.png" class="brand-logo" alt="" width="239" height="240" />
      <span class="brand-word">
        <strong>Zhang's Bistro</strong>
        <span class="cn">川味张</span>
      </span>'''

FOOTER = f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="index.html" class="footer-logo"><img src="assets/img/logo-full.png" alt="Zhang's Bistro 川味张" width="560" height="713" loading="lazy" /></a>
        <p>Authentic Sichuan cuisine in Carrollton, Texas. Traditional recipes, bold chili oil, and a menu 179 dishes deep. Order online for pickup or delivery.</p>
      </div>
      <div class="footer-col">
        <h4>Explore</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="menu.html">Menu</a></li>
          <li><a href="story.html">Our Story</a></li>
          <li><a href="visit.html">Location &amp; Hours</a></li>
          <li><a href="{ORDER_URL}" target="_blank" rel="noopener">Order Online</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Find Us</h4>
        <address>
          <a href="{MAPS_URL}" target="_blank" rel="noopener">2528 Old Denton Road<br />Carrollton, TX 75006</a><br /><br />
          <a class="tel" href="tel:+14692893379">(469) 289-3379</a><br /><br />
          Tue–Sun: 11 AM – 10 PM<br />
          Mon: Closed
        </address>
      </div>
      <div class="footer-col">
        <h4>Map</h4>
        <div class="footer-map">
          <iframe src="{MAPS_EMBED}" title="Map of Zhang's Bistro, 2528 Old Denton Road, Carrollton, TX" loading="lazy" tabindex="-1" aria-hidden="true" referrerpolicy="no-referrer-when-downgrade"></iframe>
          <a class="footer-map-link" href="{MAPS_URL}" target="_blank" rel="noopener" aria-label="Open Zhang's Bistro in Google Maps"><span>Open in Google Maps →</span></a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Zhang's Bistro 川味张. All rights reserved.</span>
      <span>2528 Old Denton Road, Carrollton, TX 75006</span>
    </div>
  </div>
</footer>'''


def replace_once(text, pattern, repl, page, label, regex=False):
    if regex:
        new, n = re.subn(pattern, lambda _: repl, text, flags=re.S)
    else:
        n = text.count(pattern)
        new = text.replace(pattern, repl)
    assert n == 1, f'{page}: expected 1 match for {label}, got {n}'
    return new


for page in PAGES:
    path = '../../' + page
    with open(path, encoding='utf-8') as f:
        html = f.read()
    html = replace_once(html, r'<link rel="icon" href="data:image/svg\+xml[^\n]*', FAVICON, page, 'favicon', regex=True)
    html = replace_once(html, OLD_BRAND, NEW_BRAND, page, 'header brand')
    html = replace_once(html, r'<footer class="site-footer">.*?</footer>', FOOTER, page, 'footer', regex=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('updated', page)
