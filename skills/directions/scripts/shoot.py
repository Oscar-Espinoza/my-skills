import sys, json, os
from playwright.sync_api import sync_playwright
SITE = "file://" + os.path.abspath(sys.argv[1])
OUT = sys.argv[2]; os.makedirs(OUT, exist_ok=True)
VPS = {"1440x900":(1440,900),"1336x647":(1336,647),"1280x720":(1280,720),"390x844":(390,844),"360x640":(360,640)}
CHECK = r"""() => {
  const ctas=[...document.querySelectorAll('.hero .ctas a')].map(a=>{const r=a.getBoundingClientRect();return {t:a.innerText.trim(),top:Math.round(r.top),bottom:Math.round(r.bottom)}});
  return {vh:innerHeight, ctas, docW:document.documentElement.scrollWidth, vw:innerWidth, h:document.documentElement.scrollHeight,
    hdrSolid: document.getElementById('hdr').classList.contains('solid')};
}"""
res={}
with sync_playwright() as p:
  b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
  for name,(w,h) in VPS.items():
    ctx=b.new_context(viewport={"width":w,"height":h}, is_mobile=w<500, has_touch=w<500, device_scale_factor=1)
    pg=ctx.new_page(); errs=[]
    pg.on("console", lambda m: m.type=="error" and errs.append(m.text))
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(SITE); pg.wait_for_timeout(1800)
    r=pg.evaluate(CHECK); r["errors"]=errs[:5]
    pg.screenshot(path=f"{OUT}/{name}-top.png")
    if name in ("1440x900","390x844"):
      pg.mouse.wheel(0,300); pg.wait_for_timeout(500); r["afterScroll"]=pg.evaluate(CHECK)["hdrSolid"]
      tot=pg.evaluate("document.documentElement.scrollHeight"); y=0
      while y<tot: y+=500; pg.mouse.wheel(0,500); pg.wait_for_timeout(120)
      pg.wait_for_timeout(800); pg.evaluate("scrollTo(0,0)"); pg.wait_for_timeout(400)
      pg.screenshot(path=f"{OUT}/{name}-full.png", full_page=True)
    res[name]=r; ctx.close()
  b.close()
print(json.dumps(res,indent=0))
