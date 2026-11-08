"""Meaningful integrity and persistence checks; no paid or external services."""
from pathlib import Path
import gzip
import hashlib
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import launch


class RestoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / '경로 space,comma'
        (self.root / 'runtime').mkdir(parents=True)
        self.raw = b'boot-data' + bytes(2 * launch.CHUNK) + b'last-byte'
        self.arc = self.root / 'runtime/factory.gz'
        self.arc.write_bytes(gzip.compress(self.raw, mtime=0))
        self.entry = dict(path='runtime/factory.gz', raw_bytes=len(self.raw),
                          raw_sha256=hashlib.sha256(self.raw).hexdigest(),
                          compressed_bytes=self.arc.stat().st_size,
                          compressed_sha256=launch.digest(self.arc))
        self.iso = self.root / 'original.iso'
        self.iso.write_bytes(b'original')
        self.manifest = {'factory_disk': self.entry, 'boot_iso': {
            'path': 'original.iso', 'bytes': 8, 'sha256': launch.digest(self.iso)}}
        self.write_manifest()
        self.state = self.root / '내 작업'
        self.state.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        (self.root / 'runtime/manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def test_restore_exact_bytes_and_keep_modified_disk(self):
        archive, entry = launch.load_factory(self.root)
        with launch.state_lock(self.state):
            disk, created = launch.restore_factory(archive, entry, self.state)
        self.assertTrue(created)
        self.assertEqual(disk.read_bytes(), self.raw)
        with disk.open('r+b') as f:
            f.write(b'MY NOTES!')
        with launch.state_lock(self.state):
            same, created = launch.restore_factory(archive, entry, self.state)
        self.assertFalse(created)
        self.assertEqual(same.read_bytes()[:9], b'MY NOTES!')

    def test_compressed_hash_failure(self):
        self.arc.write_bytes(b'not an archive')
        with self.assertRaises(ValueError):
            launch.load_factory(self.root)
        self.assertFalse((self.state / 'TempleOS.img').exists())

    def test_wrong_raw_hash_leaves_no_disk(self):
        self.entry['raw_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            launch.restore_factory(self.arc, self.entry, self.state)
        self.assertEqual(list(self.state.iterdir()), [])

    def test_declared_size_limits_decompression(self):
        self.entry['raw_bytes'] = 10
        with self.assertRaises(ValueError):
            launch.restore_factory(self.arc, self.entry, self.state)
        self.assertFalse((self.state / 'TempleOS.img').exists())

    def test_existing_file_is_never_replaced(self):
        p = self.state / 'TempleOS.img'
        p.write_bytes(b'user disk without receipt')
        with self.assertRaises(ValueError):
            launch.restore_factory(self.arc, self.entry, self.state)
        self.assertEqual(p.read_bytes(), b'user disk without receipt')

    def test_manifest_path_escape_is_rejected(self):
        self.entry['path'] = '../outside.gz'
        self.write_manifest()
        with self.assertRaises(ValueError):
            launch.load_factory(self.root)

    def test_original_iso_integrity(self):
        self.iso.write_bytes(b'changed!')
        with self.assertRaises(ValueError):
            launch.load_factory(self.root)

    @unittest.skipIf(sys.platform == 'win32', 'symlinks require privileges on Windows')
    def test_symlink_disk_not_followed(self):
        p = self.root / 'valuable'
        p.write_bytes(b'keep')
        (self.state / 'TempleOS.img').symlink_to(p)
        with self.assertRaises(ValueError):
            launch.restore_factory(self.arc, self.entry, self.state)
        self.assertEqual(p.read_bytes(), b'keep')

    def test_concurrent_state_lock(self):
        with launch.state_lock(self.state):
            with self.assertRaises(RuntimeError):
                with launch.state_lock(self.state):
                    pass

    def test_windows_command_quoting_and_machine(self):
        disk = r'C:\Users\Learner\자료 folder,1\TempleOS.img'
        cmd = launch.qemu_options(r'C:\Program Files\qemu\qemu-system-x86_64.exe', disk,
                                  system='Windows', sound=True, iso='original.iso')
        self.assertEqual(cmd[0], r'C:\Program Files\qemu\qemu-system-x86_64.exe')
        self.assertIn('file=' + disk.replace(',', ',,') + ',format=raw,if=ide,index=0', cmd)
        self.assertIn('dsound,id=bookaudio', cmd)
        self.assertEqual(cmd[cmd.index('-accel') + 1], 'tcg')
        self.assertEqual(cmd[cmd.index('-nic') + 1], 'none')


if __name__ == '__main__':
    unittest.main()
