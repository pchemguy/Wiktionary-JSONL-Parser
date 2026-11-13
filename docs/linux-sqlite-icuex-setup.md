# Linux setup for Python with SQLiteICUex

Build a separate CPython whose standard `sqlite3` module links to SQLite with [SQLiteICUex](https://github.com/pchemguy/SQLiteICUex) built in. New connections register `UTF_CI` automatically. This recipe was checked on Debian 13 x86-64 with CPython 3.12.14, SQLite 3.54.1, and ICU 76.1.

## Prerequisites

Use Bash, a C toolchain, Make, Git, curl, Python 3, `dpkg-deb`, `sha256sum`, tar, and xz. Debian's ICU 76 runtime must already be available to the linker and loader. The commands extract matching Debian headers into the build directory, so they can run as an ordinary user. They download sources and write a private Python installation. Optional CPython modules depend on the development headers available on the host.

Run the blocks in order in the same shell, starting at the root of this repository. Keep the build directory after installation because the installed Python extension's runpath points to the SQLite library there.

## Download and pin the sources

```bash
set -eu

repo_root="$PWD"
test -f "$repo_root/docs/dev/spec/schema.sql"
build_root="$(mktemp -d "$repo_root/../sqlite-icuex-build.XXXXXX")"
build_root="$(cd "$build_root" && pwd -P)"
cd "$build_root"
mkdir downloads lib python-build

curl -fLsS https://www.python.org/ftp/python/3.12.14/Python-3.12.14.tar.xz -o downloads/python.tar.xz
curl -fLsS https://www.sqlite.org/2026/sqlite-amalgamation-3540100.zip -o downloads/sqlite.zip
curl -fLsS https://deb.debian.org/debian/pool/main/i/icu/libicu-dev_76.1-4_amd64.deb -o downloads/libicu-dev.deb

sha256sum -c <<'EOF'
5c8462af5790baf43a321a1559dbe0db06d1be4300fb85fb53c40060668e548a  downloads/python.tar.xz
0a9c8e34352dad46006aa82836d5383bff9dc6bc9ce5a60553c05aa30e6ad1f9  downloads/sqlite.zip
856ea1b86a008d71d3ffaf6a4a465ff38edf3a257ebab3f0222ce05fe94a5c1a  downloads/libicu-dev.deb
EOF

git init -q SQLiteICUex
git -C SQLiteICUex fetch -q --depth 1 https://github.com/pchemguy/SQLiteICUex.git 29d5266d52b6a889ec43a472339a417f4e4e2826
git -C SQLiteICUex checkout -q --detach FETCH_HEAD

tar -xf downloads/python.tar.xz
python3 -m zipfile -e downloads/sqlite.zip .
dpkg-deb -x downloads/libicu-dev.deb icu-dev
```

## Build SQLite and CPython

```bash
sqlite_src="$build_root/sqlite-amalgamation-3540100"
cc -std=c99 -O2 -fPIC \
  -DSQLITE_EXTRA_AUTOEXT=sqlite3IcuexInit \
  -DSQLITE_ENABLE_COLUMN_METADATA -DSQLITE_ENABLE_FTS3 \
  -DSQLITE_ENABLE_FTS3_PARENTHESIS -DSQLITE_ENABLE_FTS4 \
  -DSQLITE_ENABLE_FTS5 -DSQLITE_ENABLE_RTREE -DSQLITE_ENABLE_MATH_FUNCTIONS \
  -c "$sqlite_src/sqlite3.c" -o "$build_root/sqlite3.o"
cc -std=c99 -O2 -fPIC -DSQLITE_CORE \
  -I"$sqlite_src" -I"$build_root/icu-dev/usr/include" \
  -c "$build_root/SQLiteICUex/src/icuex.c" -o "$build_root/icuex.o"
cc -shared -Wl,-soname,libsqlite3.so.0 -Wl,--no-undefined \
  "$build_root/sqlite3.o" "$build_root/icuex.o" \
  -Wl,-l:libicui18n.so.76 -Wl,-l:libicuuc.so.76 -Wl,-l:libicudata.so.76 \
  -ldl -lpthread -lm -o "$build_root/lib/libsqlite3.so.0"
ln -s libsqlite3.so.0 "$build_root/lib/libsqlite3.so"

cd "$build_root/python-build"
LIBSQLITE3_CFLAGS="-I$sqlite_src" \
LIBSQLITE3_LIBS="-L$build_root/lib -Wl,-rpath,$build_root/lib -lsqlite3" \
  "$build_root/Python-3.12.14/configure" \
  --prefix="$build_root/python-install" --without-ensurepip --enable-loadable-sqlite-extensions
make -j"${BUILD_JOBS:-4}"
make altinstall
```

`SQLITE_EXTRA_AUTOEXT` registers SQLiteICUex when each connection opens. CPython's `LIBSQLITE3_CFLAGS` and `LIBSQLITE3_LIBS` bind its `_sqlite3` module to the custom library. The private install leaves the system Python and SQLite untouched.

## Verify the linked runtime

```bash
python_icu="$build_root/python-install/bin/python3.12"
env -u LD_LIBRARY_PATH -u PYTHONHOME "$python_icu" -I - "$repo_root/docs/dev/spec/schema.sql" <<'PY'
from pathlib import Path
import sqlite3
import sys

assert sqlite3.sqlite_version == "3.54.1", sqlite3.sqlite_version
with sqlite3.connect(":memory:") as conn:
    collations = {row[1] for row in conn.execute("PRAGMA collation_list")}
    assert {"UTF_CI", "UTF_CI_AI"} <= collations, collations
    assert conn.execute(
        "SELECT ? = ? COLLATE UTF_CI, ? = ? COLLATE UTF_CI",
        ("\u0401\u043b\u043a\u0430", "\u0451\u043b\u043a\u0430", "\u0451", "\u0435"),
    ).fetchone() == (1, 0)
    conn.executescript(Path(sys.argv[1]).read_text(encoding="utf-8"))

print("SQLite 3.54.1, ICUex collations, and the project schema are available.")
PY
printf 'Use this interpreter for the project: %s\n' "$python_icu"
```

If the linker cannot find `libicui18n.so.76`, verify that Debian's `libicu76` runtime is installed. If the collation check fails, run `ldd` on the installed `_sqlite3` extension and check that it resolves `libsqlite3.so.0` from the private build directory.
