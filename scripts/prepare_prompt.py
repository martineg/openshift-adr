#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path

# --- Configuration (Relative to project root) ---
ADR_DIRECTORY = "adr"
PROMPT_DIRECTORY = "prompts"
CHAR_LIMIT = 1950  # A safe buffer below 2000

# --- Prompt "Wrapper" Text (Internalized) ---
WRAPPER_ESTIMATE = 150 
SAFE_CHUNK_LIMIT = CHAR_LIMIT - WRAPPER_ESTIMATE

PROMPT_SINGLE = """
Please read and remember the following Architecture Decision Record text.
**Respond ONLY with "Confirmed. ADR loaded."**
---
{ADR_FULL_TEXT}
---
"""

PROMPT_MULTI_START = """
Please read and remember the following text. It is **Part 1/{total}** of a single Architecture Decision.
**Respond ONLY with "Confirmed. Ready for Part 2."**
---
{ADR_FULL_TEXT}
---
"""

PROMPT_MULTI_PART = """
Here is **Part {part_num}/{total}** of the Architecture Decision. Please read it.
**Respond ONLY with "Confirmed. Ready for Part {next_part}."**
---
{ADR_FULL_TEXT}
---
"""

PROMPT_MULTI_END = """
Here is the **final Part {part_num}/{total}** of the Architecture Decision. Please read it.
**Respond ONLY with "Confirmed. ADR loaded."**
---
{ADR_FULL_TEXT}
---
"""

def split_text_into_chunks(text, max_length):
    """
    Splits a large text into smaller chunks under max_length,
    respecting line breaks.
    """
    chunks = []
    current_chunk_lines = []
    current_chunk_char_count = 0
    
    for line in text.split('\n'):
        line_len = len(line) + 1  # +1 for the newline char

        if (current_chunk_char_count + line_len > max_length) and current_chunk_lines:
            chunks.append('\n'.join(current_chunk_lines))
            current_chunk_lines = [line]
            current_chunk_char_count = line_len
        else:
            current_chunk_lines.append(line)
            current_chunk_char_count += line_len
            
    if current_chunk_lines:
        chunks.append('\n'.join(current_chunk_lines))
        
    return chunks

def get_project_root():
    """Finds the project root directory."""
    try:
        script_path = Path(__file__).resolve()
        return script_path.parent.parent
    except NameError:
        return Path.cwd()

def read_file(file_path: Path) -> str:
    """Reads a file and exits on error."""
    if not file_path.exists():
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    try:
        return file_path.read_text()
    except Exception as e:
        print(f"Error: Could not read file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def handle_create_prompt(project_root: Path, prefix_base: str):
    """Generates the 'CREATE' prompt."""
    prompt_template_path = project_root / PROMPT_DIRECTORY / "adr-create.md"
    prompt_template_content = read_file(prompt_template_path)
    
    prefix_with_dash = f"{prefix_base}-"
    
    # Replace the [PREFIX] placeholder
    final_prompt = prompt_template_content.replace("[PREFIX]", prefix_base)
    
    # Also replace the specific [PREFIX]- in the ID rule for clarity
    final_prompt = final_prompt.replace(f"{prefix_base}-", prefix_with_dash)
    
    print(f"# --- START OF 'CREATE' PROMPT FOR {prefix_base} ---")
    print(final_prompt.strip())
    print(f"# --- END OF 'CREATE' PROMPT ---")

def handle_review_update_prompts(project_root: Path, target: str):
    """Generates one or more 'LOAD' prompts for the 'REVIEW/UPDATE' workflow."""
    
    # --- Logic to Distinguish Prefix from ID ---
    id_pattern = re.compile(r'^(.+)-(\d+)$')
    id_match = id_pattern.match(target)
    
    if id_match:
        prefix_base = id_match.group(1)
        filename_str = f"{prefix_base}.md"
        search_pattern_str = r"^\#\#\s*({target_id})\b".format(target_id=re.escape(target))
    else:
        prefix_base = target
        filename_str = f"{prefix_base}.md"
        prefix_for_regex = f"{prefix_base}-"
        search_pattern_str = r"^\#\#\s*({prefix_dash}\S+)".format(prefix_dash=re.escape(prefix_for_regex))
    
    filename_path = project_root / ADR_DIRECTORY / filename_str

    # --- Read ADR File ---
    adr_content = read_file(filename_path)

    # --- Regex Logic to find ADRs ---
    pattern = re.compile(search_pattern_str, re.MULTILINE | re.IGNORECASE)
    matches = list(pattern.finditer(adr_content))
    
    if not matches:
        print(f"Error: No ADRs matching '{target}' found in {filename_str}.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(matches)} ADR(s) in {filename_str}. Generating 'LOAD' prompts...\n")

    # --- Iterate through matches and slice the content ---
    for i, current_match in enumerate(matches):
        start_index = current_match.start()
        
        end_index = len(adr_content)
        next_match_start = -1
        if i + 1 < len(matches):
             next_match_start = matches[i+1].start()
        
        if id_match:
            all_adr_pattern = re.compile(r"^\#\#\s*([A-Z]+(?:-[A-Z]+)?-\d+)", re.MULTILINE | re.IGNORECASE)
            all_matches_in_file = list(all_adr_pattern.finditer(adr_content))
            for j, match_in_file in enumerate(all_matches_in_file):
                if match_in_file.start() == start_index and j + 1 < len(all_matches_in_file):
                    end_index = all_matches_in_file[j+1].start()
                    break
            else: 
                end_index = len(adr_content)
        elif next_match_start != -1:
             end_index = next_match_start
            
        adr_full_text_raw = adr_content[start_index:end_index]
        adr_text_cleaned = adr_full_text_raw.split("\n---\n")[0].strip()
        
        ad_id_match = re.search(r"^\#\#\s*(\S+)", adr_text_cleaned)
        ad_id = ad_id_match.group(1) if ad_id_match else "UNKNOWN_ADR"

        # --- Check Length and Generate Prompt(s) ---
        if len(adr_text_cleaned) + WRAPPER_ESTIMATE <= CHAR_LIMIT:
            final_prompt = PROMPT_SINGLE.format(ADR_FULL_TEXT=adr_text_cleaned)
            print(f"# --- START OF PROMPT FOR {ad_id} (1 part) ---")
            print(final_prompt.strip())
            print(f"# --- END OF PROMPT FOR {ad_id} ---\n# (Copy/paste, get confirmation, then use 'prompts/adr-update-review.md')\n")
        
        else:
            print(f"# --- NOTE: ADR '{ad_id}' IS TOO LONG. SPLITTING INTO MULTIPLE PROMPTS... ---")
            chunks = split_text_into_chunks(adr_text_cleaned, SAFE_CHUNK_LIMIT)
            total_chunks = len(chunks)
            
            for part_num, chunk_content in enumerate(chunks, 1):
                next_part = part_num + 1
                if part_num == 1:
                    final_prompt = PROMPT_MULTI_START.format(total=total_chunks, ADR_FULL_TEXT=chunk_content)
                elif part_num == total_chunks:
                    final_prompt = PROMPT_MULTI_END.format(part_num=part_num, total=total_chunks, ADR_FULL_TEXT=chunk_content)
                else:
                    final_prompt = PROMPT_MULTI_PART.format(part_num=part_num, total=total_chunks, next_part=next_part, ADR_FULL_TEXT=chunk_content)
                
                if len(final_prompt) > CHAR_LIMIT:
                     print(f"# !!!!!!!!! WARNING: CHUNK {part_num}/{total_chunks} FOR {ad_id} IS STILL TOO LONG. MANUAL REVIEW NEEDED. !!!!!!!!!")
                
                print(f"# --- START OF PROMPT FOR {ad_id} (Part {part_num}/{total_chunks}) ---")
                print(final_prompt.strip())
                print(f"# --- END OF PROMPT FOR {ad_id} (Part {part_num}/{total_chunks}) ---")

            print(f"# --- ALL PARTS FOR {ad_id} GENERATED. ---\n# (Copy/paste ALL parts in order, THEN use 'prompts/adr-update-review.md')\n")

def main_parser():
    parser = argparse.ArgumentParser(
        description="Generate NotebookLM prompts for ADR maintenance.",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create a mutually exclusive group for --create and --review-update
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--create",
        action="store_true",
        help="Generate the 'CREATE' prompt for a given prefix."
    )
    action_group.add_argument(
        "--review-update",
        action="store_true",
        help="Generate the 'LOAD' prompt(s) for the 'REVIEW/UPDATE' workflow."
    )
    
    parser.add_argument(
        "target",
        type=str,
        help="The base prefix (e.g., OCP-BM) or a specific ADR ID (e.g., OCP-BM-01)"
    )
    
    args = parser.parse_args()
    project_root = get_project_root()
    
    if args.create:
        # --- Handle CREATE ---
        # Check if target looks like a full ID, which is not allowed for --create
        if re.match(r'^(.+)-(\d+)$', args.target):
            print(f"Error: --create requires a base prefix (e.g., GITOPS), not a specific ID (e.g., GITOPS-01).", file=sys.stderr)
            sys.exit(1)
        handle_create_prompt(project_root, args.target)
        
    elif args.review_update:
        # --- Handle REVIEW/UPDATE ---
        handle_review_update_prompts(project_root, args.target)

if __name__ == "__main__":
    main_parser()