import importlib.util
spec = importlib.util.spec_from_file_location('b', ''+__import__('os').path.dirname(__file__)+'/build.py')
b = importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
R = b.R
utm = lambda a, n: f"https://store.steampowered.com/app/{a}/{n}/?utm_source=anmgp&utm_medium=website&utm_campaign=site"
page = b.head("ANMGP Studio — Independent Game Studio",
  "ANMGP Studio is an independent game studio. Different worlds, one obsession: games you can't put down. Trench League · Automotive Empire.",
  "og-image.jpg", "") + b.nav('home') + f'''
<header class="hero"><div class="wrap">
  <img src="/anmgp-logo.png" alt="ANMGP Studio logo">
  <p><strong style="color:var(--text)">Different worlds. One obsession: games you can't put down.</strong><br>Every ANMGP game has its own world and its own feel — what they share is depth, personality and the pull of just one more try.</p>
</div></header>

<section id="games"><div class="wrap">
  <div class="eyebrow">Our games</div>
  <h2>Games</h2>

  <article class="game tl">
    <a class="art" href="/trench-league/" aria-label="Trench League" style="background-image:url('/trench-league-art.jpg?v=2')"></a>
    <div class="info">
      <div><span class="tag">PC · Steam</span><span class="tag">Free demo coming soon</span></div>
      <h3>Trench League</h3>
      <p>A brutal top-down armored sport. Win the spiked steel ball with your fists, knock rivals out cold and fight your way across the solar system.</p>
      <ul>
        <li>Two-button controls: easy to pick up, hard to survive</li>
        <li>8 worlds, 64 clubs, leagues, playoffs and a Solar Final</li>
        <li>The Cut: an illegal midweek knockout</li>
        <li>Local hot seat and online play: 1 vs 1, co-op, 2 vs 2, cups</li>
      </ul>
      <div class="btns">
        <a class="btn primary" href="{utm(5378190,'Trench_League')}" target="_blank" rel="noopener">Wishlist on Steam</a>
        <a class="btn" href="/trench-league/">Game page &amp; press kit</a>
      </div>
    </div>
  </article>

  <article class="game ae">
    <a class="art" href="/automotive-empire/" aria-label="Automotive Empire" style="background-image:url('/automotive-empire-art.jpg')"></a>
    <div class="info">
      <div><span class="tag">PC · Steam</span><span class="tag">Free demo coming soon</span></div>
      <h3>Automotive Empire</h3>
      <p>A deep motorsport management sim. Start with one kart and climb the whole pyramid while 21 championships run at once.</p>
      <ul>
        <li>21 championships across 7 disciplines</li>
        <li>172 rival teams on the same calendar</li>
        <li>Five R&amp;D pillars — and never enough budget</li>
        <li>From karting to GP, rally, stock cars and endurance</li>
      </ul>
      <div class="btns">
        <a class="btn primary" href="{utm(5190350,'Automotive_Empire')}" target="_blank" rel="noopener">Wishlist on Steam</a>
        <a class="btn" href="/automotive-empire/">Game page &amp; press kit</a>
      </div>
    </div>
  </article>
</div></section>

<section id="trailers" class="alt"><div class="wrap">
  <div class="eyebrow">Watch</div>
  <h2>Trailers</h2>
  <div class="trailers">
    <div>
      <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/cHix4J8GH2E" title="Trench League gameplay trailer" loading="lazy" allowfullscreen></iframe></div>
      <h4>Trench League — Gameplay Trailer</h4>
    </div>
    <div>
      <div class="video"><iframe src="https://www.youtube-nocookie.com/embed/Cq5T_GW8Kr4" title="Automotive Empire gameplay trailer" loading="lazy" allowfullscreen></iframe></div>
      <h4>Automotive Empire — Gameplay Trailer</h4>
    </div>
  </div>
</div></section>

<section id="about"><div class="wrap about">
  <div>
    <div class="eyebrow">The studio</div>
    <h2>About ANMGP Studio</h2>
    <p>ANMGP Studio is an independent game studio making the games we'd lose sleep over ourselves.</p>
    <p>From a brutal armored sport played across the solar system to a motorsport empire you build from a single kart, every game is a different world — and every one is crafted to keep you coming back.</p><p>More worlds are on the way.</p>
    <p><a href="https://store.steampowered.com/developer/anmgpstudio" target="_blank" rel="noopener">Follow ANMGP Studio on Steam →</a></p>
  </div>
  <div><img src="/press/anmgp-studio-logo-dark.jpg" alt="ANMGP Studio logo" style="width:100%;border-radius:12px;border:1px solid var(--line)" loading="lazy"></div>
</div></section>

{b.newsletter('Stay in the loop')}
<section id="contact" class="alt"><div class="wrap">
  <div class="eyebrow">Get in touch</div>
  <h2>Press, creators &amp; contact</h2>
  <div class="grid3">
    <div class="box">
      <h4>Email &amp; press</h4>
      <p><a href="mailto:info@anmgp.com">info@anmgp.com</a></p>
      <p>Press, streamer keys and business enquiries.</p>
      <ul style="margin-top:10px">
        <li><a href="/trench-league/#press-kit">Trench League press kit</a></li>
        <li><a href="/automotive-empire/#press-kit">Automotive Empire press kit</a></li>
      </ul>
    </div>
    <div class="box">
      <h4>Follow</h4>
      <ul>
        <li><a href="https://www.youtube.com/@ANMGPStudio" target="_blank" rel="noopener">YouTube</a></li>
        <li><a href="https://x.com/ANMGP_Studio" target="_blank" rel="noopener">X</a></li>
        <li><a href="https://www.instagram.com/anmgp_studio" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="https://bsky.app/profile/anmgpstudio.bsky.social" target="_blank" rel="noopener">Bluesky</a></li>
        <li><a href="https://www.tiktok.com/@anmgpstudio" target="_blank" rel="noopener">TikTok</a></li>
      </ul>
    </div>
    <div class="box">
      <h4>Community</h4>
      <ul>
        <li><a href="{b.DISCORD}" target="_blank" rel="noopener">ANMGP Studio Discord</a></li>
        <li><a href="https://store.steampowered.com/developer/anmgpstudio" target="_blank" rel="noopener">Steam developer page</a></li>
      </ul>
    </div>
  </div>
</div></section>
''' + b.footer()
page = page.replace('<li><a href="#newsletter">Newsletter</a></li><li><a href="/#contact">Contact</a></li>', '<li><a href="#newsletter">Newsletter</a></li><li><a href="#contact">Contact</a></li>')
open(f'{R}/index.html', 'w').write(page)
print('home ok')
