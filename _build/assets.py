import os, shutil, zipfile
from PIL import Image
R='/home/claude/anmgp-site'; U='/mnt/user-data/uploads'
MD=U+'/Marketing Department'
def jpg(src,dst,size=None,q=88):
    im=Image.open(src).convert('RGB')
    if size: im=im.resize(size,Image.LANCZOS)
    os.makedirs(os.path.dirname(dst),exist_ok=True); im.save(dst,quality=q,optimize=True,progressive=True)
def png(src,dst,maxw=None):
    im=Image.open(src).convert('RGBA'); im=im.crop(im.getbbox())
    if maxw and im.width>maxw: im=im.resize((maxw,round(im.height*maxw/im.width)),Image.LANCZOS)
    os.makedirs(os.path.dirname(dst),exist_ok=True); im.save(dst,optimize=True)

# studio
png(U+'/Logistics Files/Logo_Alpha.png', R+'/press/anmgp-studio-logo.png', 1400)

# ---- Trench League
T=R+'/trench-league'; TP=T+'/press'
K=MD+'/Trench League/Steam Capsules 2026-10-22 KeyArt'
png(U+'/Godot/Trench League/Logistic Files/trench_league_logo_transparent.png', TP+'/trench-league-logo.png')
for n,o in [('TL_main_capsule_1232x706','capsule-main-1232x706'),('TL_header_capsule_920x430','capsule-header-920x430'),('TL_vertical_capsule_748x896','capsule-vertical-748x896'),('TL_library_capsule_600x900','capsule-library-600x900')]:
    jpg(f'{K}/{n}.png', f'{TP}/trench-league-{o}.jpg', q=90)
jpg(f'{K}/TL_library_hero_3840x1240.png', T+'/hero.jpg', (1920,620), 85)
jpg(f'{K}/TL_main_capsule_1232x706.png', R+'/trench-league-art.jpg', q=88)
S=MD+'/Trench League/Screenshots'
shots=[('trench_2026-10-13_18-35-35_872','match-mars'),('trench_2026-10-13_18-39-57_396','match-ice'),('trench_2026-10-13_18-34-44_547','breach'),('trench_2026-10-13_18-37-42_550','reclaim'),('trench_2026-10-13_18-39-02_229','lineups'),('trench_2026-10-13_18-43-06_759','championship-hub'),('trench_2026-10-13_18-44-50_935','season-champions'),('trench_2026-10-10_13-24-09_986','custom-game')]
for i,(f,n) in enumerate(shots,1):
    jpg(f'{S}/{f}.png', f'{TP}/trench-league-screenshot-{i:02d}-{n}.jpg', q=88)

# ---- Automotive Empire
A=R+'/automotive-empire'; AP=A+'/press'
C=MD+'/Automotive Empire/Visual Assets/Steam Capsules 2026-10-16 v2'
png(U+'/Logistics Files/Title (fixed gold).png', AP+'/automotive-empire-logo.png', 2400)
for n,o in [('AE_main_capsule_1232x706','capsule-main-1232x706'),('AE_header_capsule_920x430','capsule-header-920x430'),('AE_vertical_capsule_748x896','capsule-vertical-748x896'),('AE_library_capsule_600x900','capsule-library-600x900')]:
    jpg(f'{C}/{n}.png', f'{AP}/automotive-empire-{o}.jpg', q=90)
jpg(R+'/automotive-empire-art.jpg', A+'/hero.jpg', q=85)
for i,(f,n) in enumerate([('ae_1_entry','choose-entry-point'),('ae_2_gp','gp-championship'),('ae_3_rally','rally'),('ae_4_sc','stock-cars'),('ae_5_epc','endurance'),('ae_6_owc','open-wheel'),('ae_7_tc','touring-cars')],1):
    shutil.copy(f'{R}/media/{f}.jpg', f'{AP}/automotive-empire-screenshot-{i:02d}-{n}.jpg')
print('ok')
