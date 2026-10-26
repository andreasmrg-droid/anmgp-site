import os, glob, zipfile, html
from PIL import Image
R = '/home/claude/anmgp-site'
NEWS = "https://zgnp-zngp.maillist-manage.com/ua/Optin?od=11287ecdb18c23&amp;zx=137b72d14&amp;lD=117ec2754353e008e&amp;sD=117ec2754353e0094"
DISCORD = "https://discord.gg/rN68SsDpm"
METRICOOL = '<script>function loadScript(a){var b=document.getElementsByTagName("head")[0],c=document.createElement("script");c.type="text/javascript",c.src="https://tracker.metricool.com/resources/be.js",c.onreadystatechange=a,c.onload=a,b.appendChild(c)}loadScript(function(){beTracker.t({hash:"51fbc312f16afc38004ffeea787fbb4f"})});</script>'
MENU_JS = '<script>document.querySelector(".menu-btn").addEventListener("click",function(){var n=document.querySelector("nav");n.classList.toggle("open");this.setAttribute("aria-expanded",n.classList.contains("open"))});document.querySelectorAll("nav ul a").forEach(function(a){a.addEventListener("click",function(){document.querySelector("nav").classList.remove("open")})});</script>'

def head(title, desc, og_img, url, body_cls=''):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://anmgp.com/{og_img}">
<meta property="og:url" content="https://anmgp.com/{url}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://anmgp.com/{og_img}">
<link rel="canonical" href="https://anmgp.com/{url}">
<link rel="icon" href="/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css?v=5">
</head>
<body class="{body_cls}">
'''

def nav(cur):
    last = ('#press-kit','Press') if cur in ('tl','ae') else ('/#contact','Contact')
    c = lambda k: ' class="cur"' if k==cur else ''
    games = f'''<li class="dd"><a href="/#games"{c('tl') if cur=='tl' else c('ae')} aria-haspopup="true">Games <span class="caret">▾</span></a>
    <ul class="sub"><li><a href="/trench-league/"{c('tl')}>Trench League</a></li><li><a href="/automotive-empire/"{c('ae')}>Automotive Empire</a></li></ul></li>'''
    return f'''<nav><div class="wrap">
  <a class="brand" href="/"><img src="/anmgp-logo.png" alt="ANMGP Studio"></a>
  <button class="menu-btn" aria-label="Menu" aria-expanded="false">Menu ☰</button>
  <ul><li><a href="/"{c('home')}>Home</a></li>{games}<li><a href="#newsletter">Newsletter</a></li><li><a href="{last[0]}">{last[1]}</a></li></ul>
</div></nav>
'''

def newsletter(heading='Stay in the loop'):
    return f'''<section id="newsletter" class="newsletter"><div class="wrap">
  <div class="eyebrow">Newsletter</div>
  <h2>{heading}</h2>
  <p>One email when there's something worth playing: free demos, launches and new games. No spam, unsubscribe anytime.</p>
  <iframe title="ANMGP Studio newsletter sign-up" scrolling="no" src="{NEWS}"></iframe>
</div></section>
'''

def footer():
    return f'''<footer><div class="wrap">© 2026 ANMGP Studio · <a href="/">anmgp.com</a> · <a href="mailto:info@anmgp.com">info@anmgp.com</a> · <a href="{DISCORD}" target="_blank" rel="noopener">Discord</a></div></footer>
{MENU_JS}
{METRICOOL}
</body>
</html>
'''

def size_of(p):
    b = os.path.getsize(p)
    return f'{b/1024/1024:.1f} MB' if b > 1024*1024 else f'{round(b/1024)} KB'

def game_page(g):
    slug, P = g['slug'], f"{R}/{g['slug']}/press"
    steam = f"https://store.steampowered.com/app/{g['appid']}/{g['steam_name']}/?utm_source=anmgp&utm_medium=website&utm_campaign={slug}"
    shots = sorted(glob.glob(f'{P}/{slug}-screenshot-*.jpg'))
    caps = sorted(glob.glob(f'{P}/{slug}-capsule-*.jpg')) + sorted(glob.glob(f'{P}/{slug}-keyart-*.jpg'))
    # zip
    zp = f'{P}/{slug}-presskit.zip'
    fact_txt = f"{g['name']} — press kit\nANMGP Studio · https://anmgp.com/{slug}/\n\n" + '\n'.join(f'{k}: {html.unescape(v)}' for k, v in g['facts_txt']) + \
        f"\n\nSHORT DESCRIPTION\n{g['short']}\n\nLONG DESCRIPTION\n{g['long_txt']}\n\nKEY FEATURES\n" + '\n'.join('- ' + html.unescape(f.replace('<b>','').replace('</b>','')) for f in g['features']) + \
        f"\n\nTrailer: https://www.youtube.com/watch?v={g['yt']}\nSteam: https://store.steampowered.com/app/{g['appid']}/\nPress contact: info@anmgp.com (keys for press and creators on request)\n\nAll images are real in-game screenshots unless marked as key art. You may use these assets for coverage of {g['name']}.\n"
    with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr(f'{slug}-factsheet.txt', fact_txt)
        for f in [f'{P}/{slug}-logo.png', f'{R}/press/anmgp-studio-logo.png'] + caps + shots:
            z.write(f, os.path.basename(f))
    def dl(path, label):
        rel = '/' + os.path.relpath(path, R).replace(os.sep, '/')
        thumb = rel if path.endswith(('.png', '.jpg')) else f'/{slug}/press/{slug}-logo.png'
        return f'<a href="{rel}" download><img src="{thumb}" alt="" loading="lazy"><span>{label}<small>{size_of(path)}</small></span></a>'
    facts = ''.join(f'<tr><th>{k}</th><td>{v}</td></tr>' for k, v in g['facts_html'])
    feats = ''.join(f'<li>{f}</li>' for f in g['features'])
    shot_html = ''.join(f'<a href="/{os.path.relpath(s,R)}" target="_blank" rel="noopener"><img src="/{os.path.relpath(s,R)}" alt="{g["name"]} screenshot" loading="lazy"></a>' for s in shots)
    dls = dl(zp, 'Full press kit (.zip)') + dl(f'{P}/{slug}-logo.png', 'Game logo (PNG, transparent)') + dl(f'{R}/press/anmgp-studio-logo.png', 'ANMGP Studio logo (PNG)') + \
        ''.join(dl(c, ('Capsule ' + c.split('capsule-')[1] if 'capsule-' in c else 'Key art, wide ' + c.split('wide-')[1]).replace('.jpg', '').replace('-', ' ')) for c in caps) + \
        ''.join(dl(s, f'Screenshot {i}') for i, s in enumerate(shots, 1))
    logo_html = f'<img class="glogo" src="/{slug}/press/{slug}-logo.png" alt="{g["name"]}">' if g['hero_logo'] else f'<h1>{g["name"]}</h1>'
    page = head(f"{g['name']} — ANMGP Studio", html.escape(g['short']), f"{slug}/press/{slug}-capsule-main-1232x706.jpg", f'{slug}/', g['cls']) + nav(g['cls']) + f'''
<header class="ghero" style="background-image:url('/{slug}/hero.jpg?v=2')"><div class="wrap">
  {logo_html}
  <div>{''.join(f'<span class="tag">{t}</span>' for t in g['tags'])}</div>
  <p class="lead">{g['tagline']}</p>
  <div class="btns">
    <a class="btn primary" href="{steam}" target="_blank" rel="noopener">Wishlist on Steam</a>
    <a class="btn" href="#trailer">Watch trailer</a>
    <a class="btn" href="#press-kit">Press kit</a>
  </div>
</div></header>

<section id="trailer"><div class="wrap">
  <div class="eyebrow">Gameplay trailer</div>
  <h2>See it in motion</h2>
  <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/{g['yt']}" title="{g['name']} gameplay trailer" loading="lazy" allowfullscreen></iframe></div>
</div></section>

<section id="about" class="alt"><div class="wrap cols">
  <div>
    <div class="eyebrow">The game</div>
    <h2>{g['about_h']}</h2>
    {g['long_html']}
    <iframe class="steamw" src="https://store.steampowered.com/widget/{g['appid']}/" loading="lazy" title="{g['name']} on Steam" style="margin-top:22px"></iframe>
  </div>
  <ul class="feat">{feats}</ul>
</div></section>

<section id="screenshots"><div class="wrap">
  <div class="eyebrow">Screenshots</div>
  <h2>Real gameplay</h2>
  <div class="shots">{shot_html}</div>
</div></section>

{newsletter()}
<section id="press-kit" class="alt"><div class="wrap">
  <div class="eyebrow">For press &amp; creators</div>
  <h2>{g['name']} press kit</h2>
  <div class="cols">
    <div>
      <div class="copy"><h4>Short description</h4>{html.escape(g['short'])}</div>
      <div class="copy"><h4>Long description</h4>{g['long_html']}</div>
      <p class="muted">Need a Steam key for coverage or a stream? Email <a href="mailto:info@anmgp.com?subject={g['name'].replace(' ','%20')}%20key%20request">info@anmgp.com</a> with your channel or outlet.</p>
    </div>
    <div class="box"><h4>Fact sheet</h4><table class="facts">{facts}</table></div>
  </div>
  <h3 style="margin-top:34px">Downloads</h3>
  <div class="dl">{dls}</div>
  <p class="note">Screenshots are real in-game captures. Assets may be used for coverage of {g['name']}. Last updated 22 Oct 2026.</p>
</div></section>
''' + footer()
    open(f'{R}/{slug}/index.html', 'w').write(page)
    return fact_txt

TL = dict(slug='trench-league', name='Trench League', appid=5378190, steam_name='Trench_League', cls='tl', yt='cHix4J8GH2E', hero_logo=True,
  tags=['PC · Steam', 'Free demo coming soon', 'Local &amp; online multiplayer'],
  tagline='A brutal top-down armored sport. Two buttons, one spiked steel ball, and a crowd that wants blood more than goals.',
  short="Punch your way to the spiked steel ball and smash it into the enemy cage. The side with the most breaches wins. Knock rivals out and the Reclaim drags them off. Face opponents from different planets of the Solar System and fight your way to the Solar Final! Test your skills against real opponents!",
  about_h='Blood. Steel. Obedience.',
  long_html='<p>In 2300 the Solar Government does not ban the Trench. It funds the lights and puts the Eye, a Census camera, in every wall. Nine armoured players a side, one spiked steel ball, and a crowd that wants blood more than goals.</p><p class="muted">Win the ball with your fists, knock rivals out cold and watch the Reclaim drag them off the pitch. Run a club across 8 worlds and 64 teams, survive the illegal midweek Cut, and settle it with friends on one screen or online.</p>',
  long_txt="In 2300 the Solar Government does not ban the Trench. It funds the lights and puts the Eye, a Census camera, in every wall. Nine armoured players a side, one spiked steel ball, and a crowd that wants blood more than goals.\nWin the ball with your fists, knock rivals out cold and watch the Reclaim drag them off the pitch. Run a club across 8 worlds and 64 teams, survive the illegal midweek Cut, and settle it with friends on one screen or online.",
  features=['<b>Two buttons do everything.</b> Easy to pick up, hard to survive.',
            '<b>Win the ball with your fists.</b> Knock a rival out cold and the Reclaim drags them off the pitch.',
            '<b>Hit the Eye</b> for points and charge the ball at the Tesla towers.',
            '<b>Four formations</b>, each one beats another and fears another.',
            '<b>64 clubs on 8 worlds</b>, from Earth to Triton: leagues, playoffs and a Solar Final.',
            '<b>The Cut:</b> an illegal midweek knockout. Win, and strike a loser&#8217;s player off their file.',
            '<b>Wounds, ageing and the Exit List</b>, plus Ironman careers.',
            '<b>Fight your friends:</b> 1 vs 1 and co-op on one screen, the Hot Seat Cup, and online play over Steam or PC to PC (1 vs 1, co-op, 2 vs 2, cups up to 32 players, ranked ladder).'],
  facts_html=[('Developer / publisher','ANMGP Studio'),('Platform','PC (Windows) · Steam'),('Release','Coming soon · Free demo coming soon'),('Price','TBA'),
              ('Genre','Top-down action sport with club management'),('Modes','Championship career, The Cut, custom matches vs CPU, local hot seat (1 vs 1, co-op, Hot Seat Cup), online (1 vs 1, co-op, 2 vs 2, cups &amp; tournaments, ranked ladder)'),
              ('Controls','Keyboard or gamepad'),('Steam','<a href="https://store.steampowered.com/app/5378190/Trench_League/" target="_blank" rel="noopener">store.steampowered.com/app/5378190</a>'),
              ('Trailer','<a href="https://www.youtube.com/watch?v=cHix4J8GH2E" target="_blank" rel="noopener">YouTube</a>'),('Press contact','<a href="mailto:info@anmgp.com">info@anmgp.com</a>')],
)
TL['facts_txt'] = [(k, v.split('<a')[0].strip() if '<a' in v and k not in ('Steam', 'Trailer', 'Press contact') else ({'Steam': 'https://store.steampowered.com/app/5378190/', 'Trailer': 'https://www.youtube.com/watch?v=cHix4J8GH2E', 'Press contact': 'info@anmgp.com'}.get(k, v))) for k, v in TL['facts_html']]

AE = dict(slug='automotive-empire', name='Automotive Empire', appid=5190350, steam_name='Automotive_Empire', cls='ae', yt='Cq5T_GW8Kr4', hero_logo=True,
  tags=['PC · Steam', 'Free demo coming soon', 'Single-player'],
  tagline='Start with one kart. Take the whole pyramid. A deep motorsport management sim where 21 championships run at once.',
  short="Start with one kart in a small garage. Expand your team from karting to the pinnacle of motorsport. Compete against 172 teams in 21 championships. Design every part, build and expand your campus. Enter the road car and racing parts markets and face another level of competition.",
  about_h='Start with one kart. Take the whole pyramid.',
  long_html='<p>Automotive Empire runs the whole motorsport pyramid as one living world. Karting, rally, touring cars, stock cars, endurance, open wheel and GP: 21 championships advance together, week by week.</p><p class="muted">You start with one kart team. 172 rival teams recruit, research and spend on the same calendar. Design every part, build it in your own plant, sign the people who make the difference, and sell road cars to pay for the racing.</p>',
  long_txt="Automotive Empire runs the whole motorsport pyramid as one living world. Karting, rally, touring cars, stock cars, endurance, open wheel and GP: 21 championships advance together, week by week.\nYou start with one kart team. 172 rival teams recruit, research and spend on the same calendar. Design every part, build it in your own plant, sign the people who make the difference, and sell road cars to pay for the racing.",
  features=['<b>Seven disciplines, all at once:</b> karting, rally, touring cars, stock cars, endurance prototypes, open wheel and GP.',
            '<b>172 rival teams</b> on the same calendar, recruiting and researching while you do.',
            '<b>Five R&amp;D pillars:</b> Design, Upgrade, Reverse Engineering, Special Projects, Commercial Cars. You will never fund all five.',
            '<b>Build parts in your own CNC plant</b> and homologate them. Every upgrade trades performance against reliability.',
            '<b>Drivers and staff</b> with contracts, loyalty and ambition: designers, team principals, strategists, pit crews and a CFO.',
            '<b>Lap-by-lap race days</b> with weather, tyres, safety cars and real-time pit calls.',
            '<b>The road car pays for the race car:</b> a live car market, a parts market and a campus of up to 20 buildings.',
            '<b>Mod-friendly</b> by design.'],
  facts_html=[('Developer / publisher','ANMGP Studio'),('Platform','PC (Windows) · Steam'),('Release','Coming soon · Free demo coming soon'),('Price','TBA'),
              ('Genre','Motorsport management simulation'),('Players','Single-player'),
              ('Steam','<a href="https://store.steampowered.com/app/5190350/Automotive_Empire/" target="_blank" rel="noopener">store.steampowered.com/app/5190350</a>'),
              ('Trailer','<a href="https://www.youtube.com/watch?v=Cq5T_GW8Kr4" target="_blank" rel="noopener">YouTube</a>'),('Press contact','<a href="mailto:info@anmgp.com">info@anmgp.com</a>')],
)
AE['facts_txt'] = [(k, {'Steam': 'https://store.steampowered.com/app/5190350/', 'Trailer': 'https://www.youtube.com/watch?v=Cq5T_GW8Kr4', 'Press contact': 'info@anmgp.com'}.get(k, v)) for k, v in AE['facts_html']]

for g in (TL, AE):
    game_page(g)
print('pages ok')
