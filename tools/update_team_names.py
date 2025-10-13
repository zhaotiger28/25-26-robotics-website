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
    # takes in last, first
    # or last,frist, grade
    parts = [p.strip() for p in line.split(',')]
    if len(parts) < 2:
        return None
    last = parts[0]
    # the rest after the first comma is treated as the first name
    first = parts[1]
    grade = None
    if len(parts) >= 3:
        grade = parts[2]
    return first, last, grade


def process_names(lines):
    parsed = []
    for line in lines:
        p = parse_last_first(line)
        if not p:
            continue
        first, last, grade = p
        if first.lower() in EXCLUDE_FIRST:
            continue
        parsed.append((first, last, grade))
    # sort by first name case-insensitively
    parsed.sort(key=lambda t: t[0].lower())
    # format grades when present
    def fmt_name(entry):
        first, last, grade = entry
        base = f"{first} {last}"
        grade_text = None
        if grade:
            import re
            m = re.search(r"(\d{1,2})", grade)
            if m:
                num = int(m.group(1))
                def ordinal(n):
                    if 10 <= (n % 100) <= 20:
                        suffix = 'th'
                    else:
                        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
                    return f"{n}{suffix}"
                grade_text = ordinal(num)
            else:
                grade_text = grade

        # Return HTML for the <h4> content: name in a .name span and optional .grade span
        if grade_text:
            # include a leading space before grade span for separation
            return f"<span class=\"name\">{base}</span> <span class=\"grade\">{grade_text}</span>"
        else:
            return f"<span class=\"name\">{base}</span>"

    return [fmt_name(e) for e in parsed]


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
