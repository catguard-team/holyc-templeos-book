#!/usr/bin/env python3
"""Maintainer integration exercise. Run only in an initialized disposable VM.

The caller boots Drive C and waits for the book prompt first. Unix QMP only.
SPDX-License-Identifier: CC0-1.0
"""
import argparse
import json
from pathlib import Path
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import qa_vm

ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--socket', required=True)
ap.add_argument('--log', type=Path, required=True)
ap.add_argument('--screens', type=Path, required=True)
ap.add_argument('--restart-check', action='store_true')
a = ap.parse_args()
qa_vm.SOCKET = a.socket
q = qa_vm.QMP()
a.screens.mkdir(parents=True, exist_ok=True)


def command(s):
    q.type(s + '\n')
    time.sleep(2)


def screen(name):
    result = q.command('screendump', {'filename': str((a.screens / (name + '.ppm')).resolve())})
    if 'error' in result:
        raise RuntimeError(result)


def log():
    return a.log.read_text(errors='replace') if a.log.exists() else ''


def wait_for(marker, seconds=90):
    until = time.monotonic() + seconds
    while time.monotonic() < until:
        if marker in log():
            return
        time.sleep(1)
    screen('TIMEOUT')
    raise RuntimeError('Guest marker not observed: ' + marker)


command('#include "QA/CHECK.HC";')
wait_for('READY')
if a.restart_check:
    command('#include "READ.HC";')
    command('U8 *s=DocSave(DocPut); BookMark(s); Free(s);')
    wait_for('Read bytes: 30')
    assert 'A small work, made with care.' in log()
    command('U8 *s=FileRead("KEEP.TXT"); BookMark(s); Free(s);')
    wait_for('PERSISTENCE-OK')
    screen('RESTART-PERSISTENCE')
    print('RESTART PERSISTENCE PASSED', flush=True)
    q.command('quit')
    raise SystemExit(0)

screen('STARTUP')
command('#include "QA/BATCH.HC";')
wait_for('ALL NONINTERACTIVE DONE')
screen('BATCH')
print('18 noninteractive examples complete', flush=True)

command('#include "INPUT.HC";')
command('Ada')
command('BookDump;')
wait_for('Hello, Ada.')
screen('INPUT')

for name in ('LIGHT', 'PALETTE', 'SHAPES'):
    command('#include "' + name + '.HC";')
    screen(name)
    q.key('spc')
    time.sleep(2)
    print(name + ' captured and returned', flush=True)

command('#include "MOVE.HC";')
screen('MOVE-START')
q.key('d'); q.key('d'); time.sleep(1)
screen('MOVE-RIGHT')
q.key('a'); time.sleep(1)
screen('MOVE-LEFT')
q.key('q'); time.sleep(2)
command('BookMark(MStrPrint("MOVE-X=%d",pilgrim_x));')
wait_for('MOVE-X=108')

command('#include "GARDEN.HC";')
screen('GARDEN-START')
for key in '1234567':
    q.key(key)
time.sleep(1)
screen('GARDEN-ALL')
q.key('4'); q.key('0'); time.sleep(1)
screen('GARDEN-INVALID')
q.key('q'); time.sleep(2)
command('BookMark(MStrPrint("GARDEN-MASK=%d",garden_lit));')
wait_for('GARDEN-MASK=119')
command('Garden;')
q.key('r'); time.sleep(1)
screen('GARDEN-RESET')
q.key('q'); time.sleep(2)
command('BookMark(MStrPrint("RESET-MASK=%d",garden_lit));')
wait_for('RESET-MASK=0')
command('FileWrite("KEEP.TXT","PERSISTENCE-OK",14);')
command('BookMark("ALL 24 COMPLETED");')
wait_for('ALL 24 COMPLETED')
screen('FINAL')
(a.screens / 'result.json').write_text(json.dumps({'cases':24,'noninteractive':18,
    'input':'Ada','move_x':108,'garden_mask':119,'reset_mask':0,
    'persistence_written':True,'requires_visual_review':True},indent=2)+'\n')
print('24 examples exercised; inspect screenshots and restart for persistence', flush=True)
q.command('quit')
