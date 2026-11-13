"""Read-only complete-inventory artifact-name check; Python 3.11+, no packages."""
import argparse
import json
from pathlib import Path
import re
import unicodedata

# No artifact-type/extension selection. A reviewed stable contract is required
# in addition to detecting version notation and the selected release value.
DOTTED = re.compile(r'\d+\.\d+')
COMPONENTS = re.compile(r'(?<![a-z0-9])\d+(?:[-_]\d+){2,}(?![a-z0-9])', re.I)
MARKED = re.compile(r'(?<![a-z0-9])(?:v|ver|version|release|rev|r)[-_ ]?\d+(?![a-z0-9])', re.I)


def _names(values, label):
    if not isinstance(values, list) or any(not isinstance(x, str) or not x or
            x in ('.', '..') or '/' in x or '\\' in x or
            any(ord(c) < 32 or ord(c) == 127 for c in x) for x in values):
        raise ValueError(label + ' must contain plain artifact names')
    if len({x.casefold() for x in values}) != len(values):
        raise ValueError(label + ' contains duplicate/colliding names')
    return values


def check_names(expected, observed, release_version, *, complete=True):
    """Reject prohibited names even in the expected contract; cover every name.

    expected is independently reviewed, never copied from the generator.
    observed is the complete staged/provider inventory. Partial draft checks
    may omit missing names but cannot certify complete release acceptance.
    This does not inspect content, checksums, source identity or permissions.
    """
    if not isinstance(release_version, str) or not release_version.strip():
        raise ValueError('Release version is required')
    expected = _names(expected, 'Expected inventory')
    observed = _names(observed, 'Actual inventory')
    if not expected:
        raise ValueError('Expected inventory is empty')
    version = release_version.removeprefix('v').removeprefix('V').casefold()
    if not version or version.strip() != version or any(c.isspace() for c in version):
        raise ValueError('Release version is invalid')
    core = re.split(r'[-+]', version, maxsplit=1)[0]
    forms = {version, core, core.replace('.', '_'), core.replace('.', '-')}
    for name in expected + observed:
        normal = unicodedata.normalize('NFKC', name).casefold()
        if (DOTTED.search(normal) or COMPONENTS.search(normal) or MARKED.search(normal)
                or any(form and form in normal for form in forms)):
            raise ValueError('Version numbers in ANY release artifact name are absolutely prohibited: ' + name)
    if set(observed) - set(expected):
        raise ValueError('Unexpected artifact names')
    if complete and set(observed) != set(expected):
        raise ValueError('Incomplete artifact inventory')
    return {'ok': True, 'complete': complete, 'checked': len(observed)}


def directory_names(directory):
    """Inspect every entry in a dedicated flat staging directory, no globbing."""
    root = Path(directory)
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Staging directory must be an ordinary directory')
    entries = list(root.iterdir())
    if any(p.is_symlink() or not p.is_file() for p in entries):
        raise ValueError('Unexamined directory/link/special entry in artifact staging')
    return sorted(p.name for p in entries)


def verify_checker(checker=check_names):
    """Exercise the actual checker/adapter against the public contract vectors."""
    vectors = json.loads(Path(__file__).with_name('release-asset-cases.json').read_text(encoding='utf-8'))
    version = vectors['release_version']
    checker(vectors['valid'], vectors['valid'], version)
    checked = len(vectors['valid'])
    for marker in vectors['invalid_markers']:
        for suffix in vectors['suffixes']:
            name = 'sample-' + marker + suffix
            try:
                checker([name], [name], version)
            except ValueError:
                checked += 1
            else:
                raise ValueError('Checker accepts prohibited version notation: ' + name)
    return {'ok': True, 'contract_vectors_checked': checked}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', help='JSON array of independently reviewed stable names')
    parser.add_argument('--version')
    parser.add_argument('--self-test', action='store_true')
    actual = parser.add_mutually_exclusive_group()
    actual.add_argument('--directory', help='Dedicated complete artifact staging directory')
    actual.add_argument('--observed', help='Complete provider name inventory as a JSON array')
    args = parser.parse_args(argv)
    try:
        if args.self_test:
            if args.expected or args.version or args.directory or args.observed:
                raise ValueError('Self-test cannot be mixed with artifact inputs')
            print(json.dumps(verify_checker()))
            return 0
        if not args.expected or not args.version or not (args.directory or args.observed):
            raise ValueError('Expected inventory, version and complete actual inventory are required')
        expected = json.loads(Path(args.expected).read_text(encoding='utf-8'))
        observed = directory_names(args.directory) if args.directory else json.loads(Path(args.observed).read_text(encoding='utf-8'))
        result = check_names(expected, observed, args.version)
    except (ValueError, OSError) as error:
        print(json.dumps({'ok': False, 'error': str(error)}, ensure_ascii=True))
        return 1
    print(json.dumps(result))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
