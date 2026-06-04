import re

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Content"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = {
    'reed-script-l3-route-c1': r"Academy - L3 Route Optimisation C1 - How route optimisation works.md",
    'reed-script-l3-route-c2': r"Academy - L3 Route Optimisation C2 - Configure route optimisation settings.md",
    'reed-script-l3-route-c3': r"Academy - L3 Route Optimisation C3 - Use route optimisation in the diary.md",
    'reed-script-l3-route-challenge': r"Academy - L3 Route Optimisation Challenge - Route optimised, diary running efficiently.md",
}

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

pattern = re.compile(
    r'(INBOX_FILES\["reed-script-l3-fleet-challenge"\] = `.*?`;\n)',
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
print(f"Injected {len(files)} Route Optimisation scripts. Total content: {total} chars.")
