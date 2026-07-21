import csv
import sys
import os

STUDENT_NAME = "Aline Uwimana"  # Umunyeshuri / Student


def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists,
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ").strip()

    if not filename:
        print("Error: You must enter a filename. / Ntabwo wanditse izina rya dosiye.")
        sys.exit(1)

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found. / Dosiye ntiboneka.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Make sure the required columns actually exist in the header
            required_columns = {'assignment', 'group', 'score', 'weight'}
            if reader.fieldnames is None or not required_columns.issubset(set(reader.fieldnames)):
                print("Error: CSV is missing required columns "
                      "(assignment, group, score, weight). / Inyandiko idakwiye.")
                sys.exit(1)

            for row_number, row in enumerate(reader, start=2):  # start=2: row 1 is the header
                # Skip completely blank rows
                if not any((row.get(key) or "").strip() for key in row):
                    continue

                assignment = (row.get('assignment') or "").strip()
                group = (row.get('group') or "").strip()
                raw_score = (row.get('score') or "").strip()
                raw_weight = (row.get('weight') or "").strip()

                if not assignment or not group or raw_score == "" or raw_weight == "":
                    print(f"Warning: Row {row_number} is missing data and was skipped. "
                          f"/ Umurongo {row_number} ufite amakuru abura.")
                    continue

                if group not in ("Formative", "Summative"):
                    print(f"Warning: Row {row_number} has an unknown group '{group}' "
                          f"(expected 'Formative' or 'Summative') and was skipped.")
                    continue

                try:
                    score = float(raw_score)
                    weight = float(raw_weight)
                except ValueError:
                    print(f"Warning: Row {row_number} has a non-numeric score/weight "
                          f"and was skipped. / Umurongo {row_number} ufite amanota adakwiye.")
                    continue

                assignments.append({
                    'assignment': assignment,
                    'group': group,
                    'score': score,
                    'weight': weight
                })

        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Evaluates the student's grades:
      a) Checks all scores are within 0-100
      b) Validates weights (Total=100, Summative=40, Formative=60)
      c) Calculates the Final Grade and GPA
      d) Determines Pass/Fail status (>= 50% in BOTH categories)
      e) Finds failed formative assignments eligible for resubmission
      f) Prints the final decision
    """
    print("\n--- Processing Grades / Turimo gusesengura amanota ---")
    print(f"Student / Umunyeshuri: {STUDENT_NAME}\n")

    # Handle a completely empty dataset gracefully (e.g. a freshly reset grades.csv)
    if not data:
        print("No assignment records found. Nothing to evaluate. "
              "/ Nta manota abonetse. Ntacyo dushobora gusesengura.")
        return

    # ------------------------------------------------------------------
    # a) Grade range validation (0-100)
    # ------------------------------------------------------------------
    out_of_range = [a for a in data if not (0 <= a['score'] <= 100)]
    if out_of_range:
        print("Error: The following assignments have scores outside the 0-100 range:")
        for a in out_of_range:
            print(f"  - {a['assignment']}: {a['score']}")
        print("Please correct the data before evaluation can continue. "
              "/ Amanota agomba kuba hagati ya 0 na 100.")
        return

    # ------------------------------------------------------------------
    # b) Weight validation (Total = 100, Summative = 40, Formative = 60)
    # ------------------------------------------------------------------
    formative = [a for a in data if a['group'] == 'Formative']
    summative = [a for a in data if a['group'] == 'Summative']

    total_weight = sum(a['weight'] for a in data)
    formative_weight = sum(a['weight'] for a in formative)
    summative_weight = sum(a['weight'] for a in summative)

    weight_errors = []
    if abs(total_weight - 100) > 1e-9:
        weight_errors.append(f"Total weight is {total_weight}, expected 100.")
    if abs(formative_weight - 60) > 1e-9:
        weight_errors.append(f"Formative weight is {formative_weight}, expected 60.")
    if abs(summative_weight - 40) > 1e-9:
        weight_errors.append(f"Summative weight is {summative_weight}, expected 40.")

    if weight_errors:
        print("Error: Weight validation failed / Ikosa mu bipimo:")
        for err in weight_errors:
            print(f"  - {err}")
        print("Evaluation cannot continue until weights are corrected.")
        return

    # ------------------------------------------------------------------
    # c) Final Grade & GPA calculation
    # ------------------------------------------------------------------
    total_grade = sum(a['score'] * a['weight'] for a in data) / total_weight
    gpa = (total_grade / 100) * 5.0

    formative_pct = sum(a['score'] * a['weight'] for a in formative) / formative_weight
    summative_pct = sum(a['score'] * a['weight'] for a in summative) / summative_weight

    print(f"Formative average / Impuzandengo y'aya Formative: {formative_pct:.2f}%")
    print(f"Summative average / Impuzandengo y'aya Summative: {summative_pct:.2f}%")
    print(f"Final Grade / Amanota y'Umwaka: {total_grade:.2f}%")
    print(f"GPA: {gpa:.2f} / 5.0")

    # ------------------------------------------------------------------
    # d) Pass/Fail decision (>= 50% in BOTH categories)
    # ------------------------------------------------------------------
    passed = formative_pct >= 50 and summative_pct >= 50

    # ------------------------------------------------------------------
    # e) Resubmission logic: failed formative assignments (< 50%)
    #    -> only those with the highest weight among the failed ones
    # ------------------------------------------------------------------
    failed_formatives = [a for a in formative if a['score'] < 50]
    resubmission_list = []
    if failed_formatives:
        highest_weight = max(a['weight'] for a in failed_formatives)
        resubmission_list = [a for a in failed_formatives if a['weight'] == highest_weight]

    # ------------------------------------------------------------------
    # f) Final decision printout
    # ------------------------------------------------------------------
    print("\n--- Final Decision / Icyemezo cya Nyuma ---")
    if passed:
        print("Status: PASSED / YATSINZE")
    else:
        print("Status: FAILED / YARANZE")

    if resubmission_list:
        print("\nResubmission required for / Agomba kongera gukora:")
        for a in resubmission_list:
            print(f"  - {a['assignment']} (score: {a['score']}, weight: {a['weight']})")
    elif not passed:
        print("\nNo formative assignment scored below 50%, but the student still failed "
              "overall (check Summative average).")
    else:
        print("\nNo resubmission needed. / Nta gikorwa cyo gusubiramo gikenewe.")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
