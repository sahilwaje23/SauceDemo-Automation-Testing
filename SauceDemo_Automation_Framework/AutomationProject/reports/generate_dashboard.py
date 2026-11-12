"""Generate a standalone section dashboard from test_cases.csv."""
import csv
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = [("Login", range(1, 6)), ("Products & Cart", range(6, 11)), ("Checkout", range(11, 17))]


def main():
    with (ROOT / "test_cases.csv").open(newline="", encoding="utf-8-sig") as stream:
        cases = list(csv.DictReader(stream))
    total = len(cases)
    passed = sum(row["Status"] == "PASS" for row in cases)
    failed = sum(row["Status"].startswith("FAIL") for row in cases)
    cards = []
    for name, reqs in SECTIONS:
        group = [r for r in cases if int(r["Requirement ID"].split("-")[1]) in reqs]
        ok = sum(r["Status"] == "PASS" for r in group)
        bad = sum(r["Status"].startswith("FAIL") for r in group)
        width_ok = ok / len(group) * 100 if group else 0
        width_bad = bad / len(group) * 100 if group else 0
        note = '<p class="note">FR-14: AUT accepted 1234 and AB12X.</p>' if name == "Checkout" and bad else ""
        cards.append(f"""<article class="card"><div class="heading"><h2>{escape(name)}</h2><strong>{ok}<small> / {len(group)}</small></strong></div>
          <div class="bar" aria-label="{ok} passed, {bad} failed"><i style="width:{width_ok:.1f}%"></i><b style="width:{width_bad:.1f}%"></b></div>
          <p class="legend"><span class="green">● {ok} passed</span><span class="red">● {bad} failed</span></p>{note}</article>""")
    html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>SauceDemo Test Dashboard</title>
    <style>body{{margin:0;background:#f4f7fb;color:#172334;font:15px/1.5 'Segoe UI',Arial,sans-serif}}main{{max-width:1050px;margin:42px auto;padding:0 22px}}.eyebrow{{color:#64748b;font-size:11px;letter-spacing:.12em;font-weight:700}}h1{{font-size:32px;margin:0}}.date{{color:#64748b;margin-top:6px}}.summary,.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:26px 0}}.cards{{grid-template-columns:repeat(3,1fr);margin-top:14px}}.metric,.card{{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:20px;box-shadow:0 4px 16px #2538580a}}.metric span{{color:#64748b}}.metric strong{{display:block;font-size:29px;margin-top:5px}}.good{{color:#13805c}}.bad{{color:#bd3c49}}.heading{{display:flex;align-items:center;justify-content:space-between}}h2{{font-size:19px;margin:3px 0}}.heading strong{{color:#13805c;font-size:25px}}small{{color:#64748b;font-size:15px;font-weight:500}}.bar{{display:flex;height:10px;background:#e8edf3;border-radius:8px;overflow:hidden;margin-top:23px}}.bar i{{background:#13805c}}.bar b{{background:#bd3c49}}.legend{{display:flex;gap:17px;font-size:13px;color:#475569}}.green{{color:#13805c}}.red{{color:#bd3c49}}.note{{padding:10px;background:#fff3f3;color:#87363f;border-left:3px solid #bd3c49;font-size:12px}}footer{{font-size:12px;color:#64748b;margin:24px 0}}@media(max-width:720px){{.cards{{grid-template-columns:1fr}}.summary{{grid-template-columns:repeat(2,1fr)}}}}</style></head>
    <body><main><p class="eyebrow">AUTOMATION FRAMEWORK · SAUCEDEMO</p><h1>Test results dashboard</h1><p class="date">Updated {date.today().strftime('%B %d, %Y')}</p>
    <section class="summary"><div class="metric"><span>Total test cases</span><strong>{total}</strong></div><div class="metric good"><span>Passed</span><strong>{passed}</strong></div><div class="metric bad"><span>Failed</span><strong>{failed}</strong></div><div class="metric"><span>Pass rate</span><strong>{(passed/total*100 if total else 0):.1f}%</strong></div></section>
    <p class="eyebrow">PASSED CASES BY SECTION</p><section class="cards">{''.join(cards)}</section><footer>Counts are based on <code>test_cases.csv</code>. Refresh with <code>python reports/generate_dashboard.py</code> after changing case statuses.</footer></main></body></html>"""
    output = ROOT / "reports/dashboard.html"
    output.write_text(html, encoding="utf-8")
    print(f"Generated {output}")


if __name__ == "__main__":
    main()
