# Lab 1: Grade Evaluator & Archiver

**Muraho!** (Hello!) This project evaluates a student's grades from a CSV file
and archives the grade file with a timestamp using a Bash script.

Sample student used for testing: **Aline Uwimana**.

## Files

- `grade-evaluator.py` — reads `grades.csv`, validates it, calculates the
  final grade / GPA, and decides Pass/Fail with resubmission recommendations.
- `organizer.sh` — archives `grades.csv` into `archive/` with a timestamp,
  resets a fresh empty `grades.csv`, and logs the action to `organizer.log`.
- `grades.csv` — sample grade data.

## How to run the Python evaluator

```bash
python3 grade-evaluator.py
```

You'll be prompted for a filename — type `grades.csv` and press Enter.

The script will:
1. Check every score is between 0 and 100.
2. Check weights: total = 100, Formative = 60, Summative = 40.
3. Calculate the Final Grade and GPA (`GPA = (Total Grade / 100) * 5.0`).
4. Print PASSED / FAILED (requires ≥ 50% in **both** Formative and Summative).
5. List any failed Formative assignment(s) with the highest weight as
   eligible for resubmission (ties are all listed).

It also handles a missing file, an empty CSV, malformed rows, bad weight
totals, and out-of-range scores gracefully — with clear messages instead
of crashing. *Nta na kimwe kigomba guhagarara mu buryo budasobanutse!*
(Nothing should crash unexpectedly!)

## How to run the organizer script

```bash
chmod +x organizer.sh   # only needed once
./organizer.sh
```

Each run will:
1. Create an `archive/` folder if it doesn't exist.
2. Move the current `grades.csv` into `archive/` renamed with a timestamp
   (e.g. `grades_20260721-154041.csv`). If two runs happen in the same
   second, a counter suffix (`_1`, `_2`, ...) is added so no file is ever
   overwritten.
3. Create a brand-new, empty `grades.csv` ready for the next batch.
4. Append a line to `organizer.log` recording the timestamp, original
   filename, and the archived filename — this log accumulates across runs.

## Notes

- GPA formula: `GPA = (Total Grade / 100) * 5.0`.
- Category averages (Formative / Summative) are each weighted internally
  by that category's own assignment weights, then compared against the
  50% pass threshold separately — **murakoze!** (thank you) for checking
  both categories, not just the overall total.
