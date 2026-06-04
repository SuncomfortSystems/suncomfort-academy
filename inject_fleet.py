import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Content"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-fleet-c1': r"Academy - L3 Fleet Management C1 - The fleet dashboard.md",
    'reed-script-l3-fleet-c2': r"Academy - L3 Fleet Management C2 - Set up geo-fences and out-of-hours alerts.md",
    'reed-script-l3-fleet-c3': r"Academy - L3 Fleet Management C3 - Trip analytics and the safe driver leaderboard.md",
    'reed-script-l3-fleet-c4': r"Academy - L3 Fleet Management C4 - Vehicle maintenance tracking and reminders.md",
    'reed-script-l3-fleet-challenge': r"Academy - L3 Fleet Management Challenge - Fleet monitored and maintained.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-contracts-challenge"\] = `.*?`;\n)',
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
print(f"Injected {len(files)} Fleet Management scripts. Total content: {total} chars.")
