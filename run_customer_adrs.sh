#!/bin/bash
#
# Interactive wrapper for customer_adrs.py
# Checks prerequisites and provides interactive product selection
#
# Usage:
#   ./run_customer_adrs.sh                    # Interactive generate mode
#   ./run_customer_adrs.sh generate           # Interactive generate mode
#   ./run_customer_adrs.sh check <input>      # Check completion (directory or URL)
#   ./run_customer_adrs.sh export <input>     # Export to file (from directory or URL)
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Get subcommand (default to generate)
SUBCOMMAND="${1:-generate}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored message
print_error() { echo -e "${RED}❌ $1${NC}"; }
print_success() { echo -e "${GREEN}✅ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
print_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }

echo "================================================================================"
echo "  Customer ADR Workflow - Interactive Setup"
echo "================================================================================"
echo ""

# Check 1: Python version
print_info "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed"
    echo "  Install Python 3.7 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 7 ]); then
    print_error "Python version $PYTHON_VERSION is too old"
    echo "  Required: Python 3.7 or higher"
    exit 1
fi

print_success "Python $PYTHON_VERSION detected"

# Check 2: PyYAML dependency
print_info "Checking PyYAML dependency..."
if ! python3 -c "import yaml" 2>/dev/null; then
    print_warning "PyYAML is not installed"
    echo ""
    read -p "  Install PyYAML now? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "  Installing PyYAML..."
        pip3 install PyYAML || pip install PyYAML
        print_success "PyYAML installed"
    else
        print_error "PyYAML is required. Install with: pip install PyYAML"
        exit 1
    fi
else
    print_success "PyYAML installed"
fi

# Check 3: Repository location
print_info "Checking repository structure..."
if [ ! -d "adr_templates" ]; then
    print_error "adr_templates/ directory not found"
    echo "  This script must be run from the repository root"
    exit 1
fi

if [ ! -f "scripts/customer_adrs.py" ]; then
    print_error "scripts/customer_adrs.py not found"
    echo "  This script must be run from the repository root"
    exit 1
fi

print_success "Repository structure verified"

# If not generate subcommand, just pass through to Python script
if [ "$SUBCOMMAND" != "generate" ]; then
    print_info "Running subcommand: $SUBCOMMAND"
    echo ""

    # Check Google API credentials for export
    if [ "$SUBCOMMAND" = "export" ]; then
        if [ ! -f "credentials.json" ]; then
            print_warning "credentials.json not found (required for Google Docs export)"
            echo "  See: https://developers.google.com/workspace/guides/create-credentials"
        fi

        # Check google-api-python-client
        if ! python3 -c "import googleapiclient" 2>/dev/null; then
            print_warning "google-api-python-client not installed"
            echo ""
            read -p "  Install google-api-python-client now? [y/N] " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                pip3 install google-api-python-client google-auth-httplib2 google-auth-oauthlib
                print_success "Google API client installed"
            else
                print_error "google-api-python-client is required for export"
                exit 1
            fi
        fi
    fi

    # Transform arguments for check/export commands
    # check <input> -> check --input <input>
    # export <input> -> export --input <input>
    if [ "$SUBCOMMAND" = "check" ] || [ "$SUBCOMMAND" = "export" ]; then
        if [ -n "$2" ]; then
            exec python3 scripts/customer_adrs.py "$SUBCOMMAND" --input "$2" "${@:3}"
        else
            exec python3 scripts/customer_adrs.py "$@"
        fi
    else
        # Pass all arguments as-is for other subcommands
        exec python3 scripts/customer_adrs.py "$@"
    fi
fi

# Continue with interactive generate mode
echo ""
echo "================================================================================"
echo "  Interactive Product Selection"
echo "================================================================================"
echo ""

# Get available products from adr_templates/
PRODUCTS=($(ls -1 adr_templates/*.md | xargs -n 1 basename | sed 's/\.md$//' | sort))

if [ ${#PRODUCTS[@]} -eq 0 ]; then
    print_error "No ADR templates found in adr_templates/"
    exit 1
fi

# Product name lookup — delegates to scripts/products.py (single source of truth).
# Falls back to the prefix itself if Python/config is unavailable.
get_product_name() {
    python3 -c "import sys; sys.path.insert(0, 'scripts'); from products import short_name; print(short_name('$1'))" 2>/dev/null \
        || echo "$1"
}

# Function to display product list with selection markers
display_products() {
    clear
    echo "================================================================================"
    echo "  Interactive Product Selection"
    echo "================================================================================"
    echo ""
    echo "Available ADR templates:"
    echo ""

    for i in "${!PRODUCTS[@]}"; do
        product="${PRODUCTS[$i]}"
        product_name="$(get_product_name "$product")"
        template_file="adr_templates/${product}.md"
        count=$(grep -c "^## ${product}-" "$template_file" 2>/dev/null || echo "0")

        # Check if product is selected
        marker="[ ]"
        for selected in "${SELECTED_INDICES[@]}"; do
            if [ "$selected" == "$i" ]; then
                marker="[X]"
                break
            fi
        done

        printf "  %2d) %s %-15s - %-45s (%2s ADRs)\n" $((i+1)) "$marker" "$product" "$product_name" "$count"
    done

    echo ""
    echo "================================================================================"
    echo ""

    if [ ${#SELECTED_INDICES[@]} -gt 0 ]; then
        echo -e "${GREEN}Selected: ${#SELECTED_INDICES[@]} product(s)${NC}"
        echo ""
    fi
}

# Initialize selected indices array
SELECTED_INDICES=()

# Interactive selection loop
while true; do
    display_products

    read -p "Select product number(s) [e.g., '5' or '5 10 17'] (or ENTER to continue): " SELECTION

    # If empty, break the loop
    if [ -z "$SELECTION" ]; then
        if [ ${#SELECTED_INDICES[@]} -eq 0 ]; then
            print_error "No products selected"
            echo ""
            read -p "Press ENTER to try again..."
            continue
        fi
        break
    fi

    # Special case: 'all' selects all products
    if [[ "$SELECTION" == "all" ]] || [[ "$SELECTION" == "ALL" ]]; then
        SELECTED_INDICES=()
        for i in "${!PRODUCTS[@]}"; do
            SELECTED_INDICES+=("$i")
        done
        continue
    fi

    # Process space-separated numbers (e.g., "5 10 17")
    for num in $SELECTION; do
        # Validate each number
        if ! [[ "$num" =~ ^[0-9]+$ ]]; then
            print_error "Invalid input: '$num' is not a number"
            sleep 1
            continue 2  # Continue outer loop
        fi

        # Convert to array index (1-based to 0-based)
        index=$((num - 1))

        # Validate range
        if [ $index -lt 0 ] || [ $index -ge ${#PRODUCTS[@]} ]; then
            print_error "Invalid selection: $num (out of range 1-${#PRODUCTS[@]})"
            sleep 1
            continue 2  # Continue outer loop
        fi

        # Toggle selection
        already_selected=false
        new_indices=()
        for selected in "${SELECTED_INDICES[@]}"; do
            if [ "$selected" == "$index" ]; then
                already_selected=true
                # Don't add it (deselect)
            else
                new_indices+=("$selected")
            fi
        done

        if [ "$already_selected" = false ]; then
            # Add to selection
            new_indices+=("$index")
        fi

        SELECTED_INDICES=("${new_indices[@]}")
    done
done

# Build selected products array and calculate totals
SELECTED_PRODUCTS=()
TOTAL_ADRS=0

# Sort indices for display
IFS=$'\n' SORTED_INDICES=($(sort -n <<<"${SELECTED_INDICES[*]}"))
unset IFS

for index in "${SORTED_INDICES[@]}"; do
    product="${PRODUCTS[$index]}"
    SELECTED_PRODUCTS+=("$product")

    template_file="adr_templates/${product}.md"
    count=$(grep -c "^## ${product}-" "$template_file" 2>/dev/null || echo "0")
    TOTAL_ADRS=$((TOTAL_ADRS + count))
done

# Display final selection
clear
echo "================================================================================"
echo "  Selected Products"
echo "================================================================================"
echo ""
print_success "You have selected ${#SELECTED_PRODUCTS[@]} product(s):"
echo ""
for product in "${SELECTED_PRODUCTS[@]}"; do
    product_name="$(get_product_name "$product")"
    template_file="adr_templates/${product}.md"
    count=$(grep -c "^## ${product}-" "$template_file" 2>/dev/null || echo "0")
    printf "  - %-15s (%s) - %2s ADRs\n" "$product" "$product_name" "$count"
done
echo ""
echo "  Total ADRs: $TOTAL_ADRS"

# Build product list for command
PRODUCT_LIST=$(IFS=,; echo "${SELECTED_PRODUCTS[*]}")

echo ""
echo "================================================================================"
echo "  Customer Information"
echo "================================================================================"
echo ""

# Get customer name
read -p "Customer organization name: " CUSTOMER_NAME

if [ -z "$CUSTOMER_NAME" ]; then
    print_error "Customer name is required"
    exit 1
fi

# Get engagement date (optional)
read -p "Engagement date [YYYY-MM-DD] (default: today): " ENGAGEMENT_DATE

# Get architect name (optional)
GIT_USER=$(git config user.name 2>/dev/null || echo "")
if [ -n "$GIT_USER" ]; then
    read -p "Architect name (default: $GIT_USER): " ARCHITECT_NAME
    ARCHITECT_NAME=${ARCHITECT_NAME:-$GIT_USER}
else
    read -p "Architect name: " ARCHITECT_NAME
fi

# Get output directory (optional)
CUSTOMER_SLUG=$(echo "$CUSTOMER_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//;s/-$//')
DEFAULT_OUTPUT="./${CUSTOMER_SLUG}-ADRs"
read -p "Output directory (default: $DEFAULT_OUTPUT): " OUTPUT_DIR
OUTPUT_DIR=${OUTPUT_DIR:-$DEFAULT_OUTPUT}

# Check if output directory exists
if [ -d "$OUTPUT_DIR" ]; then
    echo ""
    print_warning "Output directory already exists: $OUTPUT_DIR"
    read -p "Overwrite existing directory? [y/N] " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Operation cancelled"
        exit 1
    fi
    FORCE_FLAG="--force"
else
    FORCE_FLAG=""
fi

echo ""
echo "================================================================================"
echo "  Summary"
echo "================================================================================"
echo ""
echo "  Customer:        $CUSTOMER_NAME"
echo "  Products:        ${SELECTED_PRODUCTS[*]}"
echo "  Total ADRs:      $TOTAL_ADRS"
if [ -n "$ENGAGEMENT_DATE" ]; then
echo "  Engagement Date: $ENGAGEMENT_DATE"
fi
if [ -n "$ARCHITECT_NAME" ]; then
echo "  Architect:       $ARCHITECT_NAME"
fi
echo "  Output:          $OUTPUT_DIR"
echo ""

read -p "Proceed with generation? [Y/n] " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]] && [[ ! -z $REPLY ]]; then
    print_error "Operation cancelled"
    exit 1
fi

echo ""
echo "================================================================================"
echo "  Generating ADR Pack..."
echo "================================================================================"
echo ""

# Build command
CMD="python3 scripts/customer_adrs.py generate --customer \"$CUSTOMER_NAME\" --products \"$PRODUCT_LIST\" --output \"$OUTPUT_DIR\""

if [ -n "$ENGAGEMENT_DATE" ]; then
    CMD="$CMD --engagement-date \"$ENGAGEMENT_DATE\""
fi

if [ -n "$ARCHITECT_NAME" ]; then
    CMD="$CMD --architect \"$ARCHITECT_NAME\""
fi

if [ -n "$FORCE_FLAG" ]; then
    CMD="$CMD $FORCE_FLAG"
fi

# Execute command
eval $CMD

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    # Success - Python script already printed mode-specific instructions
    # (Google Docs mode: URL + navigation, Local mode: directory + export)
    :
else
    print_error "ADR pack generation failed (exit code: $EXIT_CODE)"
    exit $EXIT_CODE
fi
