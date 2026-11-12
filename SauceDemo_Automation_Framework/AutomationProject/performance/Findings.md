# JMeter Findings

## Run profile and measurements

Apache JMeter 5.6.3, Java 17; 20 users, 60-second ramp-up, 180-second duration. The measured run recorded 17,160 samples and 0 HTTP errors (0.000%).

| NFR | Measured P95 | Error rate | Result | Observation |
|---|---:|---:|---|---|
| NFR-01 Login page < 3,000 ms | 451 ms | 0.000% overall | PASS (HTTP document) | `GET /` login document, before session cookie. |
| NFR-02 Products page < 4,000 ms | 455 ms | 0.000% overall | PASS (HTTP document) | Authenticated app-shell `GET /` with session cookie. |
| NFR-03 Overall errors < 2% | N/A | 0.000% | PASS | 0 errors across 17,160 requests. |

Additional resource samples: JavaScript bundle P95 3,393 ms (20 requests); CSS bundle P95 650 ms (20 requests).

## Network behavior and limits

The current SauceDemo React application validates login in browser JavaScript and stores `session-username`; it does not submit credentials to a server login endpoint. Direct `GET /inventory.html` returns 404. The JMeter plan therefore requests the login document, sets the client session marker in a per-thread cookie manager, requests the root app shell as the authenticated state, then fetches the JS/CSS bundle paths extracted from the shell. JMeter cannot execute React. NFR P95 values represent HTTP document responses, not browser-rendered product content or end-to-end login. Results reflect one test host, network path, date, and public demo deployment.
