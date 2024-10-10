# main.py

from utils import (
    fetch_content_from_url,
    extract_messages,
    deduplicate_messages,
    sort_messages_by_time,
    write_to_md_file,
)


def main():
    """Main function to fetch, process, and save conversation data."""
    # Example sharable link (replace this with the actual link)
    sharable_link = "https://chatgpt.com/share/blahblahblah"
    output_file_path = "output.md"

    content = fetch_content_from_url(sharable_link)

    pattern = r'"message":\{.*?"author":\{"role":"(.*?)".*?"create_time":([0-9.]+).*?"parts":\s*\[(.*?)\]'

    # Extract and process the data
    matches = extract_messages(content, pattern)
    deduplicated_data = deduplicate_messages(matches)
    sorted_data = sort_messages_by_time(deduplicated_data)
    write_to_md_file(sorted_data, output_file_path)

    print(f"Sorted and deduplicated content has been saved to {output_file_path}")


# Run the script
if __name__ == "__main__":
    main()
