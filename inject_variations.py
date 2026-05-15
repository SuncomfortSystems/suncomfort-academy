import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Owners Inbox\Scripts"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-variations-c1': r"Academy - L3 Variations C1 - Set up variation templates and option templates.md",
    'reed-script-l3-variations-c2': r"Academy - L3 Variations C2 - Raise a variation in the field.md",
    'reed-script-l3-variations-c3': r"Academy - L3 Variations C3 - Manage variations from the office.md",
    'reed-script-l3-variations-challenge': r"Academy - L3 Variations Challenge - Variation raised, approved, and invoiced.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-route-challenge"\] = `.*?`;\n)',
    re.DOTALL,
)

new_entries = ""
for key, filename in files.items():
    path = scripts_dir + "\\" + filename
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    escaped = content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    new_entries += f'INBOX_FILES["{key}"] = `{escaped}`;\n'

def replacer(m):
    return m.group(1) + new_entries

new_html, n = pattern.subn(replacer, html, count=1)
if n != 1:
    raise SystemExit(f"Expected 1 insertion point, got {n}")

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(new_html)

total = sum(len(open(scripts_dir + "\\" + fn, encoding="utf-8").read()) for fn in files.values())
print(f"Injected {len(files)} Variations scripts. Total content: {total} chars.")
