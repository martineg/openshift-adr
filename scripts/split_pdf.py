import os
import io
import argparse
from pypdf import PdfReader, PdfWriter

def _save_batch(pages, output_dir, base_name, part_number):
    """Helper function to write a list of page objects to a file."""
    output_filename = f"{base_name}_part_{part_number:03d}.pdf"
    output_path = os.path.join(output_dir, output_filename)
    
    writer = PdfWriter()
    for page in pages:
        writer.add_page(page)
    
    with open(output_path, "wb") as f:
        writer.write(f)
    
    # Get actual size for display
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Saved: {output_filename} ({size_mb:.2f} MB) - {len(pages)} pages")

def split_pdf_by_size(input_path, max_size_mb):
    # Convert MB to Bytes
    MAX_BYTES = max_size_mb * 1024 * 1024
    
    if not os.path.exists(input_path):
        print(f"Error: File not found at '{input_path}'")
        return

    # Create output directory based on filename
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_dir = f"{base_name}_split"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return
    
    print(f"Processing '{input_path}' ({total_pages} pages). Target size: <={max_size_mb}MB")

    current_batch = []
    part_number = 1

    for i, page in enumerate(reader.pages):
        # 1. Create a temporary writer to test the file size with the new page included
        temp_writer = PdfWriter()
        
        # Add all pages currently pending in the batch
        for batch_page in current_batch:
            temp_writer.add_page(batch_page)
        
        # Add the new candidate page
        temp_writer.add_page(page)

        # 2. Check the size of this combination in memory (without writing to disk yet)
        with io.BytesIO() as buffer:
            temp_writer.write(buffer)
            current_size = buffer.tell()

        # 3. Logic to decide whether to save or keep accumulating
        if current_size > MAX_BYTES:
            if len(current_batch) == 0:
                # EDGE CASE: A single page is larger than the limit. 
                # We must save it anyway to avoid dropping data.
                print(f"Warning: Page {i+1} alone is larger than {max_size_mb}MB. Saving as its own file.")
                current_batch.append(page)
                _save_batch(current_batch, output_dir, base_name, part_number)
                current_batch = []
                part_number += 1
            else:
                # The new page tipped it over the limit. 
                # Save the CURRENT batch (without the new page)
                _save_batch(current_batch, output_dir, base_name, part_number)
                part_number += 1
                
                # Start a new batch with the current page
                current_batch = [page]
        else:
            # Limit not reached, add page to batch and continue
            current_batch.append(page)
        
        # Simple progress indicator
        print(f"Processed page {i+1}/{total_pages}", end='\r')

    # 4. Save any remaining pages in the final batch
    if current_batch:
        _save_batch(current_batch, output_dir, base_name, part_number)

    print(f"\nDone! Files saved in directory: {output_dir}")

if __name__ == "__main__":
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="Split a PDF into smaller files based on size limit without breaking pages."
    )
    
    parser.add_argument(
        "pdf_path", 
        help="Path to the input PDF file"
    )
    
    parser.add_argument(
        "--size", 
        type=float, 
        default=2.0, 
        help="Maximum file size in MB (default: 2.0)"
    )

    args = parser.parse_args()

    split_pdf_by_size(args.pdf_path, args.size)