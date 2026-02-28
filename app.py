import pandas as pd
import re
import os
from tkinter import Tk, filedialog

def is_valid_name(name):
    """Check if a name is likely a valid English or German name."""
    if not isinstance(name, str):
        return False

    name = name.strip()

    # Skip blank or missing names
    if not name:
        return False

    # Basic length check
    if len(name) < 3 or len(name) > 25:
        return False

    # Regex pattern for English + German letters (allows spaces, hyphens, apostrophes)
    pattern = r"^[A-Za-zÄÖÜäöüß][A-Za-zÄÖÜäöüß' -]*[A-Za-zÄÖÜäöüß]$"
    if not re.match(pattern, name):
        return False

    # No consecutive apostrophes or hyphens
    if re.search(r"[' -]{2,}", name):
        return False

    return True


def filter_valid_names(input_file, first_name_col, last_name_col):
    """Filter valid English + German names and save to Excel in same folder."""
    # Load data
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    else:
        df = pd.read_excel(input_file)

    # Drop completely empty rows in name columns
    df = df.dropna(subset=[first_name_col, last_name_col])

    # Apply validation
    mask = (
        df[first_name_col].apply(is_valid_name) &
        df[last_name_col].apply(is_valid_name)
    )

    valid_df = df[mask]

    # Output file path (same folder as input)
    base, _ = os.path.splitext(input_file)
    output_file = base + "_valid.xlsx"

    # Save valid entries to Excel
    valid_df.to_excel(output_file, index=False)

    print(f"\n✅ {len(valid_df)} valid rows saved to: {output_file}")
    print(f"💾 Skipped {len(df) - len(valid_df)} invalid or blank rows.\n")


def main():
    """Main interactive function."""
    print("📂 Select your input file (CSV or Excel)...")
    
    Tk().withdraw()  # hide the Tkinter root window
    input_file = filedialog.askopenfilename(
        title="Select input file",
        filetypes=[("Excel or CSV", "*.xlsx *.csv")]
    )

    if not input_file:
        print("❌ No file selected. Exiting.")
        return

    df = pd.read_excel(input_file) if input_file.endswith(".xlsx") else pd.read_csv(input_file)
    print("\n📋 Columns detected in your file:")
    for i, col in enumerate(df.columns):
        print(f"  {i + 1}. {col}")

    first_col = input("\nEnter the column name for FIRST NAME: ").strip()
    last_col = input("Enter the column name for LAST NAME: ").strip()

    filter_valid_names(input_file, first_col, last_col)


if __name__ == "__main__":
    main()
