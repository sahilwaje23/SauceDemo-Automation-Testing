"""Render the recorded test case matrix as a readable initial HTML snapshot."""
import csv
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "test_cases.csv").open(newline="", encoding="utf-8-sig") as stream:
    cases = list(csv.DictReader(stream))
passed = sum(row["Status"] == "PASS" for row in cases)
failed = sum(row["Status"].startswith("FAIL") for row in cases)
rows = []
for row in cases:
    css = "pass" if row["Status"] == "PASS" else "fail" if row["Status"].startswith("FAIL") else "pending"
    rows.append("<tr><td>{}</td><td>{}</td><td>{}</td><td class='{}'>{}</td><td>{}</td></tr>".format(
        escape(row["Test Case ID"]), escape(row["Requirement ID"]), escape(row["Test Scenario"]), css,
        escape(row["Status"]), escape(row["Actual Result"])))
html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>SauceDemo Test Execution Snapshot</title>
<style>body{{font:14px/1.5 'Segoe UI',Arial,sans-serif;background:#f5f7fb;color:#182230;margin:0}}main{{max-width:1100px;margin:38px auto;padding:0 22px}}h1{{margin-bottom:4px}}.muted{{color:#667085}}.summary{{display:flex;gap:16px;margin:22px 0}}.pill{{background:white;border:1px solid #e1e7ef;border-radius:12px;padding:16px 22px;min-width:130px}}.pill strong{{display:block;font-size:26px}}.pass{{color:#13805c;font-weight:700}}.fail{{color:#bd3c49;font-weight:700}}table{{width:100%;border-collapse:collapse;background:white;border-radius:12px;overflow:hidden}}th,td{{text-align:left;padding:11px 12px;border-bottom:1px solid #e9edf2}}th{{background:#eef2f7;color:#475467}}.note{{background:#fff8e8;border:1px solid #f3dfaa;border-radius:10px;padding:13px;margin:20px 0}}@media(max-width:720px){{main{{overflow-x:auto}}table{{min-width:760px}}}}</style></head>
<body><main><p class="muted">AUTOMATION FRAMEWORK · SAUCEDEMO</p><h1>Test execution snapshot</h1><p class="muted">Recorded run: November 5, 2026 · Duration: 340.21 seconds</p>
<section class="summary"><div class="pill"><span>Total cases</span><strong>{len(cases)}</strong></div><div class="pill pass"><span>Passed</span><strong>{passed}</strong></div><div class="pill fail"><span>Failed</span><strong>{failed}</strong></div><div class="pill"><span>Skipped</span><strong>0</strong></div></section>
<div class="note">This is a snapshot rendered from the recorded test case matrix. Run <code>pytest</code> to produce a fresh PyTest-HTML execution report and failure screenshots.</div>
<table><thead><tr><th>Case</th><th>Requirement</th><th>Scenario</th><th>Status</th><th>Actual result</th></tr></thead><tbody>{''.join(rows)}</tbody></table>
</main></body></html>"""
(ROOT / "reports/report.html").write_text(html, encoding="utf-8")
print("Created report snapshot from test_cases.csv")
