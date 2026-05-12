#!/usr/bin/env python3
"""Git push script - Initialize repo and push to GitHub"""
import subprocess
import os
import sys

REPO_PATH = r"d:\Trae CN\github\nwacs\nwacs"
REMOTE_URL = "https://github.com/dddyang1477/NWACS.git"
LOG_FILE = os.path.join(REPO_PATH, "_git_push_log.txt")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def run(cmd, cwd=REPO_PATH):
    log(f"RUN: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.stdout:
        log(f"STDOUT: {result.stdout.strip()}")
    if result.stderr:
        log(f"STDERR: {result.stderr.strip()}")
    if result.returncode != 0:
        log(f"FAILED (code {result.returncode})")
    else:
        log("OK")
    return result

def main():
    log("=" * 60)
    log("Starting Git push to GitHub")
    log("=" * 60)

    # Step 1: git init
    log("\n--- Step 1: git init ---")
    run("git init")

    # Step 2: git add -A
    log("\n--- Step 2: git add -A ---")
    run("git add -A")

    # Step 3: git commit
    log("\n--- Step 3: git commit ---")
    run('git commit -m "NWACS v8 - Full project upload"')

    # Step 4: git remote add
    log("\n--- Step 4: git remote add ---")
    run(f"git remote add origin {REMOTE_URL}")

    # Step 5: git push --force
    log("\n--- Step 5: git push --force ---")
    run("git push -u origin master --force")

    log("\n" + "=" * 60)
    log("DONE")
    log("=" * 60)

if __name__ == "__main__":
    main()