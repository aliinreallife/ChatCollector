import re

raw_html_path = "raw_html.txt"

with open(raw_html_path, "r", encoding="utf-8") as file:
    content = file.read()

# Define the regex pattern to strictly capture parts, author, and create_time under "message"
pattern = r'"message":\{.*?"author":\{"role":"(.*?)".*?"create_time":([0-9.]+).*?"parts":\s*\[(.*?)\]'

matches = re.findall(pattern, content, re.DOTALL)

# Store results in a dictionary to remove duplicates based on parts_content
unique_data = {}

for match in matches:
    author = match[0]  # Extract the author
    create_time = float(match[1])  # Extract create_time and convert to float
    parts_content = match[2].strip().strip('"').replace("\\n", "\n")

    if parts_content not in unique_data or create_time < unique_data[parts_content][1]:
        unique_data[parts_content] = (author, create_time)

sorted_data = sorted(unique_data.items(), key=lambda x: x[1][1])

output_file_path = "output.md"

with open(output_file_path, "w", encoding="utf-8") as md_file:
    for parts_content, (
        author,
        _,
    ) in sorted_data:  # Ignore create_time when writing to file
        if author == "assistant":
            md_file.write(f"**ChatGPT**:\n\n{parts_content}\n\n")
        else:
            md_file.write(f"**You**:\n\n{parts_content}\n\n")
        md_file.write("---\n\n")  # Separator for better readability

print(f"Sorted and deduplicated content has been saved to {output_file_path}")
