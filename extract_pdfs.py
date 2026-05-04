import os
import glob
import pymupdf4llm

def extract_pdfs():
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    pdf_files = glob.glob(os.path.join(data_dir, "*.pdf"))
    
    for i, pdf_path in enumerate(pdf_files):
        print(f"Extracting {pdf_path}...")
        md_text = pymupdf4llm.to_markdown(pdf_path)
        
        # Save to sample_0{i+1}.md
        base_name = os.path.basename(pdf_path)
        md_path = os.path.join(data_dir, f"sample_{i+1:02d}.md")
        
        with open(md_path, "w", encoding="utf-8") as f:
            # We add a header indicating the original file for contextual prepend
            f.write(f"# Original Document: {base_name}\n\n")
            f.write(md_text)
            
        print(f"Saved to {md_path}")

if __name__ == "__main__":
    extract_pdfs()
