# Release tool

`build_release.py` builds the Python source distribution and wheel from the checkout and prepares the two GitHub release downloads. Run it with Python 3.11 or later and the `build` package. Use a repository checkout with the bundled release inventory checker.

```bash
python tools/build_release.py
```

The build writes the installable distributions to `dist/` and stages `wiktionary-jsonl-parser-python.zip` and `SHA256SUMS` in `release/`. The ZIP uses the distributions' installable filenames internally. The script reads the version from `pyproject.toml` and checks the full staging inventory. It does not create a tag or upload files.

Use `--dist PATH` and `--release PATH` to select alternate directories. The staging directory must be absent or empty. To build without an isolated build environment, supply `--no-isolation` and provide Hatchling and its dependencies to the same interpreter. Verify the bundle from the staging directory with `sha256sum -c SHA256SUMS`.
