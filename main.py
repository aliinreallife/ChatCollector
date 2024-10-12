import argparse
import re
import sys
from utils import (
    deduplicate_messages,
    extract_messages,
    extract_title_from_response,
    fetch_content_from_url,
    sort_messages_by_time,
    validate_link,
    write_to_md_file,
)


def main():
    """Main function to fetch, process, and save conversation data."""
    parser = argparse.ArgumentParser(description="Process ChatGPT share link.")
    parser.add_argument(
        "--share-link", required=True, help="The ChatGPT share link to process"
    )
    args = parser.parse_args()

    sharable_link = args.share_link

    if not validate_link(sharable_link):
        print(f"Invalid share link format: {sharable_link}")
        return False

    try:
        content = fetch_content_from_url(sharable_link)
    except Exception as e:
        print(
            f"Error fetching content from the link: {sharable_link}. Error: {e}",
        )
        return False

    if content is None or len(content) == 0:
        print(
            f"Failed to fetch or empty content from the link: {sharable_link}",
        )
        return False
    pattern = r'"message":\{.*?"author":\{"role":"(.*?)".*?"create_time":([0-9.]+).*?"parts":\s*\[(.*?)\]'

    title = extract_title_from_response(content)
    # Extract and process the data
    matches = extract_messages(content, pattern)

    if not matches:
        print(
            f"Failed to extract messages from the content: {sharable_link}",
        )
        return False

    deduplicated_data = deduplicate_messages(matches)
    sorted_data = sort_messages_by_time(deduplicated_data)

    output_filename = f"{sharable_link.split('/')[-1]}.md"

    try:
        output_file_path = write_to_md_file(sorted_data, title, output_filename)
    except Exception as e:
        print(
            f"Error writing content to file: {output_filename}. Error: {e}",
        )
        return False

    print(f"Sorted and deduplicated content has been saved to {output_file_path}")
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
