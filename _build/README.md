# Site build scripts (not published — Jekyll ignores folders starting with _)
- assets.py: copies/resizes logos, capsules, screenshots from Andreas's staged files into <game>/press/ and hero images.
- build.py: generates trench-league/index.html and automotive-empire/index.html (game data dicts at the bottom) and the press kit zips.
- home.py: generates index.html (homepage) using build.py's shared header/nav/footer.
- welcome.html: newsletter welcome email (also saved as a Zoho Campaigns template).
Run: python3 assets.py && python3 build.py && python3 home.py  (paths assume the repo at /home/claude/anmgp-site and staged uploads under /mnt/user-data/uploads).
Rule: update the press kits whenever capsules, logos, screenshots, descriptions, features or facts change.
