import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Owners Inbox\Scripts"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-forms-c1': r"Academy - L3 Custom Forms C1 - Build your first custom form.md",
    'reed-script-l3-forms-c2': r"Academy - L3 Custom Forms C2 - Assign forms and control when they appear.md",
    'reed-script-l3-forms-c3': r"Academy - L3 Custom Forms C3 - Complete forms on mobile and review in the office.md",
    'reed-script-l3-forms-challenge': r"Academy - L3 Custom Forms Challenge - Form built, assigned, and signed off.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-stock-challenge"\] = `.*?`;\n)',
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
print(f"Injected {len(files)} Custom Forms scripts. Total content: {total} chars.")
