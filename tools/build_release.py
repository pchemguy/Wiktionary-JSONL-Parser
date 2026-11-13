"""Build Python distributions and stage the two GitHub release downloads."""

import argparse
import hashlib
import json
import subprocess
import sys
import tomllib
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = "wiktionary_jsonl_parser"
BUNDLE = "wiktionary-jsonl-parser-python.zip"
CHECKSUMS = "SHA256SUMS"
GATE = ROOT / ".agents/plugins/sdd-manager/skills/sdd-verify/scripts/release_assets.py"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    parser.add_argument("--release", type=Path, default=ROOT / "release")
    parser.add_argument("--no-isolation", action="store_true")
    args = parser.parse_args()

    dist = args.dist.resolve()
    release = args.release.resolve()
    if dist == release or dist in release.parents or release in dist.parents:
        parser.error("--dist and --release must be separate directories")
    if release.exists() and (not release.is_dir() or any(release.iterdir())):
        parser.error("--release must be absent or an empty directory")

    with (ROOT / "pyproject.toml").open("rb") as metadata:
        version = tomllib.load(metadata)["project"]["version"]
    if not GATE.is_file():
        parser.error("the release gate must be available from a repository checkout")

    command = [sys.executable, "-m", "build", "--outdir", str(dist)]
    if args.no_isolation:
        command.append("--no-isolation")
    subprocess.run(command, cwd=ROOT, check=True)
    wheel = dist / f"{PACKAGE}-{version}-py3-none-any.whl"
    source = dist / f"{PACKAGE}-{version}.tar.gz"

    release.mkdir(parents=True, exist_ok=True)
    bundle = release / BUNDLE
    with ZipFile(bundle, "x", compression=ZIP_DEFLATED) as archive:
        for package in (wheel, source):
            archive.write(package, package.name)
    with bundle.open("rb") as stream:
        sha256 = hashlib.file_digest(stream, "sha256").hexdigest()
    with (release / CHECKSUMS).open("x", encoding="ascii", newline="\n") as stream:
        stream.write(f"{sha256}  {BUNDLE}\n")

    with TemporaryDirectory() as temporary:
        expected = Path(temporary) / "expected.json"
        expected.write_text(json.dumps([BUNDLE, CHECKSUMS]), encoding="utf-8")
        subprocess.run(
            [
                sys.executable,
                str(GATE),
                "--expected",
                str(expected),
                "--directory",
                str(release),
                "--version",
                version,
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
