import re


def load_content(file_path):
    """Load the content from a file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def extract_messages(content, pattern):
    """Extract author, create_time, and parts_content using a regex pattern."""
    return re.findall(pattern, content, re.DOTALL)


def deduplicate_messages(matches):
    """Remove duplicates based on parts_content, keeping the earliest create_time."""
    unique_data = {}
    for match in matches:
        author = match[0]
        create_time = float(match[1])
        parts_content = match[2].strip().strip('"').replace("\\n", "\n")

        # Keep only the earliest entry by creation time
        if (
            parts_content not in unique_data
            or create_time < unique_data[parts_content][1]
        ):
            unique_data[parts_content] = (author, create_time)

    return unique_data


def sort_messages_by_time(deduplicated_data):
    """Sort the deduplicated messages by creation time."""
    return sorted(deduplicated_data.items(), key=lambda x: x[1][1])


def write_to_md_file(sorted_data, output_file_path):
    """Write the sorted data to a markdown file."""
    with open(output_file_path, "w", encoding="utf-8") as md_file:
        for parts_content, (author, _) in sorted_data:
            if author == "assistant":
                md_file.write(f"**ChatGPT**:\n\n{parts_content}\n\n")
            else:
                md_file.write(f"**You**:\n\n{parts_content}\n\n")
            md_file.write("---\n\n")


def main():
    # File paths
    raw_html_path = "raw_html.txt"
    output_file_path = "output.md"

    # Regex pattern
    pattern = r'"message":\{.*?"author":\{"role":"(.*?)".*?"create_time":([0-9.]+).*?"parts":\s*\[(.*?)\]'

    content = load_content(raw_html_path)
    matches = extract_messages(content, pattern)
    deduplicated_data = deduplicate_messages(matches)
    sorted_data = sort_messages_by_time(deduplicated_data)
    write_to_md_file(sorted_data, output_file_path)

    print(f"Sorted and deduplicated content has been saved to {output_file_path}")


# Run the script
if __name__ == "__main__":
    main()
