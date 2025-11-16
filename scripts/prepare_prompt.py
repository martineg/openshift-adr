#!/usr/bin/env python3
import re
import sys
import argparse
from pathlib import Path

# --- Configuration (Relative to project root) ---
ADR_DIRECTORY = "adr"
PROMPT_DIRECTORY = "prompts"
DICT_DIRECTORY = "dictionaries"
DOC_MAPPING_FILENAME = "adr_doc_prefix_mapping.md"
CREATE_LOAD_TEMPLATE = "template-adr-create-load.md"  # <-- NEW
CREATE_EXEC_TEMPLATE = "adr-create.md"            # <-- NEW
CHAR_LIMIT = 1950
WRAPPER_ESTIMATE = 200 # Increased buffer for multi-part prompts
SAFE_CHUNK_LIMIT = CHAR_LIMIT - WRAPPER_ESTIMATE

# --- "LOAD" Prompt Wrappers (for UPDATE) ---
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
    chunks = []
    current_chunk_lines = []
    current_chunk_char_count = 0
    for line in text.split('\n'):
        line_len = len(line) + 1
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
    try:
        script_path = Path(__file__).resolve()
        return script_path.parent.parent
    except NameError:
        return Path.cwd()

def read_file(file_path: Path) -> str:
    if not file_path.exists():
        print(f"Error: File not found at '{file_path}'", file=sys.stderr)
        sys.exit(1)
    try:
        return file_path.read_text()
    except Exception as e:
        print(f"Error: Could not read file {file_path}: {e}", file=sys.stderr)
        sys.exit(1)

def parse_doc_mapping(content: str, target_prefix: str) -> (list, list):
    source_of_truth_files = []
    all_prefixes = set()
    
    # **BUG FIX**: Iterate all lines, but add checks for header/junk
    lines = content.split('\n')
    for line in lines:
        if not line.strip() or not line.startswith('|'):
            continue
        
        parts = [col.strip() for col in line.strip('|').split('|')]
        if len(parts) < 2:
            continue
            
        doc_file, prefixes_in_row_str = parts[0], parts[1]

        # **BUG FIX**: Skip header, separator, or empty rows
        if doc_file.lower() == "documentation file" or doc_file.startswith(':'):
            continue
            
        prefixes_in_row = [p.strip() for p in prefixes_in_row_str.split(',')]
        
        for prefix in prefixes_in_row:
            if not prefix or prefix.lower() == 'id_ad_prefix' or prefix.startswith(':'):
                continue
                
            all_prefixes.add(f"{prefix}-") # Add to the "baseline" list
            
            if prefix == target_prefix:
                source_of_truth_files.append(f"- `{doc_file}`")
                
    return sorted(source_of_truth_files), sorted(list(all_prefixes))

def get_next_adr_id(adr_file_content: str, prefix_with_dash: str) -> str:
    pattern = re.compile(r"^\#\#\s*{prefix}(\d+)".format(prefix=re.escape(prefix_with_dash)),
                         re.MULTILINE | re.IGNORECASE)
    ids = [int(match.group(1)) for match in pattern.finditer(adr_file_content)]
    if not ids:
        return "01"
    next_id = max(ids) + 1
    return f"{next_id:02d}" # Format as two digits

# --- NEW 'CREATE' WORKFLOW FUNCTION ---
def handle_create_prompt(project_root: Path, prefix_base: str):
    """Generates a two-part conversational 'CREATE' prompt."""
    
    load_template_path = project_root / PROMPT_DIRECTORY / CREATE_LOAD_TEMPLATE
    exec_template_path = project_root / PROMPT_DIRECTORY / CREATE_EXEC_TEMPLATE
    mapping_file_path = project_root / DICT_DIRECTORY / DOC_MAPPING_FILENAME
    adr_file_path = project_root / ADR_DIRECTORY / f"{prefix_base}.md"

    load_template_content = read_file(load_template_path)
    exec_template_content = read_file(exec_template_path)
    mapping_content = read_file(mapping_file_path)
    
    adr_file_content = ""
    if adr_file_path.exists():
        adr_file_content = adr_file_path.read_text()
    
    prefix_with_dash = f"{prefix_base}-"
    
    # 1. Get data from helper functions
    source_files, baseline_prefixes = parse_doc_mapping(mapping_content, prefix_base)
    next_id = get_next_adr_id(adr_file_content, prefix_with_dash)
    
    source_file_list_str = '\n'.join(source_files) or "N/A (Using all sources)"
    baseline_prefix_list_str = '`' + '`, `'.join(baseline_prefixes) + '`'

    # 2. Generate Prompt 1 (LOAD) - This is the long one
    prompt1_load_content = f"**1. Your Source of Truth (FOCUSED FILE LIST):**\n" \
                           f"Your analysis must be based **ONLY** on the following document(s):\n" \
                           f"{source_file_list_str}\n\n" \
                           f"**2. Baseline ADRs (DO NOT DUPLICATE):**\n" \
                           f"You must check against the following list of *all existing ADR prefixes*. Do not suggest topics that are already covered by these prefixes.\n" \
                           f"{baseline_prefix_list_str}"
    
    # 3. Generate Prompt 2 (EXECUTE)
    prompt2_execute = exec_template_content.format(
        PREFIX_DASH=prefix_with_dash,
        NEXT_ADR_ID=next_id
    )

    # 4. Print the two-part conversation
    print(f"# --- START OF 'CREATE' WORKFLOW FOR {prefix_base} ---")
    print(f"# This is a 2-step process. Run Prompt 1, then run Prompt 2.\n")
    
    # --- Check length of Prompt 1 and split if needed ---
    if len(prompt1_load_content) + WRAPPER_ESTIMATE <= CHAR_LIMIT:
        # It fits in one prompt
        final_prompt1 = load_template_content.format(ADR_FULL_TEXT=prompt1_load_content)
        print(f"# --- PROMPT 1: LOAD CONTEXT (1 part) ---")
        print(final_prompt1.strip())
        print(f"# --- END OF PROMPT 1 ---")
    else:
        # It's too long, split it
        print(f"# --- NOTE: 'CREATE' CONTEXT IS TOO LONG. SPLITTING INTO MULTIPLE PROMPTS... ---")
        chunks = split_text_into_chunks(prompt1_load_content, SAFE_CHUNK_LIMIT)
        total_chunks = len(chunks)
        
        for part_num, chunk_content in enumerate(chunks, 1):
            next_part = part_num + 1
            if part_num == 1:
                final_prompt = PROMPT_MULTI_START.format(total=total_chunks, ADR_FULL_TEXT=chunk_content)
            elif part_num == total_chunks:
                final_prompt = PROMPT_MULTI_END.format(part_num=part_num, total=total_chunks, ADR_FULL_TEXT=chunk_content)
            else:
                final_prompt = PROMPT_MULTI_PART.format(part_num=part_num, total=total_chunks, next_part=next_part, ADR_FULL_TEXT=chunk_content)
            
            print(f"# --- START OF PROMPT 1 (Part {part_num}/{total_chunks}) ---")
            print(final_prompt.strip())
            print(f"# --- END OF PROMPT 1 (Part {part_num}/{total_chunks}) ---")

    print(f"\n# --- PROMPT 2: EXECUTE TASK ---")
    print(f"# (Run this prompt *after* the context above is fully loaded)\n")
    print(prompt2_execute.strip())
    print(f"# --- END OF 'CREATE' WORKFLOW ---")


# --- This function (handle_review_update_prompts) is unchanged ---
def handle_review_update_prompts(project_root: Path, target: str):
    """Generates one or more 'LOAD' prompts for the 'REVIEW/UPDATE' workflow."""
    
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
    adr_content = read_file(filename_path)

    pattern = re.compile(search_pattern_str, re.MULTILINE | re.IGNORECASE)
    matches = list(pattern.finditer(adr_content))
    
    if not matches:
        print(f"Error: No ADRs matching '{target}' found in {filename_str}.", file=sys.stderr)
        sys.exit(1)
        
    print(f"Found {len(matches)} ADR(s) in {filename_str}. Generating 'LOAD' prompts...\n")

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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage (run from project root '~/workspace/adr'):

  To CREATE new ADRs for OCP-BM:
  ./scripts/prepare_prompt.py --create OCP-BM

  To REVIEW all ADRs for OCP-BM:
  ./scripts/prepare_prompt.py --review-update OCP-BM
  
  To REVIEW a single ADR:
  ./scripts/prepare_prompt.py --review-update OCP-BM-01
"""
    )
    
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
        if re.match(r'^(.+)-(\d+)$', args.target):
            print(f"Error: --create requires a base prefix (e.g., GITOPS), not a specific ID (e.g., GITOPS-01).", file=sys.stderr)
            sys.exit(1)
        handle_create_prompt(project_root, args.target)
        
    elif args.review_update:
        handle_review_update_prompts(project_root, args.target)

if __name__ == "__main__":
    main_parser()