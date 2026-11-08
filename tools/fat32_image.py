"""Make a small, disposable FAT32 transfer image using only Python stdlib.

The output must be a new ordinary file. No device paths or overwrites.
SPDX-License-Identifier: CC0-1.0
"""
from pathlib import Path
import re
import struct


def write_image(path, files):
    path = Path(path)
    if path.exists() or path.is_symlink():
        raise FileExistsError(path)
    if len(files) > 120:
        raise ValueError('Too many root entries')
    if any(not re.fullmatch(r'[A-Z0-9_]{1,8}\.[A-Z0-9]{1,3}', n) for n in files):
        raise ValueError('Use uppercase 8.3 names')
    if any(not isinstance(b, bytes) or not b for b in files.values()):
        raise ValueError('Files must contain nonempty bytes')
    start, total, spc, reserved, fat_sectors = 2048, 1048576, 8, 32, 1024
    def put32(buf, off, val):
        struct.pack_into('<I', buf, off, val)
    mbr = bytearray(512)
    mbr[446:462] = struct.pack('<B3sB3sII', 0, b'\x00\x02\x00', 0x0c,
                             b'\xfe\xff\xff', start, total)
    mbr[510:] = b'\x55\xaa'
    boot = bytearray(512)
    boot[:3], boot[3:11] = b'\xeb\x58\x90', b'MSDOS5.0'
    struct.pack_into('<HBHBHHBHHHII', boot, 11, 512, spc, reserved, 2,
                     0, 0, 0xf8, 0, 63, 255, start, total)
    struct.pack_into('<IHHIHH', boot, 36, fat_sectors, 0, 0, 2, 1, 6)
    boot[64], boot[66] = 0x80, 0x29
    put32(boot, 67, 0x20261108)
    boot[71:82], boot[82:90], boot[510:] = b'HOLYC BOOK ', b'FAT32   ', b'\x55\xaa'
    info = bytearray(512)
    for off, val in [(0, 0x41615252), (484, 0x61417272), (488, 0xffffffff),
                     (492, 0xffffffff), (508, 0xaa550000)]:
        put32(info, off, val)
    fat = bytearray(fat_sectors * 512)
    for off, val in [(0, 0x0ffffff8), (4, 0xffffffff), (8, 0x0fffffff)]:
        put32(fat, off, val)
    root = bytearray(spc * 512)
    data, cluster = [], 3
    for i, (name, content) in enumerate(sorted(files.items())):
        stem, ext = name.split('.')
        entry = bytearray(32)
        entry[:11], entry[11] = (stem.ljust(8) + ext.ljust(3)).encode('ascii'), 0x20
        struct.pack_into('<H', entry, 20, cluster >> 16)
        struct.pack_into('<H', entry, 26, cluster & 65535)
        put32(entry, 28, len(content))
        root[i * 32:i * 32 + 32] = entry
        count = (len(content) + spc * 512 - 1) // (spc * 512)
        if cluster + count >= len(fat) // 4:
            raise ValueError('Files exceed transfer image capacity')
        for j in range(count):
            put32(fat, (cluster + j) * 4,
                  cluster + j + 1 if j < count - 1 else 0x0fffffff)
        data.append((cluster, content))
        cluster += count
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as f:
        f.truncate((start + total) * 512)
        f.write(mbr)
        for sector, buf in [(0, boot), (1, info), (6, boot), (7, info),
                            (reserved, fat), (reserved + fat_sectors, fat)]:
            f.seek((start + sector) * 512)
            f.write(buf)
        base = start + reserved + 2 * fat_sectors
        f.seek(base * 512)
        f.write(root)
        for c, buf in data:
            f.seek((base + (c - 2) * spc) * 512)
            f.write(buf)
    return path
