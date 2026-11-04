#!/usr/bin/env python3
"""Static site generator for galene.ie. Run: python3 src/build.py  -> writes to ./site"""
import os, shutil, html, datetime
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
:root{--tide:#0D5C7F;--tide-mid:#1680A6;--deep:#083A55;--teal:#2E7D8C;--seafoam:#A3C4C9;--linen:#F0EBE3;--white:#FAFAF8;--stone:#6B8089;--ink:#1C2B33;--sand:#C4A882}
*{box-sizing:border-box}
body{margin:0;background:var(--linen);color:var(--ink);font:300 17px/1.65 "DM Sans",system-ui,sans-serif}
h1,h2,h3{font-family:Cinzel,serif;font-weight:500;color:var(--tide);letter-spacing:.04em;line-height:1.2;margin:0 0 .5em}
h1{font-size:clamp(1.9rem,4vw,2.9rem)}h2{font-size:clamp(1.4rem,2.6vw,1.9rem)}h3{font-size:1.1rem}
a{color:var(--tide)}p{margin:0 0 1em}
.wrap{max-width:1080px;margin:0 auto;padding:0 20px}
header{background:var(--linen);border-bottom:1px solid #e2dcd2;position:sticky;top:0;z-index:5}
.hdr{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.hdr img{height:34px;display:block}
nav{display:flex;gap:22px;font-size:.95rem}nav a{color:var(--stone);text-decoration:none}nav a:hover,nav a.on{color:var(--tide)}
.hero{background:radial-gradient(ellipse at 50% 60%,#2BAFC9 0%,#1478A0 68%);color:var(--white);position:relative;overflow:hidden;padding:88px 0 96px}.hero .wrap{position:relative}
.hero h1{color:var(--white)}.hero p{max-width:40rem;font-size:1.15rem;opacity:.92}
.ripples{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;pointer-events:none}.ripple{position:absolute;border-radius:50%;border:1px solid rgba(163,196,201,.18)}.ripple:nth-child(1){width:180px;height:180px}.ripple:nth-child(2){width:400px;height:400px;opacity:.55}.ripple:nth-child(3){width:680px;height:680px;opacity:.28}.ripple:nth-child(4){width:1000px;height:1000px;opacity:.12}.hero-home{min-height:88vh;display:flex;align-items:center;text-align:center}.hero-home .wrap{display:flex;flex-direction:column;align-items:center}.hero-mark{width:64px;height:64px;margin-bottom:32px}.hero-title{font-family:Cinzel,serif;font-weight:400;font-size:clamp(3.2rem,9vw,8rem);letter-spacing:.28em;color:var(--white);line-height:1;margin:0 0 28px;padding-left:.28em}.hero-sub{font-family:"Cormorant Garamond",serif;font-style:italic;font-weight:300;font-size:clamp(1.25rem,2.5vw,1.9rem);color:rgba(255,255,255,.88);line-height:1.55;max-width:540px;margin:0 auto 40px}.quote{font-family:"Cormorant Garamond",serif;font-style:italic;font-size:1.25rem;color:var(--stone)}
.eyebrow{font-size:.68rem;font-weight:500;letter-spacing:.42em;text-transform:uppercase;color:rgba(255,255,255,.82);margin-bottom:22px}
.btn{display:inline-block;padding:12px 22px;border-radius:3px;text-decoration:none;font-weight:400;letter-spacing:.06em;font-size:.95rem}
.btn-sea{background:var(--seafoam);color:var(--deep)}.btn-sea:hover{background:var(--white)}
.btn-dark{background:var(--tide);color:var(--white)}.btn-dark:hover{background:var(--teal)}
.btn-ghost{border:1px solid var(--seafoam);color:var(--white)}.btn-ghost:hover{border-color:var(--white)}
.btn[aria-disabled]{opacity:.55;cursor:default}
section{padding:64px 0}section.alt{background:var(--white)}
.grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
.card{background:var(--white);border-left:3px solid var(--teal);padding:24px 24px 20px;display:flex;flex-direction:column}
.card h3{margin-bottom:.25em}.card .sub{color:var(--stone);font-size:.9rem;margin-bottom:.8em}.card p{flex:1}
.card a.more{text-decoration:none;font-size:.95rem}
.ph{background:var(--seafoam);aspect-ratio:4/3;border-radius:3px;display:flex;align-items:center;justify-content:center;color:var(--deep);font-size:.85rem;letter-spacing:.1em;text-transform:uppercase;margin-bottom:18px}
dl.facts{display:grid;grid-template-columns:max-content 1fr;gap:8px 22px;margin:0}dl.facts dt{color:var(--stone);font-weight:400}dl.facts dd{margin:0}
.note{background:var(--white);border-left:3px solid var(--sand);padding:16px 20px;margin:24px 0}
table{border-collapse:collapse;width:100%;font-size:.95rem}th,td{text-align:left;vertical-align:top;padding:10px 12px;border-bottom:1px solid #e2dcd2}th{color:var(--stone);font-weight:400}
footer{background:var(--deep);color:var(--seafoam);padding:48px 0 36px;font-size:.9rem}
footer img{height:30px;margin-bottom:18px}footer a{color:var(--seafoam)}footer .cols{display:grid;gap:24px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}
.small{font-size:.85rem;color:var(--stone)}
@media(max-width:720px){.hero-home{min-height:70vh}.hdr{height:auto;padding:10px 20px;flex-wrap:wrap}.hdr img{height:24px}nav{gap:12px;font-size:.82rem;flex-wrap:wrap}.hero{padding:60px 0 64px}.rings{display:none}dl.facts{grid-template-columns:1fr}}
"""

RINGS = '<div class="ripples" aria-hidden="true"><div class="ripple"></div><div class="ripple"></div><div class="ripple"></div><div class="ripple"></div></div>'
MARK = '<svg class="hero-mark" viewBox="0 0 100 100" aria-hidden="true"><circle cx="50" cy="50" r="42" fill="none" stroke="#FAFAF8" stroke-width="8"/><line x1="16.534" y1="68" x2="83.466" y2="68" stroke="#FAFAF8" stroke-width="8"/><circle cx="50" cy="50" r="5" fill="#FAFAF8"/></svg>'

NAV = [("Products","/products/"),("Declarations","/doc/"),("Company","/company/"),("Contact","/contact/")]

def page(path, title, body, desc="", active=""):
    depth = path.count("/")
    nav = "".join(f'<a href="{h}"{" class=on" if n==active else ""}>{n}</a>' for n,h in NAV)
    canonical = BASE + ("/" if path=="index.html" else "/"+os.path.dirname(path)+"/")
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{canonical}">
<link rel="icon" href="/assets/img/favicon.ico" sizes="32x32"><link rel="icon" href="/assets/img/favicon-32.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="/assets/img/icon-180.png">
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<style>{CSS}</style></head><body>
<header><div class="wrap hdr"><a href="/"><img src="/assets/img/galene-lockup-horizontal-tide.svg" alt="Galene"></a><nav>{nav}</nav></div></header>
{body}
<footer><div class="wrap"><img src="/assets/img/galene-lockup-horizontal-linen.svg" alt="Galene"><div class="cols">
<div><strong>{COMPANY['legal']}</strong>, trading as Galene<br>{COMPANY['addr']}<br>CRO {COMPANY['cro']} · VAT {COMPANY['vat']}</div>
<div><a href="mailto:{COMPANY['email']}">{COMPANY['email']}</a><br>{COMPANY['phone']}</div>
<div><a href="/doc/">Declarations of conformity</a><br><a href="/company/">Company information</a><br><a href="/privacy/">Privacy</a></div>
</div><p style="margin-top:28px;opacity:.85">Calm at Work · Ireland<br><span class="quote" style="color:var(--seafoam)">Γαλήνη — the nereid who stilled the seas.</span></p><p style="opacity:.6">© {YEAR} {COMPANY['legal']}, trading as Galene. Built for the way your brain works.</p></div></footer>
</body></html>"""
    full = os.path.join(OUT, path); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full,"w",encoding="utf-8").write(doc)

def hero(eyebrow, h1, p, ctas=""):
    return f'<div class="hero">{RINGS}<div class="wrap"><div class="eyebrow">{eyebrow}</div><h1>{h1}</h1><p>{p}</p>{ctas}</div></div>'

def product_card(p):
    return f'<div class="card"><div class="ph">Photo to follow</div><h3>{p["name"]}</h3><div class="sub">{p["short"]}</div><p>{p["one"]}</p><a class="more" href="/products/{p["slug"]}/">Details →</a></div>'

def buy_button(p):
    if p["slug"]=="visual-timer": return '<span class="btn btn-ghost" aria-disabled="true">Planned for early 2027 · not yet on sale</span>'
    return '<a class="btn btn-ghost" href="#" aria-disabled="true" title="Available on Amazon.de from January 2027">Buy on Amazon.de · from January 2027</a>'

def build():
    if os.path.isdir(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT); shutil.copytree(os.path.join(ROOT,"assets"), os.path.join(OUT,"assets"))
    open(os.path.join(OUT,"CNAME"),"w").write("galene.ie\n")
    open(os.path.join(OUT,".nojekyll"),"w").write("")
    # home
    cards = "".join(product_card(p) for p in PRODUCTS)
    body = f'<div class="hero hero-home">{RINGS}<div class="wrap">{MARK}<div class="eyebrow">Named for the goddess of calm seas</div><h1 class="hero-title">Galene</h1><p class="hero-sub">Built for the way your brain works — wherever you work.</p><p><a class="btn btn-sea" href="/products/">See the products</a> &nbsp; <a class="btn btn-ghost" href="/company/">About the company</a></p></div></div>'
    body += '<section class="alt"><div class="wrap"><p style="max-width:44rem;font-size:1.1rem">Workplace tools for neurodivergent professionals: noise, glare, restlessness and time, dealt with quietly at the desk. Launching on Amazon.de in January 2027.</p></div></section>'
    body += f'<section><div class="wrap"><h2>The products</h2><p style="max-width:44rem">Five things chosen for one reason each. Nothing medical, nothing that looks out of place on a desk.</p><div class="grid">{cards}</div></div></section>'
    body += '<section class="alt"><div class="wrap"><h2>Why these five</h2><p style="max-width:44rem">Open-plan noise, screen glare, restlessness and time-blindness are four of the most common difficulties neurodivergent adults describe at work. Each product answers one of them with an ordinary object, chosen for its certification and build rather than for claims. We say what a product does and what it is tested to, and no more.</p></div></section>'
    page("index.html","Galene — built for the way your brain works", body, "Workplace tools for neurodivergent professionals. Ear inserts, tinted focus glasses, weighted lap blanket, screen light bar and visual timer. Launching on Amazon.de January 2027.")
    # products index
    body = hero("Products","Five tools, one job each.","Available on Amazon.de from January 2027. Each page lists what the product is, what it is tested to, and the safety information that goes with it.")
    body += f'<section><div class="wrap"><div class="grid">{cards}</div></div></section>'
    page("products/index.html","Products — Galene", body, "Galene products: ear inserts, tinted focus glasses, weighted lap blanket, screen light bar, visual timer.", "Products")
    for p in PRODUCTS:
        facts = "".join(f"<dt>{k}</dt><dd>{html.escape(v)}</dd>" for k,v in p["facts"])
        body = hero(p["short"], p["name"], p["one"], buy_button(p))
        body += f'<section><div class="wrap"><div class="grid" style="grid-template-columns:1fr 1fr;align-items:start"><div><div class="ph" style="aspect-ratio:1">Photo to follow</div></div><div><p>{p["intro"]}</p><h3>Details</h3><dl class="facts">{facts}</dl></div></div>'
        body += f'<div class="note"><strong>Safety information.</strong> {p["safety"]}</div><p class="small">Declaration of conformity and test documentation: <a href="/doc/">galene.ie/doc</a>. Manufacturer and EU responsible person details: <a href="/company/">company information</a>.</p></div></section>'
        page(f"products/{p['slug']}/index.html", f"{p['name']} — Galene", body, p["one"], "Products")
    # doc
    rows = "".join(f"<tr><td><strong>{d['product']}</strong></td><td>{d['reg']}</td><td>{d['std']}</td><td>{d['nb']}</td><td>{d['status']}</td></tr>" for d in DOCS)
    body = hero("galene.ie/doc","Declarations of conformity","This is the address printed on Galene packaging. Each product's EU declaration of conformity, the regulations it is declared against and the standards applied are listed here, with a PDF of the signed declaration once the product is on sale.")
    body += f'<section><div class="wrap"><table><thead><tr><th>Product</th><th>EU legislation</th><th>Standards and certificates</th><th>Notified body</th><th>Declaration</th></tr></thead><tbody>{rows}</tbody></table>'
    body += f'<div class="note"><strong>Manufacturer and EU responsible person.</strong> {COMPANY["legal"]}, trading as Galene, {COMPANY["addr"]}. {COMPANY["email"]} · {COMPANY["phone"]}. For the ear inserts, Colgalene Solutions Ltd is the manufacturer placing the product on the market under its own name. For the other products, the manufacturer is named on the product or its packaging and Colgalene Solutions Ltd is the importer and EU responsible person under Regulation (EU) 2019/1020.</div>'
    body += '<p class="small">To request a copy of a declaration or a test report before it is published here, email the address above with the product name and model.</p></div></section>'
    page("doc/index.html","Declarations of conformity — Galene", body, "EU declarations of conformity for Galene products.", "Declarations")
    # company
    c = COMPANY
    body = hero("Company information","Colgalene Solutions Ltd, trading as Galene","A private company limited by shares, registered in Ireland. Owner and director: Colin Browne.")
    body += f'''<section><div class="wrap"><div class="grid" style="grid-template-columns:1fr 1fr;align-items:start"><div><h3>Registered details</h3><dl class="facts">
<dt>Legal name</dt><dd>{c["legal"]}</dd><dt>Trading as</dt><dd>Galene (registered business name {c["rbn"]})</dd><dt>Company number</dt><dd>CRO {c["cro"]}, Companies Registration Office, Ireland</dd>
<dt>Registered office</dt><dd>{c["addr"]}</dd><dt>VAT number</dt><dd>{c["vat"]}</dd><dt>EORI</dt><dd>{c["eori"]}</dd><dt>Director</dt><dd>{c["director"]}</dd>
<dt>Email</dt><dd><a href="mailto:{c["email"]}">{c["email"]}</a></dd><dt>Telephone</dt><dd>{c["phone"]}</dd></dl></div>
<div><h3>Angaben gemäß § 5 DDG</h3><p lang="de">{c["legal"]} (Handelsname Galene)<br>{c["addr"]}<br>Vertreten durch den Director: {c["director"]}<br>E-Mail: {c["email"]} · Telefon: {c["phone"]}<br>Registergericht: Companies Registration Office (CRO), Irland, Nr. {c["cro"]}<br>USt-IdNr. (Irland): {c["vat"]}<br>Deutsche USt-IdNr.: wird nach Erteilung ergänzt<br>WEEE-Reg.-Nr. (Stiftung EAR): wird nach Erteilung ergänzt<br>Verpackungsregister LUCID: wird nach Erteilung ergänzt</p>
<p lang="de" class="small">Plattform der EU-Kommission zur Online-Streitbeilegung: <a href="https://ec.europa.eu/consumers/odr">ec.europa.eu/consumers/odr</a>. Wir sind nicht verpflichtet und nicht bereit, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p></div></div>
<h3 style="margin-top:40px">Roles under EU product law</h3><p style="max-width:48rem">Colgalene Solutions Ltd is the EU responsible person (Regulation (EU) 2019/1020, Article 4) for every Galene product, and the manufacturer of the Galene ear inserts, which are placed on the market under our own name. Declarations of conformity are at <a href="/doc/">galene.ie/doc</a>.</p></div></section>'''
    page("company/index.html","Company information — Galene", body, "Colgalene Solutions Ltd, trading as Galene: registered details, Impressum, EU responsible person.", "Company")
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
    print("built", sum(len(f) for _,_,f in os.walk(OUT)), "files")

if __name__ == "__main__":
    build()
