import pandas as pd
import re
import os
from tkinter import Tk, filedialog


def is_valid_required_name(name):
    """Validate REQUIRED name: English + Indian languages, 3–25 chars."""
    if not isinstance(name, str):
        return False

    name = name.strip()
    if not name:
        return False

    if len(name) < 3 or len(name) > 25:
        return False

    return _matches_name_pattern(name)


def is_valid_optional_name(name):
    """
    Validate OPTIONAL name:
    - blank / NaN is allowed
    - otherwise must be valid like required name
    """
    if name is None:
        return True

    name = str(name).strip()
    if name == "":
        return True

    return is_valid_required_name(name)


def _matches_name_pattern(name):
    """Shared regex check for English + Indian language characters."""
    pattern = (
        r"^[A-Za-z"
        r"\u0900-\u097F"  # Devanagari
        r"\u0980-\u09FF"  # Bengali
        r"\u0A00-\u0A7F"  # Gurmukhi
        r"\u0A80-\u0AFF"  # Gujarati
        r"\u0B00-\u0B7F"  # Oriya
        r"\u0B80-\u0BFF"  # Tamil
        r"\u0C00-\u0C7F"  # Telugu
        r"\u0C80-\u0CFF"  # Kannada
        r"\u0D00-\u0D7F"  # Malayalam
        r"][A-Za-z"
        r"\u0900-\u097F"
        r"\u0980-\u09FF"
        r"\u0A00-\u0A7F"
        r"\u0A80-\u0AFF"
        r"\u0B00-\u0B7F"
        r"\u0B80-\u0BFF"
        r"\u0C00-\u0C7F"
        r"\u0C80-\u0CFF"
        r"\u0D00-\u0D7F"
        r"' -]*[A-Za-z"
        r"\u0900-\u097F"
        r"\u0980-\u09FF"
        r"\u0A00-\u0A7F"
        r"\u0A80-\u0AFF"
        r"\u0B00-\u0B7F"
        r"\u0B80-\u0BFF"
        r"\u0C00-\u0C7F"
        r"\u0C80-\u0CFF"
        r"\u0D00-\u0D7F"
        r"]$"
    )

    if not re.match(pattern, name):
        return False

    if re.search(r"[ '-]{2,}", name):
        return False

    return True


def filter_valid_names(input_file, first_name_col, last_name_col):
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file, low_memory=False)
    else:
        df = pd.read_excel(input_file)

    # First name MUST exist
    df = df.dropna(subset=[first_name_col])

    mask = df.apply(
        lambda row:
            is_valid_required_name(row[first_name_col]) and
            is_valid_optional_name(row[last_name_col]),
        axis=1
    )

    valid_df = df[mask]

    base, _ = os.path.splitext(input_file)
    output_file = base + "_valid_names.xlsx"

    valid_df.to_excel(output_file, index=False)

    print(f"\n✅ {len(valid_df)} valid name rows saved to: {output_file}")
    print(f"💾 Skipped {len(df) - len(valid_df)} invalid rows.\n")


def resolve_column(col_input, columns):
    col_input = col_input.strip()

    if col_input.isdigit():
        idx = int(col_input) - 1
        if 0 <= idx < len(columns):
            return columns[idx]
        raise ValueError(f"❌ Invalid column number: {col_input}")

    if col_input in columns:
        return col_input

    raise ValueError(f"❌ Column not found: {col_input}")


def main():
    print("📂 Select your input file (CSV or Excel)...")

    Tk().withdraw()
    input_file = filedialog.askopenfilename(
        title="Select input file",
        filetypes=[("Excel or CSV", "*.xlsx *.csv")]
    )

    if not input_file:
        print("❌ No file selected. Exiting.")
        return

    df = pd.read_excel(input_file) if input_file.endswith(".xlsx") else pd.read_csv(input_file, low_memory=False)

    print("\n📋 Columns detected in your file:")
    for i, col in enumerate(df.columns):
        print(f"  {i + 1}. {col}")

    first_input = input("\nEnter FIRST NAME column (number or name): ")
    last_input = input("Enter LAST NAME column (number or name): ")

    try:
        first_col = resolve_column(first_input, df.columns)
        last_col = resolve_column(last_input, df.columns)
    except ValueError as e:
        print(e)
        return

    filter_valid_names(input_file, first_col, last_col)


if __name__ == "__main__":
    main()
