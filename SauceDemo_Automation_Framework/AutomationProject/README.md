# SauceDemo Automation Testing Framework

Reusable Selenium 4 + PyTest framework for the lab brief. Covers FR-01 through FR-16 with Page Object Model, CSV-driven cases, failure screenshots, rotating logs, HTML test results, and a separate JMeter workload.

## Stack and structure

Python 3.11+, Selenium 4, PyTest, WebDriver Manager, PyTest-HTML, CSV, Java 17+, Apache JMeter 5.6+.

```text
AutomationProject/
  pages/                 Base, Login, Products, Cart, Checkout page objects
  tests/                 Functional tests for FR-01 through FR-16
  testdata/              Login and postal-code CSV inputs
  reports/               PyTest report, dashboard, screenshots, logs
  performance/jmx/       JMeter load plan
  performance/results/   JTL and aggregate summary
  performance/html_report/ JMeter dashboard
  performance/Findings.md Performance findings and limitations
  utils/                 Configuration and logging
  conftest.py             Browser fixtures and screenshot hook
  pytest.ini              Markers and report options
  requirements.txt
```

## Windows PowerShell setup and Selenium

Open PowerShell in this folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pytest
```

If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` and activate again. `pytest -m smoke` runs the critical path; `pytest -m regression` runs all functional tests. Headless is default; set `$env:HEADLESS = "false"` for a visible browser. Use `$env:BROWSER = "edge"` for Edge, and unset the variable to return to Chrome. Drivers are fetched on first execution. Use `SAUCEDEMO_BASE_URL`, `SAUCEDEMO_USERNAME`, `SAUCEDEMO_PASSWORD`, and `WAIT_TIMEOUT` to override runtime settings.

Each normal run creates `reports/report.html` with counts and duration. Failures save screenshots under `reports/screenshots/`, attached to the report where supported; timestamped logs are under `reports/logs/automation.log`.

## Section dashboard

Open `reports/dashboard.html` to see passed cases by Login, Products & Cart, and Checkout. After updating statuses in `test_cases.csv`, refresh it with:

```powershell
python reports/generate_dashboard.py
```

## JMeter

Install Java 17+ and Apache JMeter 5.6+. From the project folder, run:

```powershell
powershell -ExecutionPolicy Bypass -File performance/run_jmeter.ps1 `
  -JMeter "C:\Program Files\apache-jmeter-5.6.3\bin\jmeter.bat"
```

The plan uses 20 users, a 60-second ramp, and 180 seconds. It writes raw samples to `performance/results/results.jtl`, a summary to `aggregate.csv`, and a JMeter dashboard under `performance/html_report/`. The runner compiles an in-memory Java Preferences provider for headless execution in locked-down Windows profiles; it only affects that JMeter process. NFR thresholds: login document P95 < 3,000 ms, authenticated app-shell P95 < 4,000 ms, overall error rate < 2%.

## Test design and observed results

`test_cases.csv` records test IDs, requirement IDs, test data, preconditions, steps, expected and actual results, status, and technique. Login and checkout CSVs provide equivalence classes and boundary values. All FRs are automated. On November 5, 2026, 21 Selenium cases ran: 19 passed and two FR-14 cases failed because the AUT accepted a 4-digit and a non-numeric postal value. These failures are kept visible in the report and matrix.

## JMeter network behavior and limitations

Inspection of the current SauceDemo client showed that login validation runs in browser JavaScript and stores a `session-username` cookie; credentials are not posted to a server authentication endpoint. The plan sets that client marker in a cookie manager and requests the app shell and discovered JS/CSS assets. JMeter does not execute React, so route samples measure HTTP documents rather than rendered UI timing. Measured results are specific to the test host, network, date, and public demo instance; see `performance/Findings.md`.
