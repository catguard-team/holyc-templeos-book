#!/usr/bin/env python3
"""Restore the exact archived QEMU source tarball; never overwrite a file.
SPDX-License-Identifier: CC0-1.0
"""
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def restore(target):
    base = ROOT / 'archive/qemu'
    m = json.loads((base / 'manifest.json').read_text(encoding='utf-8'))
    target = Path(target)
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    h, size, created = hashlib.sha256(), 0, False
    try:
        with target.open('xb') as out:
            created = True
            for entry in m['parts']:
                name = entry['file']
                if Path(name).name != name or '/' in name or '\\' in name:
                    raise ValueError('Invalid part path')
                data = (base / name).read_bytes()
                if len(data) != entry['bytes'] or hashlib.sha256(data).hexdigest() != entry['sha256']:
                    raise ValueError('Part hash mismatch: ' + name)
                out.write(data)
                h.update(data)
                size += len(data)
        if size != m['bytes'] or h.hexdigest() != m['sha256']:
            raise ValueError('Complete source archive mismatch')
    except BaseException:
        if created:
            target.unlink(missing_ok=True)
        raise
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    print(restore(args.output))
