import re

draft_path = r"C:\Users\sarab\Desktop\Commusoft\Owners Inbox\Business Cases\Cedar - v6 Enablement Stack Modernisation - DRAFT.md"
dashboard_path = r"C:\Users\sarab\Desktop\Commusoft\github\suncomfort-academy\dashboard.html"

with open(draft_path, "r", encoding="utf-8") as f:
    draft_content = f.read()

escaped = draft_content.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")

with open(dashboard_path, "r", encoding="utf-8") as f:
    html = f.read()

new_entry = f'INBOX_FILES["cedar-stack-modernisation"] = `{escaped}`;\n'

pattern = re.compile(
    r'INBOX_FILES\["cedar-stack-modernisation"\] = `.*?`;\n',
    re.DOTALL,
)

new_html, n = pattern.subn(new_entry, html, count=1)
if n != 1:
    raise SystemExit(f"Expected 1 replacement, got {n}")

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(new_html)

print(f"Updated business case entry. Draft is {len(draft_content)} chars; escaped is {len(escaped)} chars.")
