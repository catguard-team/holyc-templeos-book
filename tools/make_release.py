#!/usr/bin/env python3
"""Make the complete local release ZIP. Does not publish or invoke CI.
SPDX-License-Identifier: CC0-1.0
"""
import json
from pathlib import Path
import zipfile
from verify_archive import sha256, verify

ROOT = Path(__file__).resolve().parents[1]
VERSION = '1.0.0'
TOP_FILES = {'.gitattributes', '.gitignore', 'AGENTS.md', 'LICENSE', 'README.md',
             'Start-mac.command', 'Start-Windows.cmd', 'start-linux.sh'}
TOP_DIRS = {'archive', 'assets', 'book', 'docs', 'editable', 'evidence', 'examples',
            'licenses', 'manuscript', 'preview', 'runtime', 'tests', 'tools'}


def files():
    for p in sorted(ROOT.rglob('*')):
        rel = p.relative_to(ROOT)
        if rel.parts[0] not in TOP_DIRS and rel.as_posix() not in TOP_FILES:
            continue
        if any(x in {'.DS_Store', '__pycache__'} for x in rel.parts) or p.suffix in {'.pyc', '.idlk'}:
            continue
        if p.is_symlink():
            raise ValueError('Do not package symlinks: ' + str(rel))
        if p.is_file():
            if p.stat().st_size >= 100 * 1024 * 1024:
                raise ValueError('Split oversized Git file: ' + str(rel))
            yield p


def main():
    paths = list(files())
    manifest = {'schema': 1, 'version': VERSION, 'algorithm': 'SHA-256',
                'excludes': ['archive-manifest.json (self)', '.git/', 'state/', 'dist/', 'caches'],
                'files': [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
                           'sha256': sha256(p)} for p in paths]}
    mp = ROOT / 'archive-manifest.json'
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    result = verify(ROOT)
    dist = ROOT / 'dist'; dist.mkdir(exist_ok=True)
    dest = dist / ('holyc-templeos-book-v' + VERSION + '.zip')
    prefix = 'holyc-templeos-book-v' + VERSION + '/'
    with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for p in sorted(paths + [mp]):
            info = zipfile.ZipInfo(prefix + p.relative_to(ROOT).as_posix(), (2026, 11, 8, 0, 0, 0))
            info.create_system = 3
            info.external_attr = (0o100755 if p.stat().st_mode & 0o111 else 0o100644) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    checksum = sha256(dest)
    (dist / 'SHA256SUMS.txt').write_text(checksum + '  ' + dest.name + '\n', encoding='ascii')
    print(json.dumps({**result, 'zip': str(dest.relative_to(ROOT)),
                      'zip_bytes': dest.stat().st_size, 'zip_sha256': checksum}, indent=2))


if __name__ == '__main__':
    main()
