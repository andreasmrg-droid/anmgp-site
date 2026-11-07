# 2026-11-07: TL inked capsules v3 (main + header) for press kit and site card
from PIL import Image
R='/home/claude/anmgp-site'; V=f'{R}/media/steam/v3'
def jpg(src,dst,q=90): Image.open(src).convert('RGB').save(dst,quality=q,optimize=True,progressive=True)
jpg(f'{V}/TL_main_capsule_1232x706.jpg',f'{R}/trench-league/press/trench-league-capsule-main-1232x706.jpg')
jpg(f'{V}/TL_header_capsule_920x430.jpg',f'{R}/trench-league/press/trench-league-capsule-header-920x430.jpg')
jpg(f'{V}/TL_main_capsule_1232x706.jpg',f'{R}/trench-league-art.jpg',88)
print('ok')
