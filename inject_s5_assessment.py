"""Convert the Series 5 challenge into a series assessment on the Academy dashboard.

The challenge already held the right material in the wrong form: Archer narrated
Claire making four decisions while the learner watched the answers appear. This
replaces all three surfaces so the dashboard shows a scored assessment instead:

  1. INBOX_FILES  - the full markdown, from Content/
  2. COURSES      - the walkthrough panel Sara and Nadia read and annotate
  3. the card     - label "Challenge" -> "Series assessment"

Backs the dashboard up first. Aborts rather than writes if the COURSES,
INBOX_FILES or card counts change.
"""

import re
import shutil
from pathlib import Path

KEY = "reed-script-l1-s5-challenge"
ROOT = Path(r"C:\Users\sarab\Desktop\Commusoft")
DASH = ROOT / "github" / "suncomfort-academy" / "dashboard.html"
SRC = ROOT / "Content" / "Reed - Script - L1 Office Staff Series 5 Challenge Invoice raised paid and synced.md"
BACKUP = DASH.with_name("dashboard.backup-preinject-s5-assessment.html")


def counts(t):
    return (
        len(re.findall(r'<div class="walkthrough-num">', t)),
        len(set(re.findall(r'INBOX_FILES\["([^"]+)"\]', t))
            | set(re.findall(r"INBOX_FILES\['([^']+)'\]", t))),
        len(set(re.findall(r"COURSES\['([^']+)'\]", t))
            | set(re.findall(r'COURSES\["([^"]+)"\]', t))),
    )


def js(s):
    """Escape a Python string for a double-quoted JS string literal."""
    return (s.replace("\\", "\\\\").replace('"', '\\"')
             .replace("\n", " ").replace("\r", " ").strip())


QUESTIONS = [
    ("Invoice type at the start of a staged job",
     "A large commercial client is billed in two parts, thirty percent upfront and the rest at completion. Claire is about to raise the first invoice. Which type should she select?",
     ["Final", "Interim", "Consolidated", "Deposit request"], "Interim",
     "Interim is the type for billing in stages while the work is still running, with the Final invoice following at completion. The type sets the structure for the whole billing sequence, so it matters at the first step.",
     "Raising a Final invoice now would close the billing on a job that is not finished. Interim is the type for staged billing, with Final following at completion."),
    ("One payment across several invoices",
     "A property management company has sent a single bank transfer covering four separate invoices across different jobs. What should Claire do?",
     ["Record a payment against each of the four invoices individually",
      "Use Cash Allocations from the customer record to assign the payment across all four",
      "Raise a consolidated invoice, then record one payment against it",
      "Record the full amount against the oldest invoice and credit the difference"],
     "Use Cash Allocations from the customer record to assign the payment across all four",
     "Cash Allocations is reached from the customer record rather than from an individual invoice, and assigns one payment across several invoices at once.",
     "Recording it four times would create four separate payment entries against one bank transaction, which makes reconciliation harder rather than easier. Cash Allocations handles it in one step, from the customer record."),
    ("Correcting an issued invoice",
     "A customer has reviewed their final invoice and says they were charged for a part that was not used. The invoice has already been issued. What should Claire do?",
     ["Edit the invoice and remove the line",
      "Delete the invoice and raise it again",
      "Raise a credit note from Quick Links and adjust it to the line being corrected",
      "Leave the invoice and apply a discount to the next one"],
     "Raise a credit note from Quick Links and adjust it to the line being corrected",
     "The original invoice stays on the record and the credit note documents the correction. Both are visible in the customer history and both sync to the accounting package correctly.",
     "Editing or deleting an issued invoice breaks the audit trail and will not sync cleanly. A credit note corrects the charge while leaving the original record intact."),
    ("A customer chasing an overdue balance",
     "A commercial customer has three unpaid invoices across two months and calls asking what they owe in total. What is the quickest way for Claire to give them a single view?",
     ["Export the three invoices to PDF and send them together",
      "Send a customer statement from the customer record",
      "Raise a consolidated invoice covering the three",
      "Send the oldest invoice and explain the rest by email"],
     "Send a customer statement from the customer record",
     "A statement gives the customer a single view of their outstanding account - unpaid invoices, unallocated credit notes, and the net balance owed - without changing any of the underlying invoices.",
     "A consolidated invoice creates a new invoice, which is not what is needed here - the three already exist. A statement summarises what is outstanding without altering the record."),
    ("After the correction, before reconciliation",
     "Claire checks the Accounting Integration Dashboard. The credit note is in the Waiting to Be Sent queue and automatic sync is enabled. What does she need to do?",
     ["Nothing - the queue clears itself and no check is needed",
      "Re-raise the credit note, because Waiting to Be Sent means it failed",
      "Nothing urgent - it will push within two hours, or use Send Data Now if it is needed in Xero immediately",
      "Switch off automatic sync and send the whole batch manually"],
     "Nothing urgent - it will push within two hours, or use Send Data Now if it is needed in Xero immediately",
     "Waiting to Be Sent is the normal queued state, not an error. Checking the dashboard confirms the record is queued rather than sitting in an error state.",
     "Waiting to Be Sent is the normal queued state. With automatic sync on it pushes within two hours, and Send Data Now pushes it immediately if it is needed sooner."),
    ("The consolidated invoice warning",
     "Claire is raising a consolidated invoice for a client and selects Final as the invoice type for one of the included jobs. A warning appears. What is Commusoft telling her?",
     ["The consolidated invoice cannot be saved until all jobs use the same invoice type",
      "The customer has reached their credit limit and the invoice cannot be issued",
      "Future diary events for that job will be cancelled if she proceeds with Final",
      "The job has an outstanding credit note that must be resolved before invoicing"],
     "Future diary events for that job will be cancelled if she proceeds with Final",
     "Selecting Final within a consolidated invoice triggers a warning that future diary events for that job will be cancelled. Claire should confirm the job is genuinely complete before proceeding.",
     "Final as an invoice type signals that the job is done, and any future diary events for it will be cancelled as a result. Claire should check whether any planned visits are still outstanding before confirming."),
]

INTRO = ("You have worked through six walkthroughs on getting paid - raising an invoice, recording a "
         "payment, correcting a charge, sending a statement, syncing to your accounting package, and "
         "consolidating several jobs onto one invoice. Each of those covered one workflow on its own. "
         "This is where you choose between them. Six questions, drawn from one end-of-month scenario at "
         "SunComfort. Answer them in order - the billing cycle is a sequence, and each decision follows "
         "from the one before. You need five correct to pass, and you can retake it as many times as you "
         "like. Your certificate arrives by email.")

CLOSE = ("An Interim invoice to open the billing, a Cash Allocation to match a single payment to four "
         "invoices, a credit note to correct a charge without touching the original, a statement to show "
         "what is outstanding, and a dashboard check to confirm the sync is queued. The billing cycle in "
         "Commusoft is a sequence, and getting each step right means the financial record looks after "
         "itself. Series 5 is complete.")


def build_courses_entry():
    scenes = [f'{{type:"section", heading:"What this is", body:"{js(INTRO)}"}}']
    for i, (head, q, opts, correct, fb, fba) in enumerate(QUESTIONS, 1):
        o = ", ".join(f'"{js(x)}"' for x in opts)
        scenes.append(
            f'{{type:"reflection", label:"Question {i}", '
            f'question:"{js(head)} - {js(q)}", options:[{o}], correct:"{js(correct)}", '
            f'feedback:"{js(fb)}", feedbackAlt:"{js(fba)}"}}'
        )
    scenes.append(f'{{type:"section", heading:"Series close", body:"{js(CLOSE)}"}}')
    body = ",\n    ".join(scenes)
    return f"""COURSES['{KEY}'] = {{
  contentType: "Series assessment",
  pathLabel: "L2 Office teams \u2014 Series 5: Getting paid \u2014 Series assessment",
  title: "Invoice raised, paid, and synced",
  duration: "6 questions",
  persona: "Office teams",
  characters: "Claire Hudson (Administrator / Financial office staff, referenced in scenario)",
  scenario: "SunComfort is closing out the month. Claire is working through the invoicing queue and six decisions have landed \u2014 a commercial client billed in stages, a payment covering four accounts, a customer disputing a charge, a customer asking what they owe, and the reconciliation that follows.",
  objectives: [
    "Select the correct invoice type for a given billing scenario",
    "Identify the right tool when a payment covers multiple invoices",
    "Apply the credit note process when an invoice correction is needed",
    "Choose between a statement and an invoice when a customer asks what they owe",
    "Read the Accounting Integration Dashboard correctly before reconciling"
  ],
  productionSetup: [
    "*Delivered as a Google Form in quiz mode, with Certify'em for the certificate.",
    "*Pass mark 5 of 6. Unlimited retakes. Email collected for the certificate.",
    "*Archer narrates the opening and close only. The questions are answered in the form, not on screen.*"
  ],
  buildBySection: [
    {{section:"What this is", media:"Written text", note:"Article copy introducing the assessment and the pass mark, with the link out to the form."}},
    {{section:"Questions 1 to 6", media:"Expanding section", note:"Delivered in the Google Form, not in the article. Listed so the build sheet covers the whole assessment. A 'Google Form' value may need adding to the approved list \u2014 flagged for Sara."}},
    {{section:"Series close", media:"Written text", note:"Used as the form's confirmation message."}}
  ],
  productionNotes: [
    "No product recording needed. This is the one item in the series with no screens to capture.",
    "The six questions come straight from the four decisions the challenge used to narrate, plus the consolidated-invoice knowledge check, plus one new question covering Walkthrough 4 (customer statements), which no assessment covered before."
  ],
  scenes: [
    {body}
  ]
}};"""


def main():
    text = DASH.read_text(encoding="utf-8")
    before = counts(text)
    shutil.copy2(DASH, BACKUP)
    print(f"Backed up to {BACKUP.name}")

    # 1. INBOX_FILES - full markdown from Content/
    md = SRC.read_text(encoding="utf-8")
    escaped = md.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    pat = re.compile(r'INBOX_FILES\["' + re.escape(KEY) + r'"\] = `.*?`;', re.DOTALL)
    text, n = pat.subn(lambda m: f'INBOX_FILES["{KEY}"] = `{escaped}`;', text, count=1)
    if n != 1:
        raise SystemExit(f"ABORT: expected 1 INBOX_FILES match, got {n}")
    print(f"INBOX_FILES replaced ({len(md)} chars)")

    # 2. COURSES - the panel
    start = text.find(f"COURSES['{KEY}']")
    if start < 0:
        raise SystemExit("ABORT: COURSES entry not found")
    nxt = text.find("COURSES['", start + 10)
    end = text.rfind("};", start, nxt) + 2
    if end <= start:
        raise SystemExit("ABORT: could not find the end of the COURSES entry")
    text = text[:start] + build_courses_entry() + text[end:]
    print(f"COURSES replaced ({len(QUESTIONS)} questions, 2 sections)")

    # 3. the card label
    card = re.compile(r"(openPanel\('" + re.escape(KEY) + r"'\)\"><div class=\"walkthrough-num\">)([^<]*)(</div>)")
    text, n = card.subn(lambda m: m.group(1) + "Series assessment" + m.group(3), text, count=1)
    if n != 1:
        raise SystemExit(f"ABORT: expected 1 card match, got {n}")
    print("Card label -> 'Series assessment'")

    after = counts(text)
    print(f"\ncards {before[0]} -> {after[0]}   inbox {before[1]} -> {after[1]}   courses {before[2]} -> {after[2]}")
    if before != after:
        raise SystemExit("ABORT: a count changed, nothing written")

    DASH.write_text(text, encoding="utf-8")
    print("WRITTEN")


if __name__ == "__main__":
    main()
