import json, re, shutil
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
data_dir=ROOT/'data'; topics_dir=ROOT/'topics'; archive_dir=ROOT/'archive'; topics_dir.mkdir(exist_ok=True); archive_dir.mkdir(exist_ok=True)
files=sorted(data_dir.glob('growth-update-*.json'))
if not files: raise SystemExit('No growth dataset found')
latest=files[-1]; data=json.loads(latest.read_text(encoding='utf-8'))
# Preserve every previous update as an immutable archive snapshot.
archive_target=archive_dir/latest.name
if not archive_target.exists(): shutil.copy2(latest, archive_target)

def slug(t):
    s=t.get('slug') or f"topic-{t.get('rank',1)}"
    return re.sub(r'-+','-',re.sub(r'[^a-z0-9-]','-',s.lower())).strip('-')

def esc(v):
    return str(v or '').replace('&','&amp;').replace('<','&lt;').replace('>','&gt;').replace('"','&quot;')

def script(t, short=False):
    title=t.get('recommended_title') or t.get('topic','')
    if short:
        return f"HOOK: {title}\n\n“यो कुरा तपाईंले थाहा पाउनैपर्छ। {title} — अब practical result हेरौं। {t.get('why_make','')} अन्त्यमा आफ्नो अनुभव comment गर्नुहोस्।”"
    return f"HOOK\n“{title} बारे धेरै कुरा सुनिन्छ, तर आज हामी theory होइन practical result हेर्छौं।”\n\nINTRO\n“नमस्कार, म Laxman Nepal। आजको भिडियोमा {t.get('topic','यो topic')} लाई सरल Nepali मा बुझ्नेछौं, practical demo गर्नेछौं र कसका लागि उपयोगी छ भन्ने स्पष्ट गर्नेछौं।”\n\nMAIN\nProblem → tool/solution → live demo → result → limitation → best use case. प्रत्येक मुख्य बुँदामा screen recording, before/after र वास्तविक result देखाउनुहोस्।\n\nOUTRO\n“तपाईंलाई यो जानकारी useful लाग्यो भने comment मा आफ्नो opinion लेख्नुहोस्। यस्तै practical tech videos का लागि @laxmannepalofficial subscribe गर्नुहोस्।”"

for t in data.get('topics',[]):
    target=t.get('target','Nepal')
    # All scripts are intentionally Nepali, even for US/global research tracks.
    long=t.get('long_video_script') or script(t)
    shorts=t.get('shorts') or [{'title':f"{t.get('topic','Tech')} — Quick Tip",'script':script(t,True)},{'title':f"यो AI/Tech trick थाहा छ?",'script':script(t,True)}]
    seo=t.get('seo_score',t.get('score',0))
    thumb=t.get('thumbnail',{})
    html=f'''<!doctype html><html lang="ne"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(t.get('description',''))}"><title>{esc(t.get('recommended_title',t.get('topic','')))} · Laxman Nepal Official</title><link rel="stylesheet" href="../style.css"></head><body><header class="topbar glass"><div class="brand"><div class="brand-mark">LN</div><div><strong>Laxman Nepal Official</strong><span>YouTube Growth Intelligence</span></div></div><a class="channel-btn" href="../index.html">← Growth</a></header><main><section class="hero glass"><span class="eyebrow">{esc(target)} · {esc(t.get('category','TECH'))}</span><h1>{esc(t.get('topic',''))}</h1><p>Research snapshot: {esc(data.get('updated_at',''))}</p><div class="hero-stats"><div class="stat"><b>{seo}/100</b><span>SEO SCORE</span></div><div class="stat"><b>{esc(t.get('demand','—'))}</b><span>DEMAND</span></div><div class="stat"><b>{esc(t.get('channel_fit','—'))}</b><span>CHANNEL FIT</span></div></div></section><section class="section-head"><div><span class="eyebrow">PUBLISHING PACKAGE</span><h2>SEO + Packaging</h2></div></section><section class="workflow-grid"><article class="glass workflow"><b>RECOMMENDED TITLE</b><h3>{esc(t.get('recommended_title',''))}</h3><p>{esc(t.get('why_make',''))}</p></article><article class="glass workflow"><b>DESCRIPTION</b><p>{esc(t.get('description',''))}</p></article><article class="glass workflow"><b>TAGS</b><p>{esc(', '.join(t.get('tags',[])))}</p></article><article class="glass workflow"><b>THUMBNAIL</b><h3>{esc(thumb.get('text',''))}</h3><p>{esc(thumb.get('concept',''))}</p><pre>{esc(thumb.get('prompt',''))}</pre></article></section><section class="section-head"><div><span class="eyebrow">LONG VIDEO · NEPALI SCRIPT</span><h2>Complete long-form plan</h2></div></section><article class="glass workflow"><pre>{esc(long)}</pre><p><b>Editing:</b> result first, visual change every 2–5 seconds, screen recordings, zooms, captions, before/after comparisons and retention pattern interrupts.</p></article><section class="section-head"><div><span class="eyebrow">SHORTS · NEPALI SCRIPT</span><h2>Short-form packages</h2></div></section>{''.join(f'<article class="glass workflow"><b>{esc(s.get("title","Short"))}</b><pre>{esc(s.get("script",s.get("description","")))}</pre><p>9:16 · result in first 1–2 seconds · captions · fast cuts · no long intro.</p></article>' for s in shorts)}<section class="section-head"><div><span class="eyebrow">VIDEO EDITING</span><h2>Production blueprint</h2></div></section><article class="glass workflow"><p>Open with the result. Remove dead air. Use screen recordings and cursor highlights. Add Nepali captions. Change visual framing every 2–5 seconds. Use before/after comparisons. Place the strongest proof before the midpoint. For Shorts, use 9:16, immediate hook and a curiosity-based ending.</p></article></main><footer>Snapshot: {esc(data.get('updated_at',''))} · <a href="https://www.youtube.com/@laxmannepalofficial">@laxmannepalofficial</a></footer></body></html>'''
    (topics_dir/f'{slug(t)}.html').write_text(html,encoding='utf-8')
# Archive index is generated from all snapshots; nothing is deleted.
rows=[]
for f in sorted(archive_dir.glob('growth-update-*.json'), reverse=True):
    try: d=json.loads(f.read_text(encoding='utf-8')); rows.append((d.get('updated_at',f.stem),f.name,len(d.get('topics',[]))))
    except Exception: pass
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Achieve & Archive · Laxman Nepal Official</title><link rel="stylesheet" href="../style.css"></head><body><header class="topbar glass"><div class="brand"><div class="brand-mark">LN</div><div><strong>Laxman Nepal Official</strong><span>Growth Archive</span></div></div><a class="channel-btn" href="../index.html">← Growth</a></header><main><section class="hero glass"><span class="eyebrow">ACHIEVE · PERMANENT HISTORY</span><h1>Every update stays.</h1><p>No idea, script or research snapshot is deleted when a new update arrives.</p></section><section class="section-head"><div><span class="eyebrow">ARCHIVE</span><h2>Research snapshots</h2></div></section><section class="topic-grid">{''.join(f'<article class="glass topic"><span class="rank">ARCHIVE</span><h3>{esc(x[0])}</h3><p>{x[2]} opportunities preserved.</p><a class="open" href="{x[1]}">Open snapshot →</a></article>' for x in rows)}</section></main><footer>© Laxman Nepal Official · Permanent Growth Archive</footer></body></html>'
(archive_dir/'index.html').write_text(html,encoding='utf-8')
