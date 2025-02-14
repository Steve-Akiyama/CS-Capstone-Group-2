import fitz  # PyMuPDF
import os
import re

pdf_path = "textbook.pdf"
output_dir = "textbook_chunks"

# Create output directory if not exists
os.makedirs(output_dir, exist_ok=True)

# Open PDF
doc = fitz.open(pdf_path)

# Get bookmarks (table of contents)
bookmarks = doc.get_toc()

# Dictionary to store chunks by chapter and sub-chapter
chunks = {}
current_chapter = None  # Track the last seen chapter

# Function to clean titles for filenames
def clean_filename(title):
    return re.sub(r'[^\w\s.-]', '', title).replace(" ", "_")

# Iterate through bookmarks and extract text
for i, (level, title, page) in enumerate(bookmarks):
    next_page = bookmarks[i + 1][2] if i + 1 < len(bookmarks) else len(doc)

    # Extract text from this section
    text = "\n".join([doc[pg].get_text("text") for pg in range(page - 1, next_page - 1) if doc[pg].get_text()])
    
    # Clean title for dictionary key and filename
    safe_title = clean_filename(title)

    if level == 1:  # Main chapter
        chunks[safe_title] = {'text': text, 'subsections': {}}
        current_chapter = safe_title  # Update the last seen chapter
        file_path = os.path.join(output_dir, f"{safe_title}.txt")
        
        # Save chapter text to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        
    elif level > 1:  # Sub-chapter
        if current_chapter is None:
            # If there's no main chapter, treat it as a standalone entry
            chunks[safe_title] = {'text': text, 'subsections': {}}
            file_path = os.path.join(output_dir, f"{safe_title}.txt")
        else:
            # Store under the last seen chapter
            chunks[current_chapter]['subsections'][safe_title] = text
            file_path = os.path.join(output_dir, f"{current_chapter}_{safe_title}.txt")

        # Save sub-chapter text to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)

# Search function to look up specific sections
def search_section(section_title):
    results = {title: content for title, content in chunks.items() if section_title.lower() in title.lower()}
    if results:
        for title, content in results.items():
            print(f"\n📖 Section: {title}\n")
            print(content['text'][:1000])  # Print first 1000 characters to avoid overwhelming output
            print("\n--- [Truncated] ---\n")
            if content['subsections']:
                print("Sub-sections:")
                for sub_title in content['subsections']:
                    print(f"  - {sub_title}")
    else:
        print(" Section not found. Try another title.")

# Example usage:
while True:
    query = input("\nEnter section title to search (or 'exit' to quit): ")
    if query.lower() == 'exit':
        break
    search_section(query)

print("\n Extraction Complete: All sections saved in 'textbook_chunks' folder.")
