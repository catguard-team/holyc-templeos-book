#!/usr/bin/env python3
"""Unix-only maintainer QMP helper for disposable VMs. SPDX-License-Identifier: CC0-1.0"""
import argparse,json,socket,time
SOCKET='/tmp/holyc-book-qmp.sock'
class QMP:
 def __init__(self):
  self.s=socket.socket(socket.AF_UNIX);self.s.connect(SOCKET);self.f=self.s.makefile('rwb',buffering=0);self.f.readline();self.command('qmp_capabilities')
 def command(self,c,a=None):
  self.f.write((json.dumps({'execute':c,**({'arguments':a} if a else {})})+'\n').encode())
  while True:
   r=json.loads(self.f.readline())
   if 'return' in r or 'error' in r:return r
 def hmp(self,s):return self.command('human-monitor-command',{'command-line':s})
 def key(self,k):
  self.hmp('sendkey '+k+' 50');time.sleep(.24)
 def type(self,text):
  special={'\n':'ret',' ':'spc','"':'shift-apostrophe',"'":'apostrophe',':':'shift-semicolon',';':'semicolon','(':'shift-9',')':'shift-0','/':'slash','\\':'backslash','#':'shift-3','_':'shift-minus','-':'minus','.':'dot',',':'comma','=':'equal','+':'shift-equal','*':'shift-8','[':'bracket_left',']':'bracket_right','{':'shift-bracket_left','}':'shift-bracket_right','!':'shift-1','<':'shift-comma','>':'shift-dot','&':'shift-7','|':'shift-backslash','?':'shift-slash','$':'shift-4','%':'shift-5','^':'shift-6'}
  for ch in text:
   self.key(special.get(ch,'shift-'+ch.lower() if ch.isupper() else ch))
 def screen(self,name):return self.command('screendump',{'filename':f'/tmp/{name}.ppm'})

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--socket',default=SOCKET)
 p.add_argument('action',choices=['type','key','screen','quit'])
 p.add_argument('value',nargs='?',default='')
 a=p.parse_args();SOCKET=a.socket;q=QMP()
 if a.action=='type':q.type(a.value)
 elif a.action=='key':q.key(a.value)
 elif a.action=='screen':print(q.command('screendump',{'filename':a.value}))
 else:print(q.command('quit'))
