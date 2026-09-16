"""Generate responsive WebP assets; originals are retained outside dist.
Requires ImageMagick's convert command only when regenerating images.
"""
from pathlib import Path
import subprocess,shutil
ROOT=Path(__file__).parent
ASSETS=ROOT/'dist/assets'
ORIGINALS=ROOT/'source-assets'
NAMES=['chickpea','beans','oats','gnocchi','lentils','edamame-bowl','mushroom-toast','porridge']
def optimize():
    ORIGINALS.mkdir(exist_ok=True)
    for name in NAMES:
        original=ORIGINALS/(name+'.png')
        old=ASSETS/(name+'.png')
        if not original.exists():shutil.copy2(old,original)
        for width in (480,800,1200):
            out=ASSETS/f'{name}-{width}.webp'
            if not out.exists() or out.stat().st_mtime<original.stat().st_mtime:
                subprocess.run(['convert',str(original),'-resize',f'{width}x>','-strip','-quality','78',str(out)],check=True)
        if old.exists():old.unlink()
if __name__=='__main__':optimize()
