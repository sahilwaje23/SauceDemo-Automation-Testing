"""Summarize CSV-format JMeter output without third-party packages."""
import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "results/results.jtl"
OUTPUT = ROOT / "results/aggregate.csv"


def main():
    if not SOURCE.exists():
        raise SystemExit(f"Missing JMeter results: {SOURCE}")
    groups = defaultdict(list)
    with SOURCE.open(newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            groups[row["label"]].append(row)
    if not any(groups.values()):
        raise SystemExit("The JTL contains no sample rows")
    with OUTPUT.open("w", newline="", encoding="utf-8") as stream:
        fields = ["label", "samples", "errors", "error_percent", "mean_ms", "p95_ms"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for label, rows in sorted(groups.items()):
            values = sorted(int(row["elapsed"]) for row in rows)
            errors = sum(row["success"].lower() != "true" for row in rows)
            writer.writerow({"label": label, "samples": len(rows), "errors": errors,
                             "error_percent": f"{100*errors/len(rows):.3f}",
                             "mean_ms": f"{sum(values)/len(values):.1f}",
                             "p95_ms": values[max(0, math.ceil(.95*len(values))-1)]})
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
