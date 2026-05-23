#!/usr/bin/env python3
import sys
import nbformat

def main(orig_nb, trans_nb):
    o = nbformat.read(orig_nb, as_version=4)
    t = nbformat.read(trans_nb, as_version=4)
    o_code = [cell.source for cell in o.cells if cell.cell_type == 'code']
    t_code = [cell.source for cell in t.cells if cell.cell_type == 'code']
    if len(o_code) != len(t_code):
        print('CODE_CELL_COUNT_MISMATCH', len(o_code), len(t_code))
        sys.exit(2)
    for i,(a,b) in enumerate(zip(o_code,t_code)):
        if a != b:
            print(f'CODE_CELL_MISMATCH at code cell {i}')
            sys.exit(3)
    print('OK')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: verify_notebook_preserve_codecells.py orig.ipynb trans.ipynb')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
