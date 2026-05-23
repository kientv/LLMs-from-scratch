#!/usr/bin/env python3
import sys
from pathlib import Path

def extract_fences(text):
    fences = []
    in_fence = False
    cur = []
    for line in text.splitlines():
        if line.strip().startswith('```'):
            if in_fence:
                fences.append('\n'.join(cur))
                cur = []
                in_fence = False
            else:
                in_fence = True
        elif in_fence:
            cur.append(line)
    return fences

def main(orig_path, trans_path):
    o = Path(orig_path).read_text(encoding='utf-8')
    t = Path(trans_path).read_text(encoding='utf-8')
    of = extract_fences(o)
    tf = extract_fences(t)
    if len(of) != len(tf):
        print('FENCE_COUNT_MISMATCH', len(of), len(tf))
        sys.exit(2)
    for i,(a,b) in enumerate(zip(of,tf)):
        if a != b:
            print(f'FENCE_MISMATCH at fence {i}')
            sys.exit(3)
    print('OK')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: verify_markdown_preserve_codeblocks.py orig.md trans.md')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
