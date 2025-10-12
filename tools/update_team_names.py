'run: py.\tools\update_team_names.py'

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
NAMES_FILE = ROOT / 'tools' / 'team-names.txt'
TEAM_HTML = ROOT / 'team.html'

EXCLUDE_FIRST = {'nayan', 'lena'}


def read_names():
    if not NAMES_FILE.exists():
        print(f"Names file not found: {NAMES_FILE}")
        sys.exit(1)
    raw = NAMES_FILE.read_text(encoding='utf-8')
    lines = [l.strip() for l in raw.splitlines() if l.strip() and not l.strip().startswith('#')]
    return lines


def parse_last_first(line):
    parts = [p.strip() for p in line.split(',')]
    if len(parts) < 2:
        return None
    last = parts[0]
    first = ','.join(parts[1:]).strip()
    return first, last


def process_names(lines):
    parsed = []
    for line in lines:
        p = parse_last_first(line)
        if not p:
            continue
        first, last = p
        if first.lower() in EXCLUDE_FIRST:
            continue
        parsed.append((first, last))
    # sort by first name case-insensitively
    parsed.sort(key=lambda t: t[0].lower())
    return [f"{first} {last}" for first, last in parsed]


def update_team_html(new_names):
    if not TEAM_HTML.exists():
        print(f"team.html not found at: {TEAM_HTML}")
        sys.exit(1)
    html = TEAM_HTML.read_text(encoding='utf-8')
    import re
    h4_regex = re.compile(r"<h4>.*?</h4>", re.IGNORECASE | re.DOTALL)
    matches = list(h4_regex.finditer(html))
    if not matches:
        print("No <h4> tags found in team.html")
        sys.exit(1)
    replace_count = min(len(new_names), len(matches))
    # Build new html by replacing only the first replace_count matches
    result = []
    last_index = 0
    for i, m in enumerate(matches):
        start, end = m.span()
        result.append(html[last_index:start])
        if i < replace_count:
            name = new_names[i]
            result.append(f"<h4>{name}</h4>")
        else:
            # keep original h4
            result.append(m.group(0))
        last_index = end
    result.append(html[last_index:])
    new_html = ''.join(result)
    TEAM_HTML.write_text(new_html, encoding='utf-8')
    print(f"Replaced {replace_count} <h4> entries in team.html")


def main():
    lines = read_names()
    if not lines:
        print("No names found in tools/team-names.txt - paste Last, First lines into it and try again.")
        sys.exit(1)
    new_names = process_names(lines)
    if not new_names:
        print("No names remain after applying exclusions (Nayan, Lena). Nothing to write.")
        sys.exit(1)
    update_team_html(new_names)


if __name__ == '__main__':
    main()
