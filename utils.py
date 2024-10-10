import os
import re

import requests


def fetch_content_from_url(url):
    """Fetches HTML content from the given sharable URL.

    Args:
        url (str): The URL to fetch content from.

    Returns:
        str: The HTML content of the URL.

    Raises:
        requests.exceptions.RequestException: If the request to the URL fails.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        raise requests.exceptions.RequestException(
            f"Failed to fetch content from URL: {url}"
        )


def extract_messages(content, pattern):
    """Extracts author, creation time, and message parts using a regex pattern.

    Args:
        content (str): The content to extract messages from.
        pattern (str): The regex pattern to match messages.

    Returns:
        list: A list of tuples containing the author, creation time, and message parts.
    """
    return re.findall(pattern, content, re.DOTALL)


def deduplicate_messages(matches):
    """Removes duplicates based on message content, keeping the earliest creation time.

    Args:
        matches (list): A list of tuples containing author, creation time, and message content.

    Returns:
        dict: A dictionary with unique message content as keys, and tuples of author and creation time as values.
    """
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
    """Sorts the deduplicated messages by creation time.

    Args:
        deduplicated_data (dict): A dictionary of deduplicated messages.

    Returns:
        list: A list of tuples containing message content and a tuple of author and creation time, sorted by creation time.
    """
    return sorted(deduplicated_data.items(), key=lambda x: x[1][1])


def write_to_md_file(
    sorted_data,
    output_file_name,
    directory="collection",
):
    """Writes the sorted data to a markdown file, with a default directory.

    Args:
        sorted_data (list): A list of sorted message content.
        output_file_name (str): The name of the output markdown file.
        directory (str, optional): The directory where the markdown file will be saved.
                                   Defaults to "collection".
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    # Full output file path
    output_file_path = os.path.join(directory, output_file_name)

    with open(output_file_path, "w", encoding="utf-8") as md_file:
        for parts_content, (author, _) in sorted_data:
            if author == "assistant":
                md_file.write(f"**ChatGPT**:\n\n{parts_content}\n\n")
            else:
                md_file.write(f"**You**:\n\n{parts_content}\n\n")
            md_file.write("---\n\n")

    return output_file_path
