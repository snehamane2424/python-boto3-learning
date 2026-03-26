print("DEBUG: main.py started")

from lambda_service import list_all_functions
from utils import extract_required_fields, save_to_json, print_functions
from config import OUTPUT_FILE


def main():
    print("Fetching Lambda functions...")

    functions = list_all_functions()

    print(f"Total functions found: {len(functions)}")

    extracted_data = extract_required_fields(functions)

    print("\nPrinting Functions:\n")
    print_functions(extracted_data)

    save_to_json(extracted_data, OUTPUT_FILE)

    print(f"\nData saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()