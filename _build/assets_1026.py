# 2026-10-26: new capsule art (Grok key art, final set uploaded to Steam)
import os
from PIL import Image
R='/home/claude/anmgp-site'; F='/mnt/user-data/uploads/Marketing Department/Capsules Final 2026-10-26'
def jpg(src,dst,size=None,q=88):
    im=Image.open(src).convert('RGB')
    if size: im=im.resize(size,Image.LANCZOS)
    im.save(dst,quality=q,optimize=True,progressive=True)
for G,slug in (('TL','trench-league'),('AE','automotive-empire')):
    P=f'{R}/{slug}/press'
    for n,o in [('main_capsule_1232x706','main-1232x706'),('header_capsule_920x430','header-920x430'),('vertical_capsule_748x896','vertical-748x896'),('library_capsule_600x900','library-600x900')]:
        jpg(f'{F}/{G}_{n}.jpg', f'{P}/{slug}-capsule-{o}.jpg', q=90)
    jpg(f'{F}/{G}_library_hero_3840x1240.jpg', f'{P}/{slug}-keyart-wide-3840x1240.jpg', q=88)
    jpg(f'{F}/{G}_library_hero_3840x1240.jpg', f'{R}/{slug}/hero.jpg', (1920,620), 85)
    jpg(f'{F}/{G}_main_capsule_1232x706.jpg', f'{R}/{slug}-art.jpg', q=88)
# AE: navy logo replaces gold
im=Image.open(f'{F}/AE_library_logo.png').convert('RGBA'); im.crop(im.getbbox()).save(f'{R}/automotive-empire/press/automotive-empire-logo.png',optimize=True)
print('ok')
