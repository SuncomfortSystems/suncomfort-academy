import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Content"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-analytics-c1': r"Academy - L3 Analytics C1 - Your Analytics dashboard.md",
    'reed-script-l3-analytics-c2': r"Academy - L3 Analytics C2 - Build a tabular report.md",
    'reed-script-l3-analytics-c3': r"Academy - L3 Analytics C3 - Build custom widgets to track performance.md",
    'reed-script-l3-analytics-c4': r"Academy - L3 Analytics C4 - The Analytics Marketplace.md",
    'reed-script-l3-analytics-c5': r"Academy - L3 Analytics C5 - Analytics+ what the upgrade unlocks.md",
    'reed-script-l3-analytics-challenge': r"Academy - L3 Analytics Challenge - The numbers behind the decision.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-forms-challenge"\] = `.*?`;\n)',
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
print(f"Injected {len(files)} Analytics scripts. Total content: {total} chars.")
