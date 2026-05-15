import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Owners Inbox\Scripts"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-contracts-c1': r"Academy - L3 Contracts and PPM C1 - Set up a contract template.md",
    'reed-script-l3-contracts-c2': r"Academy - L3 Contracts and PPM C2 - Link a contract to a customer.md",
    'reed-script-l3-contracts-c3': r"Academy - L3 Contracts and PPM C3 - Configure PPM auto-job creation.md",
    'reed-script-l3-contracts-c4': r"Academy - L3 Contracts and PPM C4 - Set up SLA templates.md",
    'reed-script-l3-contracts-c5': r"Academy - L3 Contracts and PPM C5 - Read the contracts and SLA reports.md",
    'reed-script-l3-contracts-challenge': r"Academy - L3 Contracts and PPM Challenge - Contract running, PPM scheduled.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

# Find the insertion point — after the last l3-sales-plus entry
insert_after = "INBOX_FILES[\"reed-script-l3-sales-plus-challenge\"]"
pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-sales-plus-challenge"\] = `.*?`;\n)',
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
print(f"Injected {len(files)} Contracts and PPM scripts. Total content: {total} chars.")
