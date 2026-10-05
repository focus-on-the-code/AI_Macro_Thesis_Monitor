"""Redacted local heuristic scan. Full-history mode requires a non-shallow Git checkout."""
import argparse
from pathlib import Path
import re
import subprocess

PATTERNS = [
    rb'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
    rb'\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{50,})\b',
    rb'\bAKIA[A-Z0-9]{16}\b',
    rb'\bsk-[A-Za-z0-9_-]{20,}\b',
    rb'(?i)(?:api[_-]?key|access[_-]?token|password|secret)\s*[=:]\s*[\x22\x27]?[A-Za-z0-9+/=_-]{16,}',
]


def git(*args):
    return subprocess.check_output(['git', *args], stderr=subprocess.PIPE)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--history', action='store_true')
    args = parser.parse_args()
    objects = []
    if args.history:
        if git('rev-parse', '--is-shallow-repository').strip() != b'false':
            raise SystemExit('BLOCKED: shallow repository; fetch complete history first')
        for item in git('rev-list', '--objects', '--all').splitlines():
            sha = item.split(b' ', 1)[0].decode()
            if git('cat-file', '-t', sha).strip() == b'blob':
                objects.append((sha, git('cat-file', 'blob', sha)))
    else:
        for path in Path('.').rglob('*'):
            if any(p in {'.git', '.venv', '__pycache__', '.ruff_cache'} for p in path.parts):
                continue
            if path.is_file():
                objects.append((str(path), path.read_bytes()))
    findings = [label for label, data in objects if any(re.search(p, data) for p in PATTERNS)]
    print(f'Scanned {len(objects)} blobs/files; mode={"history" if args.history else "working-tree"}; findings={len(findings)}')
    for label in findings:
        print(f'REVIEW REQUIRED: {label} (matched content redacted)')
    if findings:
        raise SystemExit(1)
    print('PASS within heuristic coverage; this cannot prove absence of every secret format.')


if __name__ == '__main__':
    main()
