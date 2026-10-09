"""Automatic photo review for Bored of Toast.

Runs inside the Auto build workflow. For every image in images/ that was
added or changed compared with origin/main, it asks a vision model whether
the photo actually shows the expected dish (taken from the file name), and
whether it contains people, text or watermarks.

It NEVER edits or generates images. It only writes a text report to
_src/photo_review.md (and prints it), so the result can be read without
looking at the pictures.

Needs the repository secret OPENAI_API_KEY. If it is missing, the review is
skipped and the build continues. Optional: PHOTO_REVIEW_MODEL (default
gpt-4o-mini). Uses only the Python standard library.
"""
import base64
import json
import os
import pathlib
import re
import subprocess
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORT = ROOT / "_src" / "photo_review.md"
KEY = os.environ.get("OPENAI_API_KEY", "").strip()
MODEL = os.environ.get("PHOTO_REVIEW_MODEL", "gpt-4o-mini").strip()
EXTS = {".webp", ".jpg", ".jpeg", ".png"}
# Skip derived variants (social cards, pins, responsive sizes).
VARIANT = re.compile(r"(-og|-pin|-\d{2,4}w?|@\dx)$")
MAX_IMAGES = 15


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout


def changed_images():
    try:
        changed = git("diff", "--name-only", "--diff-filter=AM", "origin/main", "--", "images")
        untracked = git("ls-files", "--others", "--exclude-standard", "images")
    except subprocess.CalledProcessError as err:
        print("ERROR: could not compare with origin/main:", (err.stderr or "").strip())
        return []
    files = set()
    for line in (changed + "\n" + untracked).splitlines():
        line = line.strip()
        if not line:
            continue
        path = pathlib.Path(line)
        if path.suffix.lower() in EXTS and not VARIANT.search(path.stem):
            files.add(path)
    return sorted(files)[:MAX_IMAGES]


def expected_dish(path):
    stem = path.stem
    if stem.startswith("step-") or "-step-" in stem:
        return None
    if stem.startswith("guide-"):
        return "food photo for a cooking guide about " + stem[6:].replace("-", " ")
    return stem.replace("-", " ")


def ask(path, expected):
    data = base64.b64encode((ROOT / path).read_bytes()).decode()
    suffix = path.suffix.lower()
    mime = {"webp": "image/webp", "png": "image/png"}.get(suffix[1:], "image/jpeg")
    prompt = (
        f'This photo will illustrate a web page for: "{expected}". '
        'Reply ONLY with JSON: {"verdict": "PASS" or "FAIL", '
        '"shows": "short description of what the photo actually shows", '
        '"reason": "one short sentence"}. '
        "FAIL if the main food clearly differs from the expected dish, "
        "if identifiable people or faces are visible, or if there is visible "
        "text, logos or watermarks. Similar-looking variations of the dish are a PASS."
    )
    body = {
        "model": MODEL,
        "max_tokens": 200,
        "response_format": {"type": "json_object"},
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url",
                 "image_url": {"url": f"data:{mime};base64,{data}", "detail": "low"}},
            ],
        }],
    }
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.load(resp)
    return json.loads(result["choices"][0]["message"]["content"])


def main():
    if not KEY:
        print("Photo review skipped: no OPENAI_API_KEY secret configured.")
        return
    images = changed_images()
    if not images:
        print("Photo review: no new or changed photos.")
        return

    rows, fails = [], 0
    for path in images:
        expected = expected_dish(path)
        if expected is None:
            continue
        try:
            res = ask(path, expected)
            verdict = str(res.get("verdict", "?")).upper()
            shows = str(res.get("shows", "")).replace("|", "/")
            reason = str(res.get("reason", "")).replace("|", "/")
        except (urllib.error.URLError, KeyError, ValueError, json.JSONDecodeError) as err:
            verdict, shows, reason = "ERROR", "", f"review failed: {err}"
        if verdict != "PASS":
            fails += 1
        rows.append(f"| `{path}` | {expected} | {verdict} | {shows} | {reason} |")

    sha = os.environ.get("GITHUB_SHA", "local")[:7]
    report = "\n".join([
        "# Photo review",
        "",
        f"Commit reviewed: `{sha}` · model: `{MODEL}` · photos: {len(rows)} · not passed: {fails}",
        "",
        "| File | Expected | Verdict | What the photo shows | Reason |",
        "|---|---|---|---|---|",
        *rows,
        "",
    ])
    REPORT.write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
