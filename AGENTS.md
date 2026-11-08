# HolyC · TempleOS book archive

Last updated: 2026-11-08.

- New book text, examples, design and project tools are CC0-1.0. Preserve the separate licenses and provenance of `archive/`, `assets/fonts/` and `tools/vendor/`.
- No GitHub Actions, paid CI, paid APIs or cloud builders. Run checks locally. Repository Actions must remain disabled.
- `manuscript/content.py` is the Korean manuscript; `examples/` contains the exact tested HolyC files. `tools/build_book.py` builds the offline HTML with bundled dependencies. The designed PDF and original INDD/IDML are also preserved.
- TempleOS is the original 5.03 release. Do not silently substitute a fork. Keep the official ISO unmodified and pin original source/hash evidence. The ready disk adds only a documented book workspace and user startup files.
- Default launcher state is persistent and ignored by Git. Never overwrite an existing user disk. Verify the compressed factory image before extraction and the full raw image before first use. No host physical disks or networking are passed to the guest.
- Test restores in new directories, including spaces and non-ASCII paths. Check boot, examples, saved data after restart and archive hashes. Distinguish actual native tests from mocks/static inspection.
- Keep platform limits honest: macOS and Linux QEMU can be checked locally; Windows native execution requires a Windows host. Adobe InDesign itself does not run natively on Linux. PDF, offline HTML, manuscript and TempleOS labs are portable.
- Do not copy proprietary font programs, workspace secrets, local paths or unrelated repository material into this public repository. PDF font embedding does not relicense the fonts under CC0.
- Update README, provenance and verification evidence when files or verified behavior change.
- Public release 1.0.0 adds an original-ISO installed 2 GiB persistent lab disk, 24 exact examples, cross-platform stdlib launchers, QEMU 11.1.3 source parts/signature, open fonts and a self-contained HTML builder. Use `tools/verify_archive.py` for the current package hashes, `tools/check_guest_files.py IMAGE` for the unmodified seeded files, and `tools/make_release.py` for the complete ZIP. Never package `state/`, `.git/` or local caches.
- Integration tests use only disposable images and `tests/run_vm_qa.py` with QMP. Confirm the book prompt before sending input; inputs during the mount/boot UI can be consumed by the wrong prompt. The factory file must be stopped before hashing/compressing.
- The published PDF fixes only the Unicode Info/XMP title and license-scope subject from the native export. All 80 page renders, text, links and bookmarks were compared unchanged; see `evidence/pdf-public-metadata.json`.
