import os

scripts_dir = r"C:\Users\sarab\Desktop\Commusoft\Owners Inbox\Scripts"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

files = [
    ("reed-script-l3-sales-plus-c1", "Academy - L3 Sales+ C1 - The opportunities dashboard.md"),
    ("reed-script-l3-sales-plus-c2", "Academy - L3 Sales+ C2 - Add and manage an opportunity.md"),
    ("reed-script-l3-sales-plus-c3", "Academy - L3 Sales+ C3 - Complete a survey on the app.md"),
    ("reed-script-l3-sales-plus-c4", "Academy - L3 Sales+ C4 - Build a full proposal with the template builder.md"),
    ("reed-script-l3-sales-plus-c5", "Academy - L3 Sales+ C5 - Present finance options to a customer.md"),
    ("reed-script-l3-sales-plus-c6", "Academy - L3 Sales+ C6 - Track a proposal through to acceptance.md"),
    ("reed-script-l3-sales-plus-c7", "Academy - L3 Sales+ C7 - Use the media portal for site data.md"),
    ("reed-script-l3-sales-plus-challenge", "Academy - L3 Sales+ Challenge - Lead to accepted proposal.md"),
]

marker = 'INBOX_FILES["reed-script-l1-ft-series1"]'

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

injection_parts = []
for key, fname in files:
    fpath = os.path.join(scripts_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    content = content.replace("`", "\\`")
    injection_parts.append(f'INBOX_FILES["{key}"] = `{content}`;\n')

injection_block = "\n".join(injection_parts)
new_html = html.replace(marker, injection_block + "\n" + marker, 1)

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print("Done. Injected", len(files), "INBOX_FILES entries.")
