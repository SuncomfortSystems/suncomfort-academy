"""Create the missing series assessment for L2 Office teams Series 2, The job record.

Series 2 is the one approved series and the only one with no challenge to
convert, so its assessment is new rather than adapted. All three surfaces are
created, none replaced:

  1. a card after Walkthrough 10 in the Job Record grid
  2. a COURSES entry - the panel, 2 sections and 6 questions
  3. an INBOX_FILES entry - the full markdown from Content/

None of the six questions repeats a walkthrough's own knowledge check; each
draws on two walkthroughs at once.

Aborts rather than writes if the expected insertion points are not found or if
counts do not rise by exactly one.
"""

import re
import shutil
from pathlib import Path

KEY = "l2-s2-assessment"
ROOT = Path(r"C:\Users\sarab\Desktop\Commusoft")
DASH = ROOT / "github" / "suncomfort-academy" / "dashboard.html"
SRC = ROOT / "Content" / "Reed - Script - L2 Series 2 Assessment The job record end to end.md"
BACKUP = DASH.with_name("dashboard.backup-pre-s2-assessment.html")

ENTRY = re.compile(r"COURSES\[\s*(?:'([^']+)'|\"([^\"]+)\"|(\d+))\s*\]\s*=\s*\{")


def counts(t):
    return (
        len(re.findall(r'<div class="walkthrough-num">', t)),
        len(set(re.findall(r'INBOX_FILES\["([^"]+)"\]', t)) | set(re.findall(r"INBOX_FILES\['([^']+)'\]", t))),
        len(ENTRY.findall(t)),
    )


def js(s):
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ").strip()


QUESTIONS = [
    ("A cost moving through the job",
     "A heat pump valve is ordered for Mrs. Thompson's job on Monday. It arrives Wednesday and Luke installs it on Thursday. Where has its cost been across those three days?",
     ["Actual costs throughout, from the moment it was ordered",
      "Forecasted while it was on order, moving to actual once it was installed",
      "Forecasted throughout, until the invoice is raised",
      "It does not appear as a cost until the job is marked complete"],
     "Forecasted while it was on order, moving to actual once it was installed",
     "A cost sits in Forecasted while the work or part is expected but not yet delivered, and moves to actual once it has actually happened. Ordering does not make a cost real; installing does. That is why a job's forecasted and actual figures rarely match until the work is finished.",
     "Forecasted covers what is expected, actual covers what has happened. The valve is forecasted while on order and becomes an actual cost when Luke installs it - not when it is ordered, and not when the invoice is raised."),
    ("Two businesses, two parts routes",
     "SunComfort uses stock control. A second business on Commusoft does not. In each case, who marks a part as ready for the technician, and where?",
     ["Both are marked by the office in the Parts tab - stock control changes only the reporting",
      "Without stock control the office marks the part available in the Parts tab; with stock control the stores team allocates it and the technician confirms installation from mobile",
      "With stock control the office does everything; without it the technician does everything",
      "Both are marked by the technician on site, at the point of installation"],
     "Without stock control the office marks the part available in the Parts tab; with stock control the stores team allocates it and the technician confirms installation from mobile",
     "Without stock control, a part is marked available in the Parts tab by whoever is sourcing it. With stock control there is a chain - stock is allocated, picked up, and then confirmed as installed by the technician in the mobile app, which is what moves it to Installed on the job. The same tab shows both, but the number of hands involved is different.",
     "Stock control does not just change reporting. It introduces allocation and pick-up steps, and it is the technician confirming installation on mobile that moves a part to Installed - not the office."),
    ("Two corrections, two mechanisms",
     "Jake uploads a photo to the wrong job, and on the same visit submits a commissioning form showing the wrong property address. Are these corrected the same way?",
     ["Yes - both are deleted from the job record and re-added correctly",
      "Yes - both are edited in place, since the job record allows amendments",
      "No - the photo can be removed or moved, but the form must be voided and a new one created",
      "No - the photo must be voided, but the form can be edited in place"],
     "No - the photo can be removed or moved, but the form must be voided and a new one created",
     "A file is a file: it can be removed from the job and added to the right one. A submitted form is a record with a signature and a timestamp behind it, so it cannot be edited or quietly deleted. It is voided, which leaves the void visible on the record, and a corrected form is created in its place. The audit trail is the reason for the difference.",
     "The two are not equivalent. A file can be removed or moved freely. A submitted form carries a signature and timestamp, so it is voided rather than edited or deleted, and a new one is created."),
    ("The sidebar and the timeline together",
     "Emma opens Mrs. Thompson's job. The sidebar shows an on-hold badge. What will the timeline add that the sidebar does not?",
     ["Nothing - the sidebar and the timeline show the same hold information",
      "The reminder date for taking the job off hold",
      "A record of who placed the job on hold and when, alongside everything else that has happened on the job",
      "The option to take the job off hold"],
     "A record of who placed the job on hold and when, alongside everything else that has happened on the job",
     "The sidebar shows the job's current state - that it is on hold, why, the reminder date, and the control to release it. The timeline shows the history: who did it, when, and how it sits among everything else that has happened. Current state and history are different questions, and the job record answers them in different places.",
     "The reminder date and the release control are both in the sidebar. What the timeline adds is history - who placed the hold and when, in sequence with everything else on the job."),
    ("Changing an appointment mid-flight",
     "Jake has tapped Travel for Mrs. Thompson's visit when she calls to move it to Thursday. Emma cancels the appointment and books a new one. What does the job record show afterwards?",
     ["The original appointment disappears and only Thursday's remains",
      "Both the cancellation and the new booking appear on the timeline, with the new appointment in the appointments tab",
      "The appointments tab shows both, but the timeline records only the new booking",
      "The job returns to an unbooked state until Thursday's appointment is confirmed"],
     "Both the cancellation and the new booking appear on the timeline, with the new appointment in the appointments tab",
     "Once a technician has started travelling, the appointment cannot be rescheduled in place - it is cancelled and a new one booked. Nothing is erased by that: the timeline keeps both events as history, while the appointments tab shows the appointment that now stands. The record of what was originally planned survives.",
     "Cancelling does not erase anything. The timeline holds both the cancellation and the new booking as history, and the appointments tab shows the appointment that now stands."),
    ("An opportunity that turns into work",
     "Mrs. Thompson's proposal included an optional filter upgrade she did not take at the time. Three weeks later she calls and accepts it. What has to happen for that upgrade to show as revenue on the job?",
     ["Nothing - the add-on was already counted when the proposal was sent",
      "It is counted once she accepts, and flows into the job's costs and invoice from there",
      "It stays an opportunity permanently and is invoiced separately",
      "Emma must raise a new job, because accepted add-ons cannot attach to an existing job"],
     "It is counted once she accepts, and flows into the job's costs and invoice from there",
     "An optional add-on is not revenue while it is only offered - it is counted when the customer selects it. Once accepted it stops being a tracked opportunity and becomes work on the job like anything else, appearing in costs and flowing through to the invoice.",
     "An offered add-on is not counted until it is selected, and once it is accepted it does not stay an opportunity or need a separate job. It becomes work on the job and flows into costs and the invoice."),
]

INTRO = ("You have worked through ten walkthroughs on the job record - the sidebar, the timeline, "
         "appointments, costs, invoices and WIP, files, forms, parts, stock control, and opportunities. "
         "Each of those covered one area on its own. This is where you put them together. Six questions "
         "following a single heat pump job at Mrs. Thompson's property from booking to invoice. Each one "
         "needs more than one part of the job record to answer. You need five correct to pass, and you can "
         "retake it as many times as you like. Your certificate arrives by email.")

CLOSE = ("A cost that moved from forecasted to actual when the part went in. A parts chain that changes "
         "shape depending on whether stock control is switched on. A file you can move and a form you "
         "cannot. A sidebar that says what is true now and a timeline that says how it got there. The job "
         "record is not ten separate tabs. It is one record showing you the same job from ten angles, and "
         "reading it well means knowing which angle answers which question. Series 2 is complete.")

CARD = (
    f'<div class="walkthrough-card" onclick="openPanel(\'{KEY}\')">'
    '<div class="walkthrough-num">Series assessment</div>'
    '<div class="walkthrough-title">The job record, end to end</div>'
    '<div class="walkthrough-meta"><span class="meta-pill">6 questions</span>'
    '<span class="meta-pill">Office teams</span>'
    '<span class="badge" style="background:#fff3ee;color:#fa6932">Draft</span></div></div>'
)


def courses_entry():
    scenes = [f'{{type:"section", heading:"What this is", body:"{js(INTRO)}"}}']
    for i, (head, q, opts, correct, fb, fba) in enumerate(QUESTIONS, 1):
        o = ", ".join(f'"{js(x)}"' for x in opts)
        scenes.append(
            f'{{type:"reflection", label:"Question {i}", question:"{js(head)} \\u2014 {js(q)}", '
            f'options:[{o}], correct:"{js(correct)}", feedback:"{js(fb)}", feedbackAlt:"{js(fba)}"}}'
        )
    scenes.append(f'{{type:"section", heading:"Series close", body:"{js(CLOSE)}"}}')
    body = ",\n    ".join(scenes)
    return f"""
COURSES['{KEY}'] = {{
  contentType: "Series assessment",
  pathLabel: "L2 Office teams \\u2014 Series 2: The job record \\u2014 Series assessment",
  title: "The job record, end to end",
  duration: "6 questions",
  persona: "Office teams",
  characters: "Emma Fletcher (Office manager), Claire Hudson (Administrator / Financial office staff), Jake Morrison and Luke Patterson (Technicians), referenced in scenario",
  scenario: "A single heat pump job at Mrs. Thompson's property, followed from booking through to invoice. Six decisions land along the way, each one drawing on more than one part of the job record.",
  objectives: [
    "Trace a cost through the job record as work moves from booked to completed",
    "Choose the right parts route depending on whether stock control is in use",
    "Correct field data using the right mechanism for the record type",
    "Read the sidebar and the timeline together to understand a job's current state",
    "Recognise what the job record does automatically and what needs a person"
  ],
  productionSetup: [
    "*Delivered as a Google Form in quiz mode, with Certify'em for the certificate.",
    "*Pass mark 5 of 6. Unlimited retakes. Email collected for the certificate.",
    "*Archer narrates the opening and close only. The questions are answered in the form, not on screen.*"
  ],
  buildBySection: [
    {{section:"What this is", media:"Written text", note:"Article copy introducing the assessment and the pass mark, with the link out to the form."}},
    {{section:"Questions 1 to 6", media:"Google Form", note:"Scored in the form. Quiz mode, pass mark 5 of 6, unlimited retakes, email collected for the certificate."}},
    {{section:"Series close", media:"Written text", note:"Used as the form's confirmation message."}}
  ],
  productionNotes: [
    "No product recording needed.",
    "Series 2 had no challenge to convert, so these six questions are new. Each draws on two walkthroughs at once and none repeats a walkthrough's own knowledge check, which stay in the articles as single-answer recall."
  ],
  scenes: [
    {body}
  ]
}};
"""


def main():
    text = DASH.read_text(encoding="utf-8")
    before = counts(text)

    if f"COURSES['{KEY}']" in text or f'openPanel(\'{KEY}\')' in text:
        raise SystemExit(f"ABORT: {KEY} already exists")

    # 1. card, straight after Walkthrough 10
    anchor = '<div class="walkthrough-card" onclick="openPanel(10)">'
    i = text.find(anchor)
    if i < 0:
        raise SystemExit("ABORT: could not find the Walkthrough 10 card")
    end = text.find("</div></div>", i)
    if end < 0:
        raise SystemExit("ABORT: could not find the end of the Walkthrough 10 card")
    end += len("</div></div>")
    text = text[:end] + "\n          " + CARD + text[end:]
    print("card inserted after Walkthrough 10")

    # 2. COURSES entry, straight after COURSES[10]
    m = ENTRY.search(text, text.find("COURSES[10]"))
    if not m:
        raise SystemExit("ABORT: could not find COURSES[10]")
    nxt = ENTRY.search(text, m.end())
    at = nxt.start() if nxt else text.find("};", m.end()) + 2
    text = text[:at] + courses_entry() + text[at:]
    print("COURSES entry inserted after COURSES[10]")

    # 3. INBOX_FILES, straight after the one for key "10"
    md = SRC.read_text(encoding="utf-8")
    escaped = md.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")
    anchor2 = 'INBOX_FILES["10"] = `'
    j = text.find(anchor2)
    if j < 0:
        raise SystemExit("ABORT: could not find INBOX_FILES[\"10\"]")
    k = text.find("`;", j + len(anchor2))
    if k < 0:
        raise SystemExit("ABORT: could not find the end of INBOX_FILES[\"10\"]")
    k += 2
    text = text[:k] + f'\n\nINBOX_FILES["{KEY}"] = `{escaped}`;' + text[k:]
    print(f"INBOX_FILES inserted ({len(md)} chars)")

    after = counts(text)
    print(f"\ncards {before[0]} -> {after[0]}   inbox {before[1]} -> {after[1]}   courses {before[2]} -> {after[2]}")
    if after != tuple(b + 1 for b in before):
        raise SystemExit("ABORT: counts did not all rise by exactly one")

    shutil.copy2(DASH, BACKUP)
    DASH.write_text(text, encoding="utf-8")
    print(f"backed up to {BACKUP.name}\nWRITTEN")


if __name__ == "__main__":
    main()
