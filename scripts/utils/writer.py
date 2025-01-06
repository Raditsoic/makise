import os
import json
import re

# Get the next position for a file within a category
def get_next_file_position(category_dir: str) -> int:
    # Count all of markdown files in the category directory
    try:
        md_files = [
            name for name in os.listdir(category_dir)
            if os.path.isfile(os.path.join(category_dir, name)) and name.endswith(".md")
        ]
        
        return len(md_files)
    except FileNotFoundError:
        print(f"Directory '{category_dir}' does not exist.")
        return 1

# Get the next position for a category
def get_next_category_position(docs_dir: str = "docs/") -> int:
    # Count all of the subfolders in the docs directory
    try:
        subfolders = [
            name for name in os.listdir(docs_dir)
            if os.path.isdir(os.path.join(docs_dir, name))
        ]
        
        return len(subfolders) + 1
    except FileNotFoundError:
        print(f"Directory '{docs_dir}' does not exist.")
        return 1

# Write the category file to match docusaurus's expected format
def write_category_file(category_file_path: str, topic: str, description: str = None) -> None:
    try:
        category_metadata = {
            "label": topic,
            "position": get_next_category_position(),
            "link": {
                "type": "generated-index"
            }
        }
        
        if description:
            category_metadata["link"]["description"] = description

        with open(category_file_path, "w") as f:
            f.write(json.dumps(category_metadata, indent=2))
        
        print(f"Category file written successfully to {category_file_path}")
    except Exception as e:
        print(f"An error occurred while writing the category file: {e}")

# Write the markdown file to the specified category directory
def write_markdown_file(content_data: dict, category_dir: str) -> None:
    os.makedirs(category_dir, exist_ok=True)
    category_file_path = os.path.join(category_dir, "_category_.json")

    if not os.path.exists(category_file_path):
        write_category_file(category_file_path, content_data["topic"])

    file_name = content_data['title']
    
    # Convert spaces to hyphens, remove non-alphanumeric characters (except hyphens and underscores), and make lowercase
    file_name = re.sub(r'[^a-zA-Z0-9\s-]', '', file_name)  # remove non-alphanumeric characters
    file_name = file_name.lower()  # make lowercase
    file_name = re.sub(r'[\s]+', '-', file_name)  # replace spaces with hyphens

    file_path = os.path.join(category_dir, f"{file_name}.md")
    with open(file_path, "a") as f:
        f.write(f"""---
sidebar-position: {get_next_file_position(category_dir)}
---
""")
        f.write(content_data["content"])
    print(f"Successfully wrote blog post to {file_path}")
    return None