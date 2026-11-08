#!/usr/bin/env python3
"""Persistent, offline TempleOS lab for macOS, Linux and Windows.

Python 3.10+ and an installed QEMU are the only runtime prerequisites.
SPDX-License-Identifier: CC0-1.0
"""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
CHUNK = 1024 * 1024
ZERO = bytes(CHUNK)


def digest(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(CHUNK), b''):
            h.update(b)
    return h.hexdigest()


def load_factory(root=ROOT):
    manifest = json.loads((root / 'runtime/manifest.json').read_text(encoding='utf-8'))
    iso = manifest['boot_iso']
    iso_path = (root / iso['path']).resolve()
    if not iso_path.is_relative_to(root.resolve()) or not iso_path.is_file():
        raise ValueError('Original ISO is missing or outside the repository')
    if iso_path.stat().st_size != iso['bytes'] or digest(iso_path) != iso['sha256']:
        raise ValueError('Original ISO SHA-256/size mismatch')
    entry = manifest['factory_disk']
    archive = (root / entry['path']).resolve()
    if not archive.is_relative_to(root.resolve()):
        raise ValueError('Factory archive path leaves the repository')
    if not archive.is_file() or archive.stat().st_size != entry['compressed_bytes']:
        raise ValueError('Factory archive is missing or has the wrong size; verify the download')
    if digest(archive) != entry['compressed_sha256']:
        raise ValueError('Factory archive SHA-256 mismatch; verify the download')
    return archive, entry


@contextmanager
def state_lock(state):
    state.mkdir(parents=True, exist_ok=True)
    path = state / 'session.lock'
    if path.is_symlink():
        raise ValueError('Refusing a symlink lock file')
    with path.open('a+b') as f:
        if f.tell() == 0:
            f.write(b'0')
            f.flush()
        f.seek(0)
        if os.name == 'nt':
            import msvcrt
            lock = lambda: msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
            unlock = lambda: msvcrt.locking(f.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl
            lock = lambda: fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
            unlock = lambda: fcntl.flock(f, fcntl.LOCK_UN)
        try:
            lock()
        except OSError as e:
            raise RuntimeError('This lab state is already in use; close its other QEMU window') from e
        try:
            yield
        finally:
            f.seek(0)
            unlock()


def restore_factory(archive, entry, state):
    """Called under state_lock. Never replaces a user disk."""
    disk, receipt = state / 'TempleOS.img', state / 'initialized.json'
    if disk.is_symlink() or receipt.is_symlink():
        raise ValueError('Refusing symlink state files')
    if disk.exists():
        if not disk.is_file() or not receipt.is_file():
            raise ValueError('Existing disk has no initialization receipt; preserve it and use --state NEW_FOLDER')
        old = json.loads(receipt.read_text(encoding='utf-8'))
        if disk.stat().st_size != old.get('raw_bytes'):
            raise ValueError('Existing disk size changed; preserve it and use --state NEW_FOLDER')
        return disk, False
    if receipt.exists():
        raise ValueError('Receipt exists without its disk; use --state NEW_FOLDER')
    if shutil.disk_usage(state).free < entry['raw_bytes'] + 64 * CHUNK:
        raise ValueError('Allow at least 2.1 GiB of free space for the writable lab disk')
    h, count, created = hashlib.sha256(), 0, False
    try:
        with disk.open('xb') as dst:
            created = True
            with gzip.open(archive, 'rb') as src:
                for block in iter(lambda: src.read(CHUNK), b''):
                    count += len(block)
                    if count > entry['raw_bytes']:
                        raise ValueError('Factory disk exceeds its declared size')
                    h.update(block)
                    # Holes reduce disk use where the filesystem supports them.
                    if block == ZERO[:len(block)]:
                        dst.seek(len(block), 1)
                    else:
                        dst.write(block)
            dst.truncate(count)
            dst.flush()
            os.fsync(dst.fileno())
        if count != entry['raw_bytes'] or h.hexdigest() != entry['raw_sha256']:
            raise ValueError('Restored factory disk SHA-256/size mismatch')
        with receipt.open('x', encoding='utf-8') as f:
            json.dump({'raw_bytes': count, 'initial_sha256': h.hexdigest(),
                       'template_sha256': entry['compressed_sha256']}, f, indent=2)
            f.write('\n')
        return disk, True
    except BaseException:
        if created:
            disk.unlink(missing_ok=True)
        raise


def qemu_candidates(system=None, environ=None):
    system, environ = system or platform.system(), environ or os.environ
    candidates = ['qemu-system-x86_64']
    if system == 'Windows':
        candidates = ['qemu-system-x86_64.exe']
        for env in ('ProgramFiles', 'ProgramFiles(x86)'):
            if environ.get(env):
                candidates.append(str(Path(environ[env]) / 'qemu/qemu-system-x86_64.exe'))
    elif system == 'Darwin':
        candidates += ['/opt/homebrew/bin/qemu-system-x86_64', '/usr/local/bin/qemu-system-x86_64',
                       '/opt/local/bin/qemu-system-x86_64']
    return candidates


def find_qemu(explicit=None):
    for candidate in ([explicit] if explicit else qemu_candidates()):
        found = shutil.which(candidate)
        if found:
            return found
    raise FileNotFoundError('QEMU not found. Install qemu-system-x86_64 using docs/PLATFORMS.md, or pass --qemu PATH')


def qemu_options(executable, disk, *, headless=False, sound=False, wav=None, system=None, iso=None):
    system = system or platform.system()
    machine = 'pc'
    audio = []
    if wav:
        machine += ',pcspk-audiodev=bookaudio'
        audio = ['-audiodev', 'wav,id=bookaudio,path=' + str(wav).replace(',', ',,')]
    elif sound:
        backend = {'Darwin': 'coreaudio', 'Windows': 'dsound', 'Linux': 'pa'}.get(system)
        if not backend:
            raise ValueError('No default audio backend for this host')
        machine += ',pcspk-audiodev=bookaudio'
        audio = ['-audiodev', backend + ',id=bookaudio']
    args = [executable, '-name', 'HolyC TempleOS Book', '-machine', machine,
            '-accel', 'tcg', '-cpu', 'qemu64', '-m', '512', '-smp', '1',
            '-drive', 'file=' + str(disk).replace(',', ',,') + ',format=raw,if=ide,index=0',
            '-cdrom', str(iso or ROOT / 'archive/templeos/TempleOS.ISO'),
            '-boot', 'c', '-vga', 'std', '-nic', 'none', '-rtc', 'base=localtime']
    if headless:
        args += ['-display', 'none']
    return args + audio


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qemu', help='Path to qemu-system-x86_64')
    ap.add_argument('--state', type=Path, default=ROOT / 'state', help='Persistent lab directory; new folder creates a fresh lab')
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument('--doctor', action='store_true', help='Check prerequisites/archive without starting a VM')
    mode.add_argument('--prepare', action='store_true', help='Restore and validate a new disk without starting QEMU')
    mode.add_argument('--dry-run', action='store_true', help='Print command as JSON without writing state')
    ap.add_argument('--sound', action='store_true', help='Enable PC speaker (CoreAudio / PulseAudio / DirectSound)')
    ap.add_argument('--headless', action='store_true', help=argparse.SUPPRESS)
    ap.add_argument('--qmp-socket', type=Path, help=argparse.SUPPRESS)
    ap.add_argument('--debug-log', type=Path, help=argparse.SUPPRESS)
    ap.add_argument('--capture-wav', type=Path, help=argparse.SUPPRESS)
    opts = ap.parse_args(argv)
    archive, entry = load_factory()
    if opts.prepare:
        executable = None
    else:
        executable = find_qemu(opts.qemu)
    if opts.doctor:
        result = subprocess.run([executable, '--version'], check=True, capture_output=True, text=True)
        print(json.dumps({'host': platform.system(), 'machine': platform.machine(),
                          'python': platform.python_version(), 'qemu': result.stdout.splitlines()[0],
                          'factory_archive': 'SHA-256 verified'}, ensure_ascii=False, indent=2))
        return 0
    state = opts.state.expanduser().resolve()
    args = qemu_options(executable or 'qemu-system-x86_64', state / 'TempleOS.img',
                        headless=opts.headless, sound=opts.sound, wav=opts.capture_wav)
    if opts.qmp_socket:
        if os.name == 'nt':
            raise ValueError('The maintainer QMP socket option is Unix-only')
        args += ['-qmp', 'unix:' + str(opts.qmp_socket) + ',server=on,wait=off']
    if opts.debug_log:
        args += ['-debugcon', 'file:' + str(opts.debug_log), '-global', 'isa-debugcon.iobase=0xe9']
    if opts.dry_run:
        print(json.dumps(args, ensure_ascii=False, indent=2))
        return 0
    with state_lock(state):
        disk, created = restore_factory(archive, entry, state)
        print(('Created' if created else 'Keeping') + ' lab disk: ' + str(disk), flush=True)
        if opts.prepare:
            return 0
        print('At TempleOS Boot Loader, press 1 then Enter for Drive C.', flush=True)
        print('Close the QEMU window to stop. Saved files remain in this lab disk.', flush=True)
        return subprocess.run(args, check=False).returncode


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as e:
        print('HolyC lab: ' + str(e), file=sys.stderr)
        raise SystemExit(1)
