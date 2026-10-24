
from pathlib import Path
import pandas as pd

# Locate the project folders
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = Path(__file__).resolve().parent / "data_inspections_csv"
REPORT_DIR = PROJECT_DIR / "reports"


def check_hive(row):
    """Recommend an action based on hive inspection records."""
    issues = []

    if row["pests_detected"]:
        issues.append("Inspect reported pest issue")

    if not row["colony_active"]:
        issues.append("Verify colony activity")

    if row["days_since_inspection"] > 14:
        issues.append("Schedule overdue inspection")

    if issues:
        return "; ".join(issues)

    return "No immediate flag"


def main():
    # Load sample inspection data
    df = pd.read_csv(DATA_FILE)

    # Convert CSV text values into Python booleans
    df["colony_active"] = (
        df["colony_active"].astype(str).str.lower().map(
            {"true": True, "false": False}
        )
    )

    df["pests_detected"] = (
        df["pests_detected"].astype(str).str.lower().map(
            {"true": True, "false": False}
        )
    )

    # Check the quality of the data
    print("Total hives:", len(df))
    print("Missing hive IDs:", df["hive_id"].isna().sum())
    print("Duplicate hive IDs:", df["hive_id"].duplicated().sum())
    print("Negative honey values:", (df["honey_kg"] < 0).sum())

    # Identify hives that need attention
    df["recommended_action"] = df.apply(check_hive, axis=1)

    follow_up = (
        df["recommended_action"] != "No immediate flag"
    ).sum()

    print("Hives requiring follow-up:", follow_up)
    print("Total honey recorded (kg):", df["honey_kg"].sum())

    # Save the monitoring report
    REPORT_DIR.mkdir(exist_ok=True)
    report_file = REPORT_DIR / "Kwale_Beekeepers_monitoring_report.csv"
    df.to_csv(report_file, index=False)

    print("Monitoring report saved to:", report_file)


if __name__ == "__main__":
    main()
