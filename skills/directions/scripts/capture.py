import json, sys, os
from playwright.sync_api import sync_playwright

OUT = os.path.abspath("refs-out")
os.makedirs(OUT, exist_ok=True)
SITES = dict(a.split("=",1) for a in sys.argv[1:]) or {"example":"https://example.com/"}
VIEWPORTS = {"1336x647": (1336, 647), "1440x900": (1440, 900), "1920x1080": (1920, 1080), "390x844": (390, 844)}

PROBE = r"""
() => {
  const hdr = document.querySelector('header') || document.querySelector('nav');
  const cs = hdr ? getComputedStyle(hdr) : null;
  const h1 = document.querySelector('h1');
  const r = h1 ? h1.getBoundingClientRect() : null;
  const ctas = [...document.querySelectorAll('a,button')].filter(e => {
    const b = e.getBoundingClientRect(); return b.width > 60 && b.top < innerHeight * 1.6 && b.top > 60 && /start|empez|prob|crear|gratis|free|comenz/i.test(e.innerText||'');
  }).slice(0,4).map(e => ({text: e.innerText.trim().slice(0,40), top: Math.round(e.getBoundingClientRect().top), bottom: Math.round(e.getBoundingClientRect().bottom)}));
  return {
    vh: innerHeight, scrollY,
    header: cs ? {bg: cs.backgroundColor, color: cs.color, height: Math.round(hdr.getBoundingClientRect().height), position: cs.position, backdrop: cs.backdropFilter, shadow: cs.boxShadow, transition: cs.transition} : null,
    h1: h1 ? {text: h1.innerText.trim(), top: Math.round(r.top), bottom: Math.round(r.bottom), font: getComputedStyle(h1).fontFamily, size: getComputedStyle(h1).fontSize, weight: getComputedStyle(h1).fontWeight, lh: getComputedStyle(h1).lineHeight, ls: getComputedStyle(h1).letterSpacing} : null,
    heroCtas: ctas,
    bodyFont: getComputedStyle(document.body).fontFamily,
  };
}
"""

OUTLINE = r"""
() => {
  const out = [];
  for (const el of document.querySelectorAll('h1,h2,h3')) {
    const b = el.getBoundingClientRect();
    if (!el.innerText.trim() || b.height === 0) continue;
    out.push({tag: el.tagName, y: Math.round(b.top + scrollY), text: el.innerText.trim().replace(/\s+/g,' ').slice(0,140)});
  }
  const nav = [...document.querySelectorAll('header a, header button')].map(e => e.innerText.trim()).filter(Boolean).slice(0,30);
  return {height: document.documentElement.scrollHeight, nav, outline: out};
}
"""

def main():
    report = {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
        for site, url in SITES.items():
            report[site] = {}
            for vname, (w, h) in VIEWPORTS.items():
                ctx = b.new_context(viewport={"width": w, "height": h}, locale="es-AR",
                                    device_scale_factor=1, is_mobile=(w < 500), has_touch=(w < 500))
                page = ctx.new_page()
                try:
                    page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    page.wait_for_timeout(5000)
                    # dismiss cookie banners if obvious
                    for sel in ["button:has-text('Accept')", "button:has-text('Aceptar')", "button:has-text('Decline')", "button:has-text('Rechazar')"]:
                        try:
                            page.locator(sel).first.click(timeout=800)
                            break
                        except Exception:
                            pass
                    page.wait_for_timeout(800)
                    entry = {"top": page.evaluate(PROBE)}
                    page.screenshot(path=f"{OUT}/{site}-{vname}-top.png")
                    for y in (120, 900):
                        page.mouse.wheel(0, y - page.evaluate("scrollY"))
                        page.wait_for_timeout(900)
                        entry[f"scroll{y}"] = page.evaluate(PROBE)
                        page.screenshot(path=f"{OUT}/{site}-{vname}-scroll{y}.png")
                    if vname in ("1440x900", "390x844"):
                        # slow scroll through to trigger lazy content, then outline + full page
                        total = page.evaluate("document.documentElement.scrollHeight")
                        y = 0
                        while y < total:
                            y += 700
                            page.mouse.wheel(0, 700)
                            page.wait_for_timeout(250)
                            total = page.evaluate("document.documentElement.scrollHeight")
                        page.wait_for_timeout(1500)
                        entry["outline"] = page.evaluate(OUTLINE)
                        page.evaluate("scrollTo(0,0)")
                        page.wait_for_timeout(800)
                        page.screenshot(path=f"{OUT}/{site}-{vname}-full.png", full_page=True)
                        if vname == "1440x900":
                            with open(f"{OUT}/{site}-text.txt", "w") as f:
                                f.write(page.inner_text("body"))
                    report[site][vname] = entry
                except Exception as e:
                    report[site][vname] = {"error": str(e)[:300]}
                ctx.close()
        b.close()
    with open(f"{OUT}/report.json", "w") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print("done")

main()
