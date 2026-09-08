"""Read-only pre-publication scan of current files and reachable Git blobs.

Reports categories/locations only, never matched credential values. A finding
is a stop condition requiring human review, not permission to delete history.
"""

from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "PRIVATE_KEY": rb"-----BEGIN (?:RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY-----",
    "GITHUB_TOKEN": rb"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,})",
    "AWS_ACCESS_KEY": rb"(?:AKIA|ASIA)[A-Z0-9]{16}",
    "SLACK_TOKEN": rb"xox[baprs]-[A-Za-z0-9-]{20,}",
    "GOOGLE_API_KEY": rb"AIza[A-Za-z0-9_-]{30,}",
    "ASSIGNED_CREDENTIAL": rb'''(?im)\b(?:password|passwd|api_key|access_token|client_secret)["']?\s*[:=]\s*["']([^"'\r\n]{8,})["']''',
    "URL_CREDENTIAL": rb"https?://[^\s/:]+:[^\s/@]{8,}@",
}
COMPILED = {name: re.compile(pattern) for name, pattern in PATTERNS.items()}
FORBIDDEN_PATH = re.compile(
    r"(?i)(\.(pdf|zip|pem|key|p12|pfx|mp3|wav|ogg|flac|m4a|mp4|png|jpe?g|gif|webp)$"
    r"|(^|/)(\.env($|\.)|credentials?(\.|/|$)|tokens?(\.|/|$)|id_rsa$|id_ed25519$)"
    r"|^data/(raw|staging)/)"
)


def git(*args, input=None):
    return subprocess.check_output(["git", *args], cwd=ROOT, input=input)


def path_problem(path):
    return bool(FORBIDDEN_PATH.search(path)) or (
        path.startswith("sources/")
        and path != "sources/README.md"
        and Path(path).name != ".gitkeep"
    )


def findings(data):
    categories = [name for name, pattern in COMPILED.items() if pattern.search(data)]
    if data.startswith((b"%PDF-", b"PK\x03\x04", b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff")):
        categories.append("EXTERNAL_BINARY")
    return categories


def main():
    failures = []
    current = {p.decode("utf-8") for p in git("ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0") if p}
    for path in sorted(current):
        if path_problem(path):
            failures.append(("CURRENT_PATH", path))
        file = ROOT / path
        if file.is_file():
            failures.extend((category, "current:" + path) for category in findings(file.read_bytes()))

    commits = git("rev-list", "--all").decode("ascii").splitlines()
    historical_paths = set()
    for commit in commits:
        historical_paths.update(p.decode("utf-8") for p in git("ls-tree", "-r", "--name-only", "-z", commit).split(b"\0") if p)
    for path in sorted(historical_paths):
        if path_problem(path):
            failures.append(("HISTORICAL_PATH", path))

    objects = [line.split(b" ", 1)[0] for line in git("rev-list", "--objects", "--all").splitlines()]
    info = git("cat-file", "--batch-check", input=b"\n".join(objects) + b"\n")
    blobs = [line.split()[0] for line in info.splitlines() if line.split()[1] == b"blob"]
    data = git("cat-file", "--batch", input=b"\n".join(blobs) + b"\n")
    offset = 0
    for expected in blobs:
        end = data.index(b"\n", offset)
        oid, kind, size = data[offset:end].split()
        assert oid == expected and kind == b"blob"
        start = end + 1
        payload = data[start:start + int(size)]
        assert len(payload) == int(size)
        failures.extend((category, "blob:" + oid.decode("ascii")) for category in findings(payload))
        offset = start + int(size) + 1
    assert offset == len(data)

    print(f"CURRENT_FILES_SCANNED: {len(current)}")
    print(f"REACHABLE_COMMITS: {len(commits)}")
    print(f"HISTORICAL_PATHS_SCANNED: {len(historical_paths)}")
    print(f"REACHABLE_BLOBS_SCANNED: {len(blobs)}")
    if failures:
        print("PUBLICATION_SECURITY: FAIL — STOP FOR HUMAN REVIEW")
        for category, location in sorted(set(failures)):
            print(f"{category}: {location}")
        return 1
    print("CURRENT_TREE_SCAN: PASS")
    print("HISTORY_BLOB_SCAN: PASS")
    print("PUBLICATION_SECURITY: PASS")
    return 0


if __name__ == "__main__":
    try:
        code = main()
    except (OSError, ValueError, AssertionError, subprocess.CalledProcessError):
        print("PUBLICATION_SECURITY: FAIL — scan incomplete", file=sys.stderr)
        code = 1
    raise SystemExit(code)
