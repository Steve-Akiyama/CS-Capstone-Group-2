import re

# Define input file path
input_file = "textbook.txt"  # Ensure this file exists in your directory

# Read the textbook content
with open(input_file, "r", encoding="utf-8") as f:
    text = f.read()

# Regex pattern to detect section headers (e.g., "2.1 Why Is Research Important?")
pattern = r"(\d+\.\d+)\s+([^\n]+)\nLEARNING OBJECTIVES\n"

# Find all matches (section headers)
matches = list(re.finditer(pattern, text))

# Chunk the textbook based on identified sections
chunks = []
for i, match in enumerate(matches):
    section_num = match.group(1)  # e.g., "2.1" (number)
    section_title = match.group(2)  # e.g., "Why Is Research Important?"

    # Find start and end index of each section
    start_idx = match.end()
    end_idx = matches[i + 1].start() if i + 1 < len(matches) else len(text)

    # Extract the section content
    section_content = text[start_idx:end_idx].strip()

    # Store chunked data with labeled chunks
    chunks.append((f"Chunk {i+1}", section_num, section_title, section_content))

# Function to create three sub-chunks for each main chunk
def split_into_subchunks(content, num_subchunks=3):
    sentences = content.split(". ")  # Split into sentences
    chunk_size = max(1, len(sentences) // num_subchunks)  # Ensure at least one sentence per chunk
    subchunks = [" ".join(sentences[i * chunk_size:(i + 1) * chunk_size]) for i in range(num_subchunks - 1)]
    subchunks.append(" ".join(sentences[(num_subchunks - 1) * chunk_size:]))  # Last subchunk gets the remainder
    return subchunks

# Print the chunked output in the terminal with labels and sub-chunks
for chunk_label, section_num, section_title, content in chunks:
    print(f"{chunk_label}: {section_num} {section_title}\n")

    # Split each chunk into three sub-chunks
    subchunks = split_into_subchunks(content, 10)
    for j, subchunk in enumerate(subchunks, 1):
        print(f"  Sub-chunk {j}:\n  {subchunk.strip()}\n")

    print("\n" + "=" * 80 + "\n")  # Separator for clarity
# say split into 250 words say if the c