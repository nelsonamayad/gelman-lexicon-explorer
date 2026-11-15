"""Run the R and Python versions of every simulation (and the webR labs) and fail on errors.

    python scripts/check_code.py              # all scripts and R labs
    python scripts/check_code.py kangaroo     # one entry

Each entry's "Show simulation code" block has R and Python tabs, built from
sims/r/<slug>.R and sims/python/<slug>.py. The interactive labs in r/<slug>.qmd
also contain runnable `{webr}` cells (including `#| setup: true` and
`#| solution: true` exercise blocks). This runs every Python script (needs
numpy and matplotlib) and, if Rscript is on the PATH, every R script and every
webR lab (base R only), with plotting sent to a file-less backend. A script
passes if it finishes without an error within the time limit.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 120
WEBR_CELL = re.compile(r"```\{webr\}\n(.*?)```", re.S)


def run(cmd, env=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT, env=env)
        return p.returncode == 0, (p.stderr or p.stdout)[-600:]
    except subprocess.TimeoutExpired:
        return False, f"timed out after {TIMEOUT} s"


def extract_webr_script(text):
    """Concatenate runnable webr cells (autorun cells, setup cells, and solution cells)."""
    chunks = []
    for cell in WEBR_CELL.findall(text):
        opts = [l for l in cell.splitlines() if l.startswith("#|")]
        body = "\n".join(l for l in cell.splitlines() if not l.startswith("#|"))
        # Skip unfilled exercise templates (they have `#| exercise:` without `setup` or `solution`);
        # the matching `#| solution: true` block tests the completed exercise.
        has_exercise = any(l.startswith("#| exercise:") for l in opts)
        is_setup_or_sol = any(re.match(r"^#\|\s*(setup|solution):\s*true", l) for l in opts)
        if has_exercise and not is_setup_or_sol:
            continue
        chunks.append(body)
    return "\n\n".join(chunks)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    only = set(sys.argv[1:])
    env = dict(os.environ, MPLBACKEND="Agg", PYTHONIOENCODING="utf-8")
    rscript = shutil.which("Rscript")
    failed, ran = [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, "sims", "python", "*.py"))):
        slug = os.path.basename(path)[:-3]
        if only and slug not in only:
            continue
        ok, msg = run([sys.executable, path], env)
        ran += 1
        if not ok:
            failed.append(f"python/{slug}: {msg.strip()}")
    if rscript:
        for path in sorted(glob.glob(os.path.join(ROOT, "sims", "r", "*.R"))):
            slug = os.path.basename(path)[:-2]
            if only and slug not in only:
                continue
            code = f'pdf(NULL); source("{path.replace(os.sep, "/")}", echo = FALSE)'
            ok, msg = run([rscript, "-e", code])
            ran += 1
            if not ok:
                failed.append(f"r/{slug}: {msg.strip()}")
        for path in sorted(glob.glob(os.path.join(ROOT, "r", "*.qmd"))):
            slug = os.path.basename(path)[:-4]
            if slug == "index" or (only and slug not in only):
                continue
            script = extract_webr_script(open(path, encoding="utf-8").read())
            if not script.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".R", encoding="utf-8", delete=False) as tmp:
                tmp.write(script)
                tmp_path = tmp.name
            try:
                code = f'pdf(NULL); source("{tmp_path.replace(os.sep, "/")}", echo = FALSE)'
                ok, msg = run([rscript, "-e", code])
            finally:
                os.remove(tmp_path)
            ran += 1
            if not ok:
                failed.append(f"r-lab/{slug}: {msg.strip()}")
    else:
        print("Rscript not found: R scripts not run")
    for f in failed:
        print("FAIL", f)
    print(f"{ran} scripts run, {len(failed)} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
