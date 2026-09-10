"""Fail closed on unexpected files in the exact Pages artifact."""
import json
from pathlib import Path
from audit_publication import findings

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'preview/dist'


def main():
    errors = []
    files = list(DIST.rglob('*'))
    for path in files:
        rel = path.relative_to(DIST).as_posix()
        if path.is_symlink():
            errors.append(rel)
        elif path.is_file():
            allowed = rel in {'index.html', 'data/nahuatl-br.json'} or (
                path.parent == DIST / 'assets' and path.suffix in {'.js', '.css'})
            if not allowed or findings(path.read_bytes()):
                errors.append(rel)
    canonical = ROOT / 'preview/public/data/nahuatl-br.json'
    exported = DIST / 'data/nahuatl-br.json'
    if not (DIST / 'index.html').is_file() or not exported.is_file():
        errors.append('missing required files')
    elif exported.read_bytes() != canonical.read_bytes():
        errors.append('derived JSON differs')
    else:
        data = json.loads(exported.read_text(encoding='utf-8'))
        if (len(data['lemmas']) != data['counts']['lemmas'] or
                not 50 <= len(data['lemmas']) <= 500 or
                {'C01', 'C02', 'C03'} & data['sources'].keys()):
            errors.append('invalid corpus scope')
    print('PREVIEW_DIST_SECURITY: ' + ('FAIL' if errors else 'PASS'))
    for error in errors:
        print(error)
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
