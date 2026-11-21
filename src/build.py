#!/usr/bin/env python3
"""Static site generator for galene.ie. Run: python3 src/build.py  -> writes to ./site"""
import os, shutil, html, datetime, urllib.parse, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site")
BASE = "https://galene.ie"
YEAR = datetime.date.today().year

COMPANY = dict(
    legal="Colgalene Solutions Ltd", trading="Galene", cro="819392", rbn="789698",
    vat="IE4757715FH", eori="IE4757715FH",
    addr="9 Slí Aonghusa, Áras Na Rí, Cashel, Co. Tipperary, E25 TF85, Ireland",
    email="info@galene.ie", phone="+353 89 213 2098", director="Colin Browne",
)

# ---------- products ----------
PRODUCTS = [
 dict(slug="ear-inserts", name="Noise-reducing ear inserts", short="Series 8",
  one="Take the edge off an open-plan office. Certified SNR 21 dB, reusable, in a case that fits a pocket.",
  intro="Open-plan offices are loud in a way that is hard to explain to people it does not bother. The Galene ear inserts lower the level without shutting you off: speech stays intelligible, the hum and the clatter drop back.",
  facts=[("Model","EN-Quietprop-S8 (Series 8)"),("Attenuation","SNR 21 dB · H 21 · M 19 · L 17 (EN 352-2:2020)"),
   ("Ear tips","XS 8 mm · S 10 mm · M 11 mm · L 12 mm, silicone, washable"),("Colours","Black. Midnight blue will follow once it is added to the certificate"),
   ("In the box","1 pair of inserts, ear tips in four sizes, carry case, leaflet (EN/DE/ES)"),
   ("Compliance","PPE Category III, Regulation (EU) 2016/425. EU type-examination: Aliénor Certification (NB 2754), certificate 2754/6256/159/06/25/0195. Production control: Certicore (NB 3232)"),],
  image="ear-inserts", caption="Carry case, render. Photographs of the inserts follow in December.", asin=None,
  safety="Hearing protectors reduce noise; they do not remove it. Fit as shown in the leaflet and wear them for the whole time you are in noise. They can make alarms and speech harder to hear. Small parts: for adults only, keep away from children. Not for sale to or use by children.",
  price=None),
 dict(slug="focus-glasses", name="Tinted focus glasses", short="28013 and G0601",
  one="A light yellow or tan tint in an ordinary adult frame, to soften screen glare and bright overhead lighting.",
  intro="Fluorescent light and a bright screen in a dim room wear people down over a day. These are not safety glasses and not a treatment: they are lightly tinted lenses (filter category 0) in a frame a colleague would not look twice at.",
  facts=[("Frames","28013 (black, grey) and G0601 (black)"),("Lenses","CR-39 resin with anti-reflective coating. H7MX light yellow (Tv 93 %) or H4M2 tan (Tv 90 %), filter category 0"),
   ("Standard","EN ISO 12312-1:2022 (test report pending, December 2026)"),("In the box","Glasses, cleaning cloth, sliding box"),
   ("Marking","Not suitable for driving"),],
  safety="The tint is visible: the lens is yellow or tan, not clear. Filter category 0. Not suitable for driving. These are not safety eyewear and give no impact protection.",
  price=None),
 dict(slug="weighted-lap-blanket", name="Weighted lap blanket", short="70 × 100 cm, 3 kg, and lap pad 48 × 56 cm, 2.3 kg",
  one="Steady, quiet weight for the desk or the sofa. Cotton outer, glass beads, removable cover. It reads as a knee throw, not a therapy aid.",
  intro="A weighted lap blanket is a simple thing: a quilted cotton blanket filled with fine glass beads, heavy enough to notice and light enough to move. Some people find it settles restlessness during long desk work. Adults only; no claims beyond that.",
  facts=[("Sizes","Blanket 70 × 100 cm, 3 kg · Lap pad 48 × 56 cm, 2.3 kg"),("Outer","Cotton, 5 × 5 cm square quilting, 7 layers, glass-bead fill (0.8–1 mm)"),
   ("Covers","Removable cotton covers in three colours (navy and two more, to be announced)"),("Textile safety","OEKO-TEX STANDARD 100, certificate 2021OK2653 (manufacturer)"),
   ("Care","Cover: washable. Blanket: see care label"),],
  safety="For adults. Not for children, infants or anyone who cannot remove the blanket themselves. Not flame retardant: keep away from open flames and heaters.",
  price=None),
 dict(slug="screen-light-bar", name="Screen light bar", short="FDGL01",
  one="Even light on the desk in front of your monitor, with no glare on the screen and a soft glow behind it. USB powered, 3000–6000 K, no visible flicker.",
  intro="The bar clips to the top edge of the monitor and lights the desk, not the screen. A warm-to-cool range and stepless dimming let you set it for the room; a back light takes the hard edge off a bright screen in a dim corner.",
  facts=[("Model","FDGL01, 42 cm, aluminium and ABS"),("Light","3000–6000 K in four modes, stepless dimming, CRI 81, no visible flicker"),
   ("Power","USB, 5 V DC 1 A, 5 W. Protection class III. No batteries. Power adapter not included"),("Energy label","Class G (EPREL 2533014, 5 kWh/1000 h)"),
   ("In the box","Light bar with monitor clip, USB cable, leaflet (EN/DE)"),("WEEE","Registered via Stiftung EAR, Germany: WEEE-Reg.-Nr. [TO CONFIRM]"),],
  image=None,  # set to "screen-light-bar" once Limi confirms in writing that Galene may use Founder's render (asked 3 Nov); file is already in assets/img/products
  caption="Manufacturer's render. Photographs of the Galene unit follow in December.", asin=None,
  safety="Indoor, dry use only. LEDs are not replaceable. Do not dispose of with household waste: electrical equipment goes to a collection point (crossed-out wheelie bin).",
  price=None),
 dict(slug="visual-timer", name="Visual timer", short="Analogue 60-minute countdown",
  one="A coloured disc that shrinks as the minutes pass. Silent mode for shared offices. No app, no screen, no notifications.",
  intro="Time can be hard to feel. Turn the dial, and the remaining time is visible from across the desk. A three-position switch gives a silent countdown or a low or high alarm.",
  facts=[("Form","Square white body with a navy silicone sleeve"),("Dial","0–60 minutes [TO CONFIRM], turn to set"),
   ("Sound","Mute, low, high"),("Power","2 × AAA batteries, not included"),("Status","Planned for early 2027")],
  safety="Not a toy. Keep batteries away from children. Dispose of batteries and the timer at a collection point, not in household waste.",
  price=None),
]

# ---------- doc page data ----------
DOCS = [
 dict(product="Noise-reducing ear inserts, model EN-Quietprop-S8", reg="Regulation (EU) 2016/425 (PPE), Category III",
  std="EN 352-2:2020", nb="EU type-examination: Aliénor Certification, NB 2754, certificate 2754/6256/159/06/25/0195 (valid to 1 June 2030). Production control: Certicore, NB 3232", status="Declaration will be published before the product goes on sale"),
 dict(product="Tinted focus glasses, models 28013 and G0601", reg="Regulation (EU) 2016/425 (PPE), Category I",
  std="EN ISO 12312-1:2022 + A11:2024 (traffic-signal recognition not tested; marked not suitable for driving); REACH Annex XVII", nb="Test reports expected December 2026", status="Declaration will be published when the test reports are received"),
 dict(product="Screen light bar, model FDGL01", reg="Directive 2014/30/EU (EMC); Directive 2011/65/EU (RoHS); Regulation (EU) 2019/2020 and 2019/2015 (ecodesign and energy labelling of light sources); Directive 2012/19/EU (WEEE)",
  std="EN 55015, EN 61547, EN IEC 63000; EPREL 2533014", nb="Not applicable (self-declaration)", status="Declaration will be published before the product goes on sale"),
 dict(product="Weighted lap blanket and covers", reg="Regulation (EU) 2023/988 (General Product Safety); Regulation (EU) 1007/2011 (textile fibre names)",
  std="OEKO-TEX STANDARD 100, 2021OK2653 (manufacturer's certificate)", nb="Not applicable", status="No CE marking applies. Safety information is on the care label and leaflet"),
 dict(product="Visual timer", reg="Directive 2014/30/EU (EMC); Directive 2011/65/EU (RoHS); Directive 2012/19/EU (WEEE); Regulation (EU) 2023/1542 (batteries)",
  std="[To be confirmed with the supplier's reports]", nb="Not applicable (self-declaration)", status="Planned product; declaration to follow"),
]

# ---------- layout ----------
CSS = """
:root{--tide:#0D5C7F;--tide-mid:#1478A0;--deep:#083A55;--teal:#2E7D8C;--seafoam:#A3C4C9;--linen:#F0EBE3;--white:#FAFAF8;--stone:#536770;--ink:#1C2B33;--sand:#C4A882;--line:#e2dcd2;color-scheme:light}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;text-size-adjust:100%;scroll-padding-top:100px}
body{margin:0;background:var(--linen);color:var(--ink);font:300 1.0625rem/1.65 "DM Sans",system-ui,sans-serif}
h1,h2,h3{font-family:Cinzel,serif;font-weight:500;color:var(--tide);letter-spacing:.04em;line-height:1.2;margin:0 0 .5em;text-wrap:balance}
h1{font-size:clamp(1.9rem,4vw,2.9rem)}h2{font-size:clamp(1.4rem,2.6vw,1.9rem)}h3,.h3{font-size:1.1rem}
a{color:var(--tide);text-underline-offset:.15em}p{margin:0 0 1em;text-wrap:pretty}
:focus-visible{outline:2px solid var(--tide);outline-offset:3px;border-radius:2px}.hero :focus-visible,footer :focus-visible{outline-color:var(--white)}
.skip{position:absolute;left:12px;top:-80px;background:var(--deep);color:var(--white);padding:10px 16px;border-radius:3px;z-index:10;text-decoration:none}.skip:focus{top:12px}
.vh{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{background:var(--linen);border-bottom:1px solid var(--line);position:sticky;top:0;z-index:5}
.hdr{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.hdr img{height:34px;width:auto;display:block}
nav{display:flex;gap:6px;font-size:.95rem}nav a{color:var(--stone);text-decoration:none;display:inline-flex;align-items:center;min-height:44px;padding:0 10px;border-bottom:2px solid transparent}nav a:hover{color:var(--tide)}nav a[aria-current]{color:var(--tide);border-bottom-color:var(--tide)}
.hero{background:radial-gradient(ellipse at 50% 60%,#1478A0 0%,#0D5C7F 78%);color:var(--white);position:relative;overflow:hidden;padding:88px 0 96px}.hero .wrap{position:relative}
.hero h1{color:var(--white)}.hero p{max-width:40rem;font-size:1.15rem}
.ripples{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}.ripple{position:absolute;border-radius:50%;border:1px solid rgba(163,196,201,.22)}.ripple:nth-child(1){width:180px;height:180px}.ripple:nth-child(2){width:400px;height:400px;opacity:.55}.ripple:nth-child(3){width:680px;height:680px;opacity:.28}.ripple:nth-child(4){width:1000px;height:1000px;opacity:.12}.hero-home{min-height:88vh;min-height:88svh;display:flex;align-items:center;text-align:center}.hero-home .wrap{display:flex;flex-direction:column;align-items:center}.hero-mark{width:64px;height:64px;margin-bottom:32px}.hero-title{font-family:Cinzel,serif;font-weight:400;font-size:clamp(2.6rem,9vw,8rem);letter-spacing:.28em;color:var(--white);line-height:1;margin:0 0 28px;padding-left:.28em}.hero-sub{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:300;font-size:clamp(1.3rem,2.5vw,1.9rem);color:var(--white);line-height:1.55;max-width:540px;margin:0 auto 40px}.quote{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:1.25rem;color:var(--stone)}
.eyebrow{font-size:.72rem;font-weight:500;letter-spacing:.42em;text-transform:uppercase;color:var(--white);margin-bottom:22px}
.cta{display:flex;gap:12px;flex-wrap:wrap}.hero-home .cta{justify-content:center}
.btn{display:inline-block;padding:12px 22px;border-radius:3px;text-decoration:none;font-weight:400;letter-spacing:.06em;font-size:.95rem}
.btn-sea{background:var(--seafoam);color:var(--deep)}.btn-sea:hover{background:var(--white)}
.btn-dark{background:var(--tide);color:var(--white)}.btn-dark:hover{background:var(--teal)}
.btn-ghost{border:1px solid rgba(250,250,248,.75);color:var(--white)}.btn-ghost:hover{border-color:var(--white);background:rgba(250,250,248,.08)}
.btn-soon{border:1px dashed rgba(250,250,248,.75);color:var(--white);cursor:default}
section{padding:64px 0}section.alt{background:var(--white)}
.grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.split{display:grid;gap:28px;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start}
.card{background:var(--white);border-left:3px solid var(--teal);padding:24px 24px 20px;display:flex;flex-direction:column;transition:transform .2s ease,box-shadow .2s ease}.card:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(8,58,85,.09)}
.card h2,.card h3{margin:0 0 .25em}.card .sub{color:var(--stone);font-size:.9rem;margin-bottom:.8em}.card p{flex:1}
.card a.more{text-decoration:none;font-size:.95rem;display:inline-flex;align-items:center;min-height:44px;margin-bottom:-10px}.card a.more:hover{text-decoration:underline}
.ph{background:var(--seafoam);aspect-ratio:4/3;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--deep);font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:18px}.ph-sq{aspect-ratio:1}
.ph-img{width:100%;height:auto;aspect-ratio:4/3;object-fit:contain;background:#fff;border-radius:3px;border:1px solid var(--line);display:block;margin-bottom:18px}.pfig{margin:0}.pfig img{width:100%;height:auto;aspect-ratio:1;object-fit:contain;background:#fff;border-radius:3px;border:1px solid var(--line);display:block}.pfig figcaption{margin-top:8px}
dl.facts{display:grid;grid-template-columns:max-content minmax(0,1fr);gap:8px 22px;margin:0}dl.facts dt{color:var(--stone);font-weight:400}dl.facts dd{margin:0;overflow-wrap:anywhere}
.note{background:var(--white);border-left:3px solid var(--sand);padding:16px 20px;margin:24px 0}
table{border-collapse:collapse;width:100%;font-size:.95rem}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid var(--line);overflow-wrap:anywhere}thead th{color:var(--stone);font-weight:400}tbody th{font-weight:500}tbody th a{display:inline-block;padding:4px 0}
footer{background:var(--deep);color:var(--seafoam);padding:48px 0 36px;font-size:.9rem}
footer img{height:30px;width:auto;margin-bottom:18px}footer a{color:var(--seafoam);display:inline-block;padding:4px 0}footer .cols{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}footer .tag{margin-top:28px}footer .quote{color:var(--seafoam)}footer .fine{font-size:.82rem}
.small{font-size:.85rem;color:var(--stone)}
.pts{display:grid;gap:28px 56px;grid-template-columns:repeat(auto-fit,minmax(min(100%,400px),1fr));margin-top:28px}.pts h3{margin-bottom:.35em}.pts p{margin:0}
.steps{list-style:none;padding:0;margin:28px 0 0;counter-reset:s;display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}.steps li{counter-increment:s;border-top:2px solid var(--teal);padding-top:14px}.steps li::before{content:counter(s,decimal-leading-zero);font-family:Cinzel,serif;font-size:1.5rem;color:var(--tide);display:block;margin-bottom:6px}.steps strong{font-weight:500}
.band{background:var(--deep);color:var(--white)}.band h2{color:var(--white)}.band p{max-width:44rem}.band .small{color:var(--seafoam)}.band a:not(.btn){color:var(--white)}.band :focus-visible{outline-color:var(--white)}
.lead{max-width:44rem;font-size:1.1rem}
@view-transition{navigation:auto}
@media(max-width:860px){.hero-home{min-height:70vh;min-height:70svh}.hdr{height:auto;padding:8px 20px 0;flex-wrap:wrap;gap:0 16px}.hdr img{height:24px}nav{width:100%;justify-content:space-between;gap:0;font-size:clamp(.72rem,3.5vw,.82rem)}nav a{padding:0}.hero{padding:60px 0 64px}.split{grid-template-columns:minmax(0,1fr)}dl.facts{grid-template-columns:minmax(0,1fr);gap:2px 0}dl.facts dd{margin-bottom:10px}
table,thead,tbody,tr,th,td{display:block}thead{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%)}tbody tr{background:var(--white);border-left:3px solid var(--teal);padding:14px 16px;margin-bottom:16px}tbody th,tbody td{border:0;padding:6px 0}td[data-label]::before{content:attr(data-label);display:block;font-size:.74rem;font-weight:500;letter-spacing:.08em;text-transform:uppercase;color:var(--stone)}}
@media(prefers-reduced-motion:reduce){.card{transition:none}.card:hover{transform:none}::view-transition-group(*),::view-transition-old(*),::view-transition-new(*){animation:none!important}}
"""

RINGS = '<div class="ripples" aria-hidden="true"><div class="ripple"></div><div class="ripple"></div><div class="ripple"></div><div class="ripple"></div></div>'
MARK = '<svg class="hero-mark" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="42" fill="none" stroke="#FAFAF8" stroke-width="8"/><line x1="16.534" y1="68" x2="83.466" y2="68" stroke="#FAFAF8" stroke-width="8"/><circle cx="50" cy="50" r="5" fill="#FAFAF8"/></svg>'

CSP = "default-src 'none'; style-src 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'; script-src 'inline-speculation-rules'; manifest-src 'self'; base-uri 'self'; form-action 'none'"
SPEC = '{"prefetch":[{"where":{"and":[{"href_matches":"/*"},{"not":{"selector_matches":"[rel~=nofollow]"}}]},"eagerness":"moderate"}]}'
FONTS = " ".join(open(os.path.join(ROOT,"assets","fonts","fonts.css"),encoding="utf-8").read().split())

NAV = [("Products","/products/"),("Employers","/employers/"),("Declarations","/doc/"),("Company","/company/"),("Contact","/contact/")]

LINKEDIN = "https://www.linkedin.com/company/galene-ie"
SUMMARY = "Workplace tools for neurodivergent professionals: noise, glare, restlessness and time, dealt with quietly at the desk."

def ld_tag(*objs):
    """JSON-LD data blocks (schema.org). Data only: not executed, so the CSP does not apply."""
    return "".join('<script type="application/ld+json">' + json.dumps(o, ensure_ascii=False, separators=(",",":")).replace("</","<\\/") + "</script>" for o in objs)

def org_ld():
    c = COMPANY
    return {"@context":"https://schema.org","@type":"Organization","@id":BASE+"/#org","name":"Galene","legalName":c["legal"],"url":BASE+"/",
      "logo":BASE+"/assets/img/icon-512.png","description":SUMMARY,"email":c["email"],"telephone":c["phone"],"vatID":c["vat"],
      "identifier":{"@type":"PropertyValue","propertyID":"CRO company number (Ireland)","value":c["cro"]},
      "founder":{"@type":"Person","name":c["director"]},
      "address":{"@type":"PostalAddress","streetAddress":"9 Slí Aonghusa, Áras Na Rí","addressLocality":"Cashel","addressRegion":"Co. Tipperary","postalCode":"E25 TF85","addressCountry":"IE"},
      "sameAs":[LINKEDIN]}

def product_ld(p):
    url = f"{BASE}/products/{p['slug']}/"
    props = [{"@type":"PropertyValue","name":k,"value":v} for k,v in p["facts"] if "[TO CONFIRM]" not in v]
    o = {"@context":"https://schema.org","@type":"Product","@id":url+"#product","name":p["name"],"description":p["one"]+" "+p["intro"],"url":url,
      "brand":{"@type":"Brand","name":"Galene"},"category":"Workplace tools for neurodivergent adults","additionalProperty":props}
    model = dict(p["facts"]).get("Model")
    if model: o["model"] = model
    if p.get("image"): o["image"] = f"{BASE}/assets/img/products/{p['image']}.jpg"
    crumbs = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
      {"@type":"ListItem","position":1,"name":"Galene","item":BASE+"/"},{"@type":"ListItem","position":2,"name":"Products","item":BASE+"/products/"},
      {"@type":"ListItem","position":3,"name":p["name"],"item":url}]}
    return ld_tag(o, crumbs)

def page(path, title, body, desc="", active="", ld=""):
    depth = path.count("/")
    here = "/" if path=="index.html" else "/"+os.path.dirname(path)+"/"
    nav = "".join(f'<a href="{h}"' + (' aria-current="page"' if h==here else ' aria-current="true"' if n==active else "") + f'>{n}</a>' for n,h in NAV)
    canonical = BASE + here
    canon_tag = f'<link rel="canonical" href="{canonical}">' if path!="404.html" else ""
    og = f'<meta property="og:type" content="website"><meta property="og:site_name" content="Galene"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{BASE}/assets/img/icon-512.png"><meta name="twitter:card" content="summary">' if path!="404.html" else '<meta name="robots" content="noindex">'
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}">{canon_tag}
<link rel="icon" href="/assets/img/favicon.ico" sizes="32x32"><link rel="icon" href="/assets/img/favicon-32.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<meta http-equiv="Content-Security-Policy" content="{CSP}"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="theme-color" content="#F0EBE3"><meta name="color-scheme" content="light">{og}
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/DMSans-normal-400-latin.woff2" crossorigin><link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Cinzel-normal-400-latin.woff2" crossorigin>
<style>{FONTS}{CSS}</style>
<script type="speculationrules">{SPEC}</script>{ld}</head><body>
<a class="skip" href="#main">Skip to content</a>
<header><div class="wrap hdr"><a href="/"><img src="/assets/img/galene-lockup-horizontal-tide.svg" alt="Galene home" width="277" height="34"></a><nav aria-label="Main">{nav}</nav></div></header>
<main id="main">
{body}
</main>
<footer><div class="wrap"><img src="/assets/img/galene-lockup-horizontal-linen.svg" alt="Galene" width="244" height="30" loading="lazy"><div class="cols">
<div><strong>{COMPANY['legal']}</strong>, trading as Galene<br>{COMPANY['addr']}<br>CRO {COMPANY['cro']} · VAT {COMPANY['vat']}</div>
<div><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a><br>{COMPANY['phone']}</div>
<div><a href="/employers/">For employers</a><br><a href="/doc/">Declarations of conformity</a><br><a href="/company/">Company information</a><br><a href="/privacy/">Privacy</a></div>
</div><p class="tag">Calm at Work · Ireland<br><span class="quote"><span lang="el">Γαλήνη</span> — the nereid who stilled the seas.</span></p><p class="fine">© {YEAR} {COMPANY['legal']}, trading as Galene. Built for the way your brain works.</p></div></footer>
</body></html>"""
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,"w",encoding="utf-8").write(doc)

def hero(eyebrow, h1, p, ctas=""):
    return f'<div class="hero">{RINGS}<div class="wrap"><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{p}</p>{ctas}</div></div>'

def product_card(p, tag="h3"):
    b = f'/assets/img/products/{p.get("image")}-card'
    img = f'<picture><source type="image/webp" srcset="{b}-half.webp 480w, {b}.webp 960w" sizes="(max-width:860px) 90vw, 330px"><img class="ph-img" src="{b}.jpg" alt="" loading="lazy" decoding="async" width="960" height="720"></picture>' if p.get("image") else '<div class="ph">Photo to follow</div>'
    cls = ' class="h3"' if tag!="h3" else ""
    return f'<article class="card">{img}<{tag}{cls}>{p["name"]}</{tag}><div class="sub">{p["short"]}</div><p>{p["one"]}</p><a class="more" href="/products/{p["slug"]}/">Details<span class="vh">: {p["name"]}</span>&nbsp;<span aria-hidden="true">→</span></a></article>'

def product_figure(p):
    if not p.get("image"): return '<div class="ph ph-sq">Photo to follow</div>'
    cap = f'<figcaption class="small">{html.escape(p["caption"])}</figcaption>' if p.get("caption") else ''
    b = f'/assets/img/products/{p["image"]}'
    return f'<figure class="pfig"><picture><source type="image/webp" srcset="{b}-half.webp 600w, {b}.webp 1200w" sizes="(max-width:860px) 90vw, 500px"><img src="{b}.jpg" alt="{html.escape(p["name"])}" width="1200" height="1200" fetchpriority="high"></picture>{cap}</figure>'

def buy_button(p):
    if p.get("asin"):
        return f'<a class="btn btn-sea" href="https://www.amazon.de/dp/{p["asin"]}" rel="noopener">Buy on Amazon.de</a>'
    if p["slug"]=="visual-timer": return '<span class="btn btn-soon">Planned for early 2027 · not yet on sale</span>'
    return '<span class="btn btn-soon">On Amazon.de from January 2027</span>'

def build():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT); shutil.copytree(os.path.join(ROOT,"assets"), os.path.join(OUT,"assets"))
    open(os.path.join(OUT,"CNAME"),"w").write("galene.ie\n")
    open(os.path.join(OUT,".nojekyll"),"w").write("")
    # home
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = f'<div class="hero hero-home">{RINGS}<div class="wrap">{MARK}<div class="eyebrow">Named for the goddess of calm seas</div><h1 class="hero-title">Galene</h1><p class="hero-sub">Built for the way your brain works — wherever you work.</p><p class="cta"><a class="btn btn-sea" href="/products/">See the products</a><a class="btn btn-ghost" href="/company/">About the company</a></p></div></div>'
    body += '<section class="alt"><div class="wrap"><p style="max-width:44rem;font-size:1.1rem">Workplace tools for neurodivergent professionals: noise, glare, restlessness and time, dealt with quietly at the desk. Launching on Amazon.de in January 2027.</p></div></section>'
    body += f'<section><div class="wrap"><h2>The products</h2><p style="max-width:44rem">Five things chosen for one reason each. Nothing medical, nothing that looks out of place on a desk.</p><div class="grid">{cards}</div></div></section>'
    body += '<section class="band"><div class="wrap"><h2>For employers</h2><p>A reasonable adjustment is often a small one: less noise, softer light, a way to see time passing. Galene supplies the tools with the compliance paperwork your health and safety or procurement team needs to approve them.</p><p class="cta"><a class="btn btn-sea" href="/employers/">How it works for employers</a></p></div></section>'
    body += '<section class="alt"><div class="wrap"><h2>Why these five</h2><p style="max-width:44rem">Open-plan noise, screen glare, restlessness and time-blindness are four of the most common difficulties neurodivergent adults describe at work. Each product answers one of them with an ordinary object, chosen for its certification and build rather than for claims. We say what a product does and what it is tested to, and no more.</p></div></section>'
    page("index.html","Galene — built for the way your brain works", body, "Workplace tools for neurodivergent professionals. Ear inserts, tinted focus glasses, weighted lap blanket, screen light bar and visual timer. Launching on Amazon.de January 2027.",
         ld=ld_tag(org_ld(), {"@context":"https://schema.org","@type":"WebSite","name":"Galene","url":BASE+"/","publisher":{"@id":BASE+"/#org"},"inLanguage":"en-IE"}))
    # products index
    body = hero("Products","Five tools, one job each.","Available on Amazon.de from January 2027. Each page lists what the product is, what it is tested to, and the safety information that goes with it.")
    cards2 = "".join(product_card(p, "h2") for p in PRODUCTS)
    body += f'<section><div class="wrap"><div class="grid">{cards2}</div></div></section>'
    page("products/index.html","Products — Galene", body, "Galene products: ear inserts, tinted focus glasses, weighted lap blanket, screen light bar, visual timer.", "Products")
    for p in PRODUCTS:
        facts = "".join(f"<dt>{k}</dt><dd>{html.escape(v)}</dd>" for k,v in p["facts"])
        body = hero(p["short"], p["name"], p["one"], buy_button(p))
        body += f'<section><div class="wrap"><div class="split"><div>{product_figure(p)}</div><div><p>{p["intro"]}</p><h2 class="h3">Details</h2><dl class="facts">{facts}</dl></div></div>'
        body += f'<div class="note"><strong>Safety information.</strong> {p["safety"]}</div><p class="small">Declaration of conformity and test documentation: <a href="/doc/">galene.ie/doc</a>. Manufacturer and EU responsible person details: <a href="/company/">company information</a>.</p></div></section>'
        page(f"products/{p['slug']}/index.html", f"{p['name']} — Galene", body, p["one"], "Products", ld=product_ld(p))
    # employers
    def mail(subject, lines):
        return "mailto:" + COMPANY["email"] + "?subject=" + urllib.parse.quote(subject) + "&body=" + urllib.parse.quote("\n".join(lines) + "\n")
    fields = ["Name:", "Employer:", "Your role:", "Number of employees:", "Anything we should know:"]
    m_kit = mail("Sample kit request", ["I would like a Galene sample kit to assess.", ""] + fields)
    m_pilot = mail("Pilot enquiry", ["I would like to ask about a Galene pilot.", "", "Site or team, and approximate number of people:"] + fields)
    body = hero("For employers","Small, practical tools for the desks where work is harder than it needs to be.","Open-plan noise, harsh lighting, long stretches at a screen and time that slips away are everyday obstacles for many employees, and for neurodivergent colleagues in particular. Galene supplies discreet, adult desk tools that deal with each of these, with the compliance paperwork an employer needs to approve them.",
        f'<p class="cta"><a class="btn btn-sea" href="{m_kit}">Request a sample kit</a><a class="btn btn-ghost" href="{m_pilot}">Ask about a pilot</a></p>')
    body += """<section class="alt"><div class="wrap"><h2>Why employers use Galene</h2><div class="pts">
<div><h3>An adjustment you can make quickly</h3><p>Employers in Ireland and across the EU have a duty to provide reasonable accommodation. Most requests are small: less noise, softer light, a way to see time passing. These are tools for exactly that, at a cost that rarely needs a business case.</p></div>
<div><h3>Paperwork included</h3><p>Each product is supplied with its declaration of conformity and a one-page specification your health and safety or procurement team can file. The list of regulations and standards is public at <a href="/doc/">galene.ie/doc</a>.</p></div>
<div><h3>One supplier, one invoice</h3><p>An Irish company, registered in Cashel, Co. Tipperary, invoicing in euro with Irish VAT.</p></div>
<div><h3>Discreet by design</h3><p>Plain colours, no slogans, nothing that singles a person out. Nothing in the range looks like a medical aid or a toy.</p></div>
</div></div></section>"""
    RANGE = [("ear-inserts","Taking the edge off open-plan noise while speech stays intelligible","Certified hearing protection, SNR 21 dB (EN 352-2:2020). PPE Category III. Reusable, four tip sizes, pocket case. Black"),
     ("focus-glasses","Softening screen glare and bright overhead lighting","Light yellow or tan tint, filter category 0, in an ordinary adult frame. Not suitable for driving. Not safety eyewear"),
     ("screen-light-bar","Even light on the desk without glare on the screen","USB powered, 3000–6000 K, stepless dimming, no visible flicker. Energy class G"),
     ("weighted-lap-blanket","Steady, quiet weight during long desk work","Cotton with glass-bead fill and a removable cover. Blanket 70 × 100 cm, 3 kg; lap pad 48 × 56 cm, 2.3 kg. For adults"),
     ("visual-timer","Making the time that is left visible at a glance","Analogue countdown with a silent mode. Planned for early 2027")]
    names = {p["slug"]: p["name"] for p in PRODUCTS}
    rrows = "".join(f"<tr role=row><th scope=row role=rowheader><a href='/products/{sl}/'>{names[sl]}</a></th><td role=cell data-label='What it is for'>{w}</td><td role=cell data-label='Key facts'>{k}</td></tr>" for sl,w,k in RANGE)
    body += f"""<section><div class="wrap"><h2>The range</h2><p class="lead">Five tools, one job each. Full specifications and safety information are on each product page.</p>
<table role="table" aria-label="The Galene range"><thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Tool</th><th role="columnheader" scope="col">What it is for</th><th role="columnheader" scope="col">Key facts</th></tr></thead><tbody role="rowgroup">{rrows}</tbody></table></div></section>"""
    body += """<section class="alt"><div class="wrap"><h2>How it works</h2><ol class="steps">
<li><strong>Sample kit.</strong> Tell us who you are and we send one set of the range to a named HR, occupational health or facilities contact to assess. Kits ship from March 2027, when our Irish stock arrives; you can reserve one now.</li>
<li><strong>Pilot.</strong> 10 to 25 units, any mix, for one site, team or employee network, at a fixed price on one invoice. After six weeks we send a short anonymous survey and share the results with you.</li>
<li><strong>Ongoing supply.</strong> Employees or managers request what they need and you receive one monthly invoice. Volume prices apply from 10 units.</li>
</ol><p class="lead" style="margin-top:36px"><strong>Prices.</strong> Pilot and volume prices are quoted on request, excluding VAT, on one invoice.</p></div></section>"""
    body += """<section><div class="wrap"><div class="note"><strong>What we do not claim.</strong> These are everyday desk tools. They are not medical devices, and we make no claim that they treat or improve any condition. The ear inserts are certified hearing protection and the stated attenuation is the certified figure. Where a product has limits, for example that the glasses are not for driving, we say so on the product page and on the pack.</div></div></section>"""
    FAQ = [
     ("What does Galene supply to employers?", "Five desk tools, one job each: noise-reducing ear inserts, tinted focus glasses, a screen light bar, a weighted lap blanket and a visual timer. They deal with open-plan noise, glare, restlessness and losing track of time, and are supplied with the compliance paperwork an employer needs to approve them."),
     ("Who are the products for?", "Adults at work. They were chosen with neurodivergent employees in mind, and any employee who finds noise, lighting or time hard to manage at a desk can use them."),
     ("Are these medical devices?", "No. They are everyday desk tools. They are not medical devices and we make no claim that they treat or improve any condition. The ear inserts are certified hearing protection, and the attenuation we state is the certified figure."),
     ("Can they be used as a reasonable accommodation?", "Employers in Ireland and across the EU have a duty to provide reasonable accommodation, and most requests are small: less noise, softer light, a way to see time passing. These tools are meant for exactly that. Whether a particular adjustment is right for an employee is for the employer and the employee to decide."),
     ("What paperwork comes with the products?", "Each product is supplied with its declaration of conformity and a one-page specification for your health and safety or procurement file. The regulations and standards for every product are listed publicly at galene.ie/doc."),
     ("How much does it cost?", "Pilot and volume prices are quoted on request, excluding VAT, on one invoice. Volume prices apply from 10 units. Email info@galene.ie with your employer name and approximate headcount for a quote."),
     ("Can we try the products before ordering?", "Yes. We send one sample kit of the range to a named HR, occupational health or facilities contact to assess. Kits ship from March 2027, when our Irish stock arrives, and can be reserved now."),
     ("How does a pilot work?", "A pilot is 10 to 25 units in any mix, for one site, team or employee network, at a fixed price on one invoice. After six weeks we send a short anonymous survey and share the results with you."),
     ("When are the products available?", "The range launches on Amazon.de in January 2027. Employer sample kits ship from March 2027. The visual timer is planned for early 2027 and is not yet on sale."),
     ("Who is behind Galene?", f"Galene is the trading name of {COMPANY['legal']}, an Irish company registered in Cashel, Co. Tipperary (CRO {COMPANY['cro']}, VAT {COMPANY['vat']}). It invoices in euro with Irish VAT and is the EU responsible person for every Galene product."),
    ]
    faq_html = "".join(f"<div><h3>{html.escape(q)}</h3><p>{html.escape(a)}</p></div>" for q,a in FAQ)
    body += f'<section class="alt"><div class="wrap"><h2>Questions employers ask</h2><div class="pts">{faq_html}</div></div></section>'
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
    body += f"""<section class="band"><div class="wrap"><h2>Start with an email</h2><p>Tell us your name, your employer, your role and roughly how many people you employ, and whether you would like a sample kit or a pilot quote. We reply within two working days.</p>
<p class="cta"><a class="btn btn-sea" href="{m_kit}">Request a sample kit</a><a class="btn btn-ghost" href="{m_pilot}">Ask about a pilot</a></p>
<p class="small">Or write to <a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a>. We use your details only to reply to your request. See our <a href="/privacy/">privacy notice</a>.</p></div></section>"""
    page("employers/index.html","For employers — Galene", body, "Workplace adjustment tools for employers: noise, glare, restlessness and time. Sample kits, pilots and one invoice from an Irish supplier.", "Employers", ld=ld_tag(faq_ld))
    # doc
    rows = "".join(f"<tr role=row><th scope=row role=rowheader>{d['product']}</th><td role=cell data-label='EU legislation'>{d['reg']}</td><td role=cell data-label='Standards and certificates'>{d['std']}</td><td role=cell data-label='Notified body'>{d['nb']}</td><td role=cell data-label='Declaration'>{d['status']}</td></tr>" for d in DOCS)
    body = hero("galene.ie/doc","Declarations of conformity","This is the address printed on Galene packaging. Each product's EU declaration of conformity, the regulations it is declared against and the standards applied are listed here, with a PDF of the signed declaration once the product is on sale.")
    body += f'<section><div class="wrap"><table role="table" aria-label="Declarations of conformity by product"><thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Product</th><th role="columnheader" scope="col">EU legislation</th><th role="columnheader" scope="col">Standards and certificates</th><th role="columnheader" scope="col">Notified body</th><th role="columnheader" scope="col">Declaration</th></tr></thead><tbody role="rowgroup">{rows}</tbody></table>'
    body += f'<div class="note"><strong>Manufacturer and EU responsible person.</strong> {COMPANY["legal"]}, trading as Galene, {COMPANY["addr"]}. {COMPANY["email"]} · {COMPANY["phone"]}. For the ear inserts, Colgalene Solutions Ltd is the manufacturer placing the product on the market under its own name. For the other products, the manufacturer is named on the product or its packaging and Colgalene Solutions Ltd is the importer and EU responsible person under Regulation (EU) 2019/1020.</div>'
    body += '<p class="small">To request a copy of a declaration or a test report before it is published here, email the address above with the product name and model.</p></div></section>'
    page("doc/index.html","Declarations of conformity — Galene", body, "EU declarations of conformity for Galene products.", "Declarations")
    # company
    c = COMPANY
    body = hero("Company information","Colgalene Solutions Ltd, trading as Galene","A private company limited by shares, registered in Ireland. Owner and director: Colin Browne.")
    body += f'''<section><div class="wrap"><div class="split"><div><h2 class="h3">Registered details</h2><dl class="facts">
<dt>Legal name</dt><dd>{c["legal"]}</dd><dt>Trading as</dt><dd>Galene (registered business name {c["rbn"]})</dd><dt>Company number</dt><dd>CRO {c["cro"]}, Companies Registration Office, Ireland</dd>
<dt>Registered office</dt><dd>{c["addr"]}</dd><dt>VAT number</dt><dd>{c["vat"]}</dd><dt>EORI</dt><dd>{c["eori"]}</dd><dt>Director</dt><dd>{c["director"]}</dd>
<dt>Email</dt><dd><a href="mailto:{c["email"]}">{c["email"]}</a></dd><dt>Telephone</dt><dd>{c["phone"]}</dd></dl></div>
<div><h2 class="h3" lang="de">Angaben gemäß § 5 DDG</h2><p lang="de">{c["legal"]} (Handelsname Galene)<br>{c["addr"]}<br>Vertreten durch den Director: {c["director"]}<br>E-Mail: {c["email"]} · Telefon: {c["phone"]}<br>Registergericht: Companies Registration Office (CRO), Irland, Nr. {c["cro"]}<br>USt-IdNr. (Irland): {c["vat"]}<br>Deutsche USt-IdNr.: wird nach Erteilung ergänzt<br>WEEE-Reg.-Nr. (Stiftung EAR): wird nach Erteilung ergänzt<br>Verpackungsregister LUCID: wird nach Erteilung ergänzt</p>
<p lang="de" class="small">Plattform der EU-Kommission zur Online-Streitbeilegung: <a href="https://ec.europa.eu/consumers/odr">ec.europa.eu/consumers/odr</a>. Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p></div></div>
<h2 class="h3" style="margin-top:40px">Roles under EU product law</h2><p style="max-width:48rem">Colgalene Solutions Ltd is the EU responsible person (Regulation (EU) 2019/1020, Article 4) for every Galene product, and the manufacturer of the Galene ear inserts, which are placed on the market under our own name. Declarations of conformity are at <a href="/doc/">galene.ie/doc</a>.</p></div></section>'''
    page("company/index.html","Company information — Galene", body, "Colgalene Solutions Ltd, trading as Galene: registered details, Impressum, EU responsible person.", "Company", ld=ld_tag(org_ld()))
    # privacy
    body = hero("Privacy","Privacy notice","Short, because this site collects almost nothing.")
    body += f'''<section><div class="wrap" style="max-width:48rem"><p><strong>Controller.</strong> {c["legal"]}, {c["addr"]}, {c["email"]}.</p>
<p><strong>This website.</strong> It is a static site hosted on GitHub Pages (GitHub, Inc.). It sets no cookies and runs no analytics or tracking scripts. The host records standard server logs (IP address, time, page requested) for security, under GitHub's own privacy statement. Fonts are served from this site; nothing is loaded from third-party servers.</p>
<p><strong>Email.</strong> If you write to us, we keep your message and our reply for as long as needed to deal with it and for our records (legal basis: Article 6(1)(b) and (f) GDPR). Our email is hosted by Google Workspace (Google Ireland Ltd).</p>
<p><strong>Purchases.</strong> Orders are placed on Amazon. Amazon is the controller for the order data it collects. We receive only what is needed to fulfil the order and to handle returns and safety obligations, and keep it for the periods required by tax and product-safety law.</p>
<p><strong>Your rights.</strong> Access, rectification, erasure, restriction, portability and objection, by email to {c["email"]}. You may complain to the Data Protection Commission (dataprotection.ie) or your local supervisory authority.</p>
<p class="small">Last updated {datetime.date.today():%-d %B %Y}.</p></div></section>'''
    page("privacy/index.html","Privacy — Galene", body, "Privacy notice for galene.ie.", "")
    # contact
    body = hero("Contact","Get in touch","For product questions, safety information, trade enquiries or anything about an order.")
    body += f'''<section><div class="wrap" style="max-width:48rem"><dl class="facts"><dt>Email</dt><dd><a href="mailto:{c["email"]}">{c["email"]}</a></dd><dt>Telephone</dt><dd>{c["phone"]} (Ireland, business hours)</dd><dt>Post</dt><dd>{c["legal"]}, {c["addr"]}</dd></dl>
<div class="note"><strong>Product safety.</strong> If you believe a Galene product is unsafe or has a fault, email us with the product name, the batch code on the packaging and a description. We respond to safety reports within two working days.</div></div></section>'''
    page("contact/index.html","Contact — Galene", body, "Contact Galene / Colgalene Solutions Ltd.", "Contact")
    # 404
    page("404.html","Page not found — Galene", hero("404","Page not found","Try the <a href='/' style='color:#F0EBE3'>home page</a> or <a href='/doc/' style='color:#F0EBE3'>declarations</a>."), "")
    urls = ["/"] + [h for _,h in NAV] + [f"/products/{p['slug']}/" for p in PRODUCTS] + ["/privacy/"]
    open(os.path.join(OUT,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc></url>" for u in urls) + "</urlset>\n")
    open(os.path.join(OUT,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n")
    c = COMPANY
    L = ["# Galene", "", f"> {SUMMARY} Galene is the trading name of {c['legal']}, an Irish company in Cashel, Co. Tipperary. The range launches on Amazon.de in January 2027; employer sample kits ship from March 2027.", "",
      "Galene sells five everyday desk tools for adults. They are not medical devices and Galene makes no claim that they treat or improve any condition. Prices are not yet published: employer pilot and volume prices are quoted on request.", "",
      "## Products", ""]
    for p in PRODUCTS:
        L.append(f"- [{p['name']}]({BASE}/products/{p['slug']}/): {p['one']}")
        L += [f"  - {k}: {v}" for k,v in p["facts"] if "[TO CONFIRM]" not in v]
        L.append(f"  - Safety: {p['safety']}")
    L += ["", "## For employers", "", f"- [For employers]({BASE}/employers/): sample kits, pilots of 10 to 25 units, ongoing supply on one monthly invoice, and the compliance paperwork for each product."]
    L += [f"- {q} {a}" for q,a in FAQ]
    L += ["", "## Compliance and company", "",
      f"- [Declarations of conformity]({BASE}/doc/): EU legislation, standards, certificates and notified bodies for each product.",
      f"- [Company information]({BASE}/company/): {c['legal']}, trading as Galene. CRO {c['cro']}, VAT {c['vat']}, EORI {c['eori']}. Registered office: {c['addr']}. Director: {c['director']}. EU responsible person for every Galene product.",
      f"- [Contact]({BASE}/contact/): {c['email']}, {c['phone']}.",
      f"- [Privacy]({BASE}/privacy/): static site, no cookies, no analytics.", ""]
    open(os.path.join(OUT,"llms.txt"),"w",encoding="utf-8").write("\n".join(L))
    print("built", sum(len(f) for _,_,f in os.walk(OUT)), "files")

if __name__ == "__main__":
    build()
