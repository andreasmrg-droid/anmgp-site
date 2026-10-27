# 2026-10-27: AE management-themed main/header capsules
from PIL import Image
R='/home/claude/anmgp-site'; F='/mnt/user-data/uploads/Marketing Department/Capsules AE Management 2026-10-27'
P=R+'/automotive-empire/press'
for n,o in [('AE_main_capsule_1232x706','capsule-main-1232x706'),('AE_header_capsule_920x430','capsule-header-920x430')]:
    Image.open(f'{F}/{n}.jpg').convert('RGB').save(f'{P}/automotive-empire-{o}.jpg',quality=90,optimize=True,progressive=True)
Image.open(f'{F}/AE_main_capsule_1232x706.jpg').convert('RGB').save(R+'/automotive-empire-art.jpg',quality=88,optimize=True,progressive=True)
print('ok')
