"""Run the R and Python versions of every simulation and fail on errors.

    python scripts/check_code.py              # all scripts
    python scripts/check_code.py kangaroo     # one entry

Each entry's "Show simulation code" block has R and Python tabs, built from
sims/r/<slug>.R and sims/python/<slug>.py. This runs every Python script
(needs numpy and matplotlib) and, if Rscript is on the PATH, every R script
(base R only), with plotting sent to a file-less backend. A script passes if
it finishes without an error within the time limit.
"""
import glob
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 120


def run(cmd, env=None):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=TIMEOUT, env=env)
        return p.returncode == 0, (p.stderr or p.stdout)[-600:]
    except subprocess.TimeoutExpired:
        return False, f"timed out after {TIMEOUT} s"


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
    else:
        print("Rscript not found: R scripts not run")
    for f in failed:
        print("FAIL", f)
    print(f"{ran} scripts run, {len(failed)} failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
