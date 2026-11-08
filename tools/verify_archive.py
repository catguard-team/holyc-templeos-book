#!/usr/bin/env python3
"""Check the locally archived release files without network access.
SPDX-License-Identifier: CC0-1.0
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def verify(root=ROOT):
    manifest = json.loads((root / 'archive-manifest.json').read_text(encoding='utf-8'))
    failed, seen = [], set()
    for entry in manifest['files']:
        name = entry['path']
        relative = PurePosixPath(name)
        if relative.is_absolute() or '..' in relative.parts or '\\' in name or name in seen:
            raise ValueError('Invalid/duplicate archive path: ' + name)
        seen.add(name)
        path = root / relative
        if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
            failed.append(name + ': unsafe path')
        elif not path.is_file():
            failed.append(name + ': missing')
        elif path.stat().st_size != entry['bytes'] or sha256(path) != entry['sha256']:
            failed.append(name + ': size/hash mismatch')
    if failed:
        raise ValueError('\n'.join(failed))
    return {'verified_files': len(seen), 'verified_bytes': sum(x['bytes'] for x in manifest['files']),
            'status': 'all SHA-256 values match'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    print(json.dumps(verify(), indent=2))
