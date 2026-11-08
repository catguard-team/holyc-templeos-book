"""Read-only maintainer check of the 24 shipped examples in a FAT32 guest disk.
SPDX-License-Identifier: CC0-1.0
"""
from pathlib import Path
import struct,hashlib,json,argparse
root_path=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('image',type=Path);args=ap.parse_args()
image=args.image
f=image.open('rb')
def read(pos,n):f.seek(pos);return f.read(n)
m=read(0,512);start=struct.unpack_from('<I',m,454)[0];b=read(start*512,512)
spc=b[13];reserved=struct.unpack_from('<H',b,14)[0];fats=b[16];fatsz=struct.unpack_from('<I',b,36)[0];root=struct.unpack_from('<I',b,44)[0]
fat=read((start+reserved)*512,fatsz*512);base=start+reserved+fats*fatsz
def chain(c):
 seen=set();data=bytearray()
 while c<0x0ffffff8:
  if c in seen or c<2:raise ValueError('bad chain')
  seen.add(c);data+=read((base+(c-2)*spc)*512,spc*512);c=struct.unpack_from('<I',fat,c*4)[0]&0x0fffffff
 return bytes(data)
def directory(c):
 out={};data=chain(c)
 for i in range(0,len(data),32):
  e=data[i:i+32]
  if e[0]==0:break
  if e[0]==0xe5 or e[11]==0x0f or e[11]&8:continue
  stem=e[:8].decode('ascii').rstrip();ext=e[8:11].decode('ascii').rstrip();name=stem+('.'+ext if ext else '')
  cl=(struct.unpack_from('<H',e,20)[0]<<16)+struct.unpack_from('<H',e,26)[0];size=struct.unpack_from('<I',e,28)[0]
  out[name]=(cl,size,bool(e[11]&16))
 return out
def get(path):
 c=root
 for part in path.strip('/').upper().split('/'):
  c,size,isdir=directory(c)[part]
 return directory(c) if isdir else chain(c)[:size]

for p in (root_path/'examples').glob('*.HC'):
 assert get('/Home/Book/'+p.name)==p.read_bytes(),p.name
for p in (root_path/'tests/guest').glob('*.HC'):
 assert get('/Home/Book/QA/'+p.name)==p.read_bytes(),p.name
assert get('/Home/Once.HC')==(root_path/'tools/guest/START.HC').read_bytes()
print('24 examples, 2 QA scripts, startup: byte exact')
