import json, re, shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data'; TOPICS=ROOT/'topics'; ARCHIVE=ROOT/'archive'
TOPICS.mkdir(exist_ok=True); ARCHIVE.mkdir(exist_ok=True)
files=sorted(DATA.glob('growth-update-*.json'))
if not files:
    fallback=DATA/'growth-data.json'
    if not fallback.exists(): raise SystemExit('No growth dataset found')
    files=[fallback]
latest=files[-1]; data=json.loads(latest.read_text(encoding='utf-8'))

def esc(v=''):
    return str(v or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def slug(t):
    raw=t.get('slug') or t.get('topic') or f"topic-{t.get('rank',1)}"
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9-]','-',raw.lower())).strip('-') or f"topic-{t.get('rank',1)}"

def nav(prefix='', archive_page=False):
    archive_href='index.html' if archive_page else f'{prefix}archive/index.html'
    return f'''<header class="topbar glass"><div class="brand"><div class="brand-mark">LN</div><div><strong>Laxman Nepal Official</strong><span>YouTube Growth Intelligence</span></div></div><button class="menu-toggle" id="menuToggle" aria-expanded="false" aria-controls="mainNav">☰ <span>Menu</span></button><nav class="nav" id="mainNav" aria-label="Main navigation"><a class="nav-link" href="{prefix}index.html">🏠 Dashboard</a><div class="nav-group"><button class="nav-group-btn" type="button">💡 Ideas for <span>⌄</span></button><div class="nav-dropdown"><a href="{prefix}audience-nepali.html">🇳🇵 Nepali Audience · Nepal</a><a href="{prefix}audience-us.html">🇺🇸 US Audience · United States</a><a href="{prefix}global.html">🌍 Global Audience · US/Global</a></div></div><a class="nav-link" href="{prefix}analytics.html">📊 @laxmannepalofficial Analytics</a><a class="nav-link" href="{archive_href}">🏆 Achieve &amp; Archive</a></nav><a class="channel-btn" href="https://www.youtube.com/@laxmannepalofficial" target="_blank" rel="noopener">@laxmannepalofficial ↗</a></header><script>const mt=document.getElementById('menuToggle'),navEl=document.getElementById('mainNav');mt?.addEventListener('click',()=>{const o=navEl.classList.toggle('open');mt.setAttribute('aria-expanded',o)});document.querySelector('.nav-group-btn')?.addEventListener('click',e=>e.currentTarget.parentElement.classList.toggle('open'));</script>'''

def fallback_long(t):
    return f'''HOOK\n“{t.get('recommended_title') or t.get('topic','')} बारे धेरैले सुन्नुभएको होला। तर आज hype होइन, practical result हेर्नेछौं।”\n\nINTRO\n“नमस्कार, म Laxman Nepal। आजको भिडियोमा {t.get('topic','यो topic')} लाई सरल नेपालीमा बुझ्नेछौं, practical demo गर्नेछौं, फाइदा र limitation दुवै हेर्नेछौं।”\n\nSTRUCTURE\nसमस्या → समाधान/टुल → live demo → वास्तविक result → limitation → कसका लागि उपयोगी → alternative → final recommendation.\n\nOUTRO\n“तपाईंलाई यो भिडियो useful लाग्यो भने आफ्नो अनुभव comment गर्नुहोस्। यस्तै practical tech videos का लागि @laxmannepalofficial subscribe गर्नुहोस्।”'''

def fallback_short(t):
    return f'''HOOK: {t.get('recommended_title') or t.get('topic','Tech')}\n\n“यो कुरा तपाईंले थाहा पाउनैपर्छ। {t.get('topic','यो tool')} लाई practical रूपमा test गर्दा यस्तो result आयो। तपाईंले प्रयोग गर्नुभएको छ भने comment गर्नुहोस्। Full explanation का लागि long video हेर्नुहोस्।”'''

# Preserve every dated dataset; never delete an old snapshot.
for f in files:
    target=ARCHIVE/f.name
    if not target.exists(): shutil.copy2(f,target)

for t in data.get('topics',[]):
    long=t.get('long_video_script') or fallback_long(t)
    shorts=t.get('shorts') or [{'title':f"{t.get('topic','Tech')} — Quick Tip",'script':fallback_short(t)},{'title':'यो Tech trick थाहा छ?','script':fallback_short(t)}]
    thumb=t.get('thumbnail') or {}; seo=t.get('seo_score',t.get('score',0))
    html=f'''<!doctype html><html lang="ne"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(t.get('description',''))}"><title>{esc(t.get('recommended_title',t.get('topic','')))} · Laxman Nepal Official</title><link rel="stylesheet" href="../style.css"></head><body>{nav('../')}<main><section class="hero glass"><span class="eyebrow">{esc(t.get('target','Nepal'))} · {esc(t.get('category','TECH'))}</span><h1>{esc(t.get('topic',''))}</h1><p>Research snapshot: {esc(data.get('updated_at',''))}</p><div class="hero-stats"><div class="stat"><b>{seo}/100</b><span>SEO SCORE</span></div><div class="stat"><b>{esc(t.get('demand','—'))}</b><span>DEMAND</span></div><div class="stat"><b>{esc(t.get('competition','—'))}</b><span>COMPETITION</span></div><div class="stat"><b>{esc(t.get('channel_fit','—'))}</b><span>CHANNEL FIT</span></div></div></section><section class="section-head"><div><span class="eyebrow">PUBLISHING PACKAGE</span><h2>Professional SEO package</h2></div></section><section class="workflow-grid"><article class="glass workflow"><b>RECOMMENDED TITLE</b><h3>{esc(t.get('recommended_title',''))}</h3><p>{esc(t.get('why_make',''))}</p></article><article class="glass workflow"><b>ALTERNATIVE TITLES</b><p>{esc(' · '.join(t.get('titles',[])))}</p></article><article class="glass workflow"><b>DESCRIPTION</b><p>{esc(t.get('description',''))}</p><b>TAGS</b><p>{esc(', '.join(t.get('tags',[])))}</p></article><article class="glass workflow"><b>THUMBNAIL</b><h3>{esc(thumb.get('text',''))}</h3><p>{esc(thumb.get('concept',''))}</p><pre>{esc(thumb.get('prompt',''))}</pre></article></section><section class="section-head"><div><span class="eyebrow">LONG VIDEO · NEPALI SCRIPT</span><h2>Complete long-form package</h2></div></section><article class="glass workflow"><pre>{esc(long)}</pre><p><b>Editing:</b> result first; visual change every 2–5 seconds; screen recordings; cursor highlights; Nepali captions; before/after proof; pattern interrupts; strongest evidence before the midpoint.</p></article><section class="section-head"><div><span class="eyebrow">SHORTS · NEPALI SCRIPT</span><h2>Separate Shorts packages</h2></div></section>{''.join(f'<article class="glass workflow"><b>{esc(s.get("title","Short"))}</b><pre>{esc(s.get("script",s.get("description","")))}</pre><p>9:16 · hook in 1–2 seconds · captions · fast cuts · no long intro.</p></article>' for s in shorts)}<section class="section-head"><div><span class="eyebrow">VIDEO EDITING</span><h2>Production blueprint</h2></div></section><article class="glass workflow"><p>Start with the final result. Cut dead air. Use screen recordings and zooms. Highlight exact UI actions. Use B-roll only when it adds information. Add a visual reset every 2–5 seconds. For Shorts: 9:16, immediate result, large captions and a curiosity-driven ending.</p></article></main><footer>Snapshot: {esc(data.get('updated_at',''))} · <a href="https://www.youtube.com/@laxmannepalofficial">@laxmannepalofficial</a></footer></body></html>'''
    (TOPICS/f'{slug(t)}.html').write_text(html,encoding='utf-8')

rows=[]
for f in sorted(ARCHIVE.glob('growth-update-*.json'),reverse=True):
    try:
        d=json.loads(f.read_text(encoding='utf-8')); rows.append((d.get('updated_at',f.stem),f.name,len(d.get('topics',[]))))
    except Exception: pass
cards=''.join(f'<article class="glass topic"><span class="rank">ARCHIVE</span><h3>{esc(date)}</h3><p>{count} opportunities preserved.</p><a class="open" style="display:block;text-align:center;text-decoration:none" href="{name}">Open snapshot →</a></article>' for date,name,count in rows)
(ARCHIVE/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Achieve &amp; Archive · Laxman Nepal Official</title><link rel="stylesheet" href="../style.css"></head><body>{nav('../', True)}<main><section class="hero glass"><span class="eyebrow">ACHIEVE · PERMANENT HISTORY</span><h1>Every update stays.</h1><p>No research idea, script or publishing package is intentionally deleted when a new update arrives.</p></section><section class="section-head"><div><span class="eyebrow">DATED SNAPSHOTS</span><h2>Research archive</h2></div></section><section class="topic-grid">{cards}</section></main><footer>© Laxman Nepal Official · Permanent Growth Archive</footer></body></html>''',encoding='utf-8')
