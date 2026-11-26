"""usage: shot.py url out.png width [full|view|sel:<css>] — scrolls to load lazy images, reports errors/overflow/images/links"""
import sys, asyncio, json
from playwright.async_api import async_playwright
async def main():
    url,out,w=sys.argv[1],sys.argv[2],int(sys.argv[3]); mode=sys.argv[4] if len(sys.argv)>4 else 'full'
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':w,'height':1000 if w>600 else 844},device_scale_factor=2 if mode.startswith('sel:') else 1)
        errs=[]
        pg.on('console',lambda m: errs.append(m.text) if m.type in('error','warning') else None)
        pg.on('pageerror',lambda e: errs.append(str(e)))
        pg.on('requestfailed',lambda r: errs.append('REQFAIL '+r.url))
        pg.on('response',lambda r: errs.append(f'HTTP{r.status} {r.url}') if r.status>=400 else None)
        await pg.goto(url,wait_until='networkidle')
        H=await pg.evaluate('document.documentElement.scrollHeight')
        for y in range(0,H,600):
            await pg.evaluate(f'window.scrollTo(0,{y})'); await pg.wait_for_timeout(60)
        await pg.evaluate('window.scrollTo(0,0)'); await pg.wait_for_timeout(700)
        info=await pg.evaluate("""()=>{const W=document.documentElement.clientWidth;
          const imgs=[...document.images];const bad=imgs.filter(i=>!(i.complete&&i.naturalWidth>0)).map(i=>i.src);
          const az=[...document.querySelectorAll('a[href*="amazon."]')];
          return {sw:document.documentElement.scrollWidth,W,imgs:imgs.length,badimgs:bad,
           amazon:az.length,tagged:az.filter(a=>a.href.includes('tag=petpolicychec-20')).length,
           relok:az.filter(a=>/sponsored/.test(a.rel)&&/nofollow/.test(a.rel)).length,
           illus:document.querySelectorAll('.pp-illus').length,cards:document.querySelectorAll('.pp-card').length}}""")
        if mode=='full': await pg.screenshot(path=out,full_page=True)
        elif mode=='view': await pg.screenshot(path=out)
        else:
            el=pg.locator(mode[4:]).first; await el.scroll_into_view_if_needed(); await pg.wait_for_timeout(300); await el.screenshot(path=out)
        print(json.dumps({'errors':errs,**info}))
        await b.close()
asyncio.run(main())
