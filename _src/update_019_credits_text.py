"""Update 019: fix the Photo credits intro text.

- Step-by-step photos come from Pexels (confirmed by the site owner), so
  "Step-by-step photos and pins are made by us." is no longer accurate.
- The About page photo (Salva Amin Azad on Pexels) is credited on the About
  page itself but was missing from the Photo credits page. It is mentioned
  in the same intro paragraph.

Idempotent: does nothing if already applied. Fails loudly if the old
sentence cannot be found in any known source file.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OLD = "Step-by-step photos and pins are made by us."
MARKER = "Step-by-step photos also come from Pexels"
ABOUT_URL = "https://www.pexels.com/photo/fresh-tomatoes-and-herbs-on-a-kitchen-table-37314037/"

CANDIDATES = ["build.py", "guides_legal.json", "storefront.py"]


def new_text(q):
    # q = quote character used for HTML attributes in the surrounding source
    return (
        "Step-by-step photos also come from Pexels. The photo on our About page is by "
        "Salva Amin Azad (<a href=" + q + ABOUT_URL + q + ">view on Pexels</a>). "
        "Pinterest pins and share images are designed by us using these photos."
    )


def main():
    for name in CANDIDATES:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        src = open(path, encoding="utf-8").read()
        if MARKER in src:
            print("Already applied. Nothing to do.")
            return
        if OLD not in src:
            continue
        # Copy the attribute quote style used on the same line (the existing Pexels link).
        idx = src.index(OLD)
        line_start = src.rfind("\n", 0, idx) + 1
        line_end = src.find("\n", idx)
        line = src[line_start:line_end if line_end != -1 else len(src)]
        q = "'"
        h = line.find("href=")
        if h != -1 and line[h + 5] in "\"'":
            q = line[h + 5]
        elif h != -1 and line[h + 5:h + 7] == '\\"':
            q = '\\"'
        if name.endswith(".json"):
            q = '\\"' if q == '"' else q
        src = src.replace(OLD, new_text(q), 1)
        open(path, "w", encoding="utf-8").write(src)
        print("OK (" + name + "): credits intro updated, quote style " + repr(q))
        return
    print("ERROR: sentence not found in " + ", ".join(CANDIDATES), file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
