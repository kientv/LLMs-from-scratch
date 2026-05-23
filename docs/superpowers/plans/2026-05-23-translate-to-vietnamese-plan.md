# Vietnamese Translation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Dịch các file Markdown của repository sang tiếng Việt theo spec, giữ nguyên code và thuật ngữ tiếng Anh.

**Architecture:** Linear batch workflow on a dedicated branch `translate-vi`. Work proceeds per-file; each batch (20 files) is committed as one unit. Each file's translation is a textual substitution only—code fences and inline `code` preserved.

**Tech Stack:** git, Python 3 (for validation scripts), `nbformat` for notebook handling, standard shell tools.

---

### Task 1: Create branch and commit spec

**Files:**
- Create: none (branch only)

- [ ] **Step 1.1:** Create branch and commit the spec file created earlier

Run:

```bash
git checkout -b translate-vi
git add docs/superpowers/specs/2026-05-23-translate-to-vietnamese-design.md
git commit -m "docs(spec): add Vietnamese translation design"
```

Expected: branch `translate-vi` is created and spec file committed.

---

### Task 2: Translate sample file `ch01/README.md`

**Files:**
- Modify: `ch01/README.md`

- [ ] **Step 2.1:** Replace the English textual content with Vietnamese translation (preserve links and any inline code). Write the final file content exactly as below.

Replace `ch01/README.md` with the following content:

```markdown
# Chương 1: Hiểu về Large Language Models

&nbsp;
## Mã nguồn chính của chương

Chương này không có mã nguồn.

&nbsp;
## Tài liệu bổ sung

[Lời khuyên để tận dụng tối đa cuốn sách này](https://sebastianraschka.com/blog/2025/reading-books.html)

Trong video bên dưới, tôi chia sẻ cách cá nhân trong việc thiết lập môi trường Python trên máy tính của mình:

<br>
<br>

[![Link to the video](https://img.youtube.com/vi/yAcWnfsZhzo/0.jpg)](https://www.youtube.com/watch?v=yAcWnfsZhzo)

<br>
<br>

Như một phần bổ sung tùy chọn, video hướng dẫn sau cung cấp tổng quan về vòng đời phát triển LLM được đề cập trong cuốn sách này:

<br>
<br>

[![Link to the video](https://img.youtube.com/vi/kPGTx4wcm_w/0.jpg)](https://www.youtube.com/watch?v=kPGTx4wcm_w)

```

Notes: this replacement preserves link URLs and image URLs as-is. No code fences exist in this file.

---

### Task 3: Automated verification that code blocks and inline code were preserved (and notebook code cells preserved)

**Files:**
- Create: `scripts/verify_markdown_preserve_codeblocks.py`
- Create: `scripts/verify_notebook_preserve_codecells.py`

- [ ] **Step 3.1:** Add a small Python script that compares code fences between original and translated Markdown files and errors if any fence content or fence counts changed. (see script below)

Script content (create `scripts/verify_markdown_preserve_codeblocks.py`):

```python
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
```

- [ ] **Step 3.2:** Add a small Python script that verifies code cells in notebooks are unchanged between original and translated versions. Use `nbformat` to parse notebooks and compare code cell sources.

Script content (create `scripts/verify_notebook_preserve_codecells.py`):

```python
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
```

- [ ] **Step 3.3:** Run the scripts to verify `ch01/README.md` translation and (if applicable) any translated notebook sample.

```bash
python3 scripts/verify_markdown_preserve_codeblocks.py ch01/README.md ch01/README.md
python3 scripts/verify_notebook_preserve_codecells.py some_notebook.ipynb some_notebook.ipynb
```

Expected: `OK` for both checks. The scripts exit non-zero if they detect mismatches.

---

### Task 4: Commit sample translation and push

**Files:**
- Modify: `ch01/README.md`
- Create: `scripts/verify_markdown_preserve_codeblocks.py`

- [ ] **Step 4.1:** Stage and commit

```bash
git add ch01/README.md scripts/verify_markdown_preserve_codeblocks.py
git commit -m "docs(vi): translate ch01/README.md (sample)"
```

- [ ] **Step 4.2:** Push branch

```bash
git push -u origin translate-vi
```

Expected: branch pushed with the sample translation commit.

---

### Task 5: Batch translation workflow

**Files:**
- Modify: multiple `*.md` files in repo (per spec)

- [ ] **Step 5.1:** Prepare file list (example: use `git ls-files '*.md'` to enumerate)

Run:

```bash
git ls-files '*.md' > /tmp/md_files_all.txt
```

- [ ] **Step 5.2:** Split into batches of 20 and translate each batch. For each batch:

- Translate files (assistant will edit files directly in this workspace), then run verification script for each file, commit batch with message `docs(vi): translate <n> files` and push.

Example commands:

```bash
# after editing files
git add file1.md file2.md ... file20.md
git commit -m "docs(vi): translate 20 files"
git push
```

---

### Task 6: Final review and PR

- [ ] **Step 6.1:** Open a Pull Request on GitHub from `translate-vi` into `main` with description: "Translate documentation to Vietnamese. Code and technical terms preserved in English."

- [ ] **Step 6.2:** Address review feedback, apply fixes, and merge when approved.

---

### Self-review checklist (run before claiming done)

- [ ] Run `scripts/verify_markdown_preserve_codeblocks.py` for all modified files
- [ ] Run `git diff --name-only origin/main...translate-vi` to list changed files
- [ ] Confirm no `.py`, `.js`, `.ipynb` files were modified unintentionally

---

Plan saved to: `docs/superpowers/plans/2026-05-23-translate-to-vietnamese-plan.md`

Execution options:
1. **Subagent-Driven (recommended)** — dispatch a subagent per task with reviews.
2. **Inline Execution** — I execute tasks here in this session, batching work and reporting progress.

Which approach do you prefer? Reply with `1` or `2`.
