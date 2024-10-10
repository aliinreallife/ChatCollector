import argparse

from utils import (
    deduplicate_messages,
    extract_messages,
    fetch_content_from_url,
    sort_messages_by_time,
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

    # Extract the part after the last "/" from the sharable link to use as the filename
    output_filename = f"{sharable_link.split('/')[-1]}.md"

    content = fetch_content_from_url(sharable_link)

    pattern = r'"message":\{.*?"author":\{"role":"(.*?)".*?"create_time":([0-9.]+).*?"parts":\s*\[(.*?)\]'

    # Extract and process the data
    matches = extract_messages(content, pattern)
    deduplicated_data = deduplicate_messages(matches)
    sorted_data = sort_messages_by_time(deduplicated_data)
    output_file_path = write_to_md_file(sorted_data, output_filename)

    print(f"Sorted and deduplicated content has been saved to {output_file_path}")


if __name__ == "__main__":
    main()
