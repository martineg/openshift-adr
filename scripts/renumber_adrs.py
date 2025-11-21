import argparse
import re
import sys
import os

def renumber_adrs(file_path, prefix, dry_run=False):
    """
    Reads a markdown file, finds headers matching '## PREFIX-xx',
    renumbers them sequentially, and overwrites the file inline.
    """
    
    # Regex to match lines starting with '## PREFIX-Digits'
    pattern = re.compile(rf"^(##\s+){re.escape(prefix)}-\d+(.*)")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at: {file_path}")
        print(f"Ensure '{prefix}.md' exists in the 'adr' folder.")
        sys.exit(1)

    new_lines = []
    counter = 1
    changed_count = 0

    print(f"Target File: {file_path}")
    print(f"Prefix:      {prefix}\n")

    for line in lines:
        match = pattern.match(line)
        if match:
            # Format new number (01, 02, etc.)
            new_number = f"{counter:02d}"
            new_id = f"{prefix}-{new_number}"
            
            # Reconstruct the line
            new_line = f"{match.group(1)}{new_id}{match.group(2).rstrip()}\n"
            
            # Check if we are actually changing anything (for logging)
            old_id_match = re.search(rf"{re.escape(prefix)}-\d+", line)
            old_id = old_id_match.group(0) if old_id_match else "UNKNOWN"
            
            if old_id != new_id:
                print(f"  - Renumbering: {old_id} -> {new_id}")
                changed_count += 1
            
            new_lines.append(new_line)
            counter += 1
        else:
            new_lines.append(line)

    print(f"\nTotal records processed: {counter - 1}")
    print(f"Total IDs modified:      {changed_count}")

    if not dry_run:
        # INLINE MODIFICATION: Overwrite the original file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"\nSuccess! File '{os.path.basename(file_path)}' has been updated inline.")
        except IOError as e:
            print(f"\nError writing to file: {e}")
    else:
        print("\n[Dry Run] No changes were applied to the file.")

def main():
    parser = argparse.ArgumentParser(description="Renumber ADRs in the sibling 'adr' directory inline.")
    
    # Positional argument: Prefix only (e.g., OCP-BM)
    parser.add_argument("prefix", help="The ADR prefix (e.g., OCP-BM). Assumes filename is OCP-BM.md")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without overwriting the file")

    args = parser.parse_args()

    # --- Path Resolution Logic ---
    # 1. Get the absolute path of this script file
    script_location = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Navigate up one level (to project root), then down into 'adr'
    adr_directory = os.path.normpath(os.path.join(script_location, "..", "adr"))
    
    # 3. Construct the expected filename (Prefix + .md)
    target_filename = f"{args.prefix}.md"
    full_file_path = os.path.join(adr_directory, target_filename)

    # Run the renumbering function
    renumber_adrs(full_file_path, args.prefix, args.dry_run)

if __name__ == "__main__":
    main()