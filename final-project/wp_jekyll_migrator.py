"""
WordPress to Jekyll Migrator.

This module provides functionality to convert WordPress export data (CSV format)
into Jekyll-compatible Markdown files with proper frontmatter formatting.
"""

import os
import csv
from datetime import datetime
import re
import unicodedata
import shutil


def sanitize_slug(title):
    """
    Takes a string title and returns a URL-safe slug.
    Normalizes Unicode, removes accents, and replaces invalid characters.
    """
    # Normalize the title to decompose accented characters
    normalized_title = unicodedata.normalize('NFKD', title)
    # Remove accents by keeping only ASCII characters
    ascii_title = normalized_title.encode('ascii', 'ignore').decode('utf-8')
    
    # Replace invalid characters with valid ones
    replacements = {
        ":": "-",
        "/": "-",
        "\\": "-",
        "?": "",
        "*": "",
        "<": "",
        ">": "",
        "|": "",
        "\"": "",
        "'": "",
    }
    
    slug = ascii_title.lower().replace(" ", "-")
    for invalid_char, valid_char in replacements.items():
        slug = slug.replace(invalid_char, valid_char)
    # Remove any remaining invalid characters
    slug = re.sub(r"[^a-zA-Z0-9\-]", "", slug)
    return slug


def read_csv_file(csv_file):
    """
    Reads WordPress export CSV and returns all posts.
    Returns a list of dictionaries containing post data.
    """
    posts = []
    try:
        with open(csv_file, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                posts.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file '{csv_file}' not found.")
        return []
    
    return posts


def process_post_row(row):
    """
    Processes a single post row and returns formatted post data.
    Returns a dictionary with extracted and processed post information.
    """
    title = row.get("Title", "Untitled")
    pub_date = row.get("Date", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    content_text = row.get("Content", "No content available.")
    custom_excerpt = row.get("Excerpt", "This is a default excerpt.")
    image_url = row.get("Image Path", "/assets/images/default.jpg")
    slug = row.get("Slug", sanitize_slug(title))
    categories = row.get("Categories", "Uncategorized")
    
    # Handle image path transformation
    if "Image Path" in row:
        image_url = image_url.replace("https://example.com/images/", "/assets/images/")
    
    # Format the date for the filename
    date = datetime.strptime(pub_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    
    return {
        "title": title,
        "pub_date": pub_date,
        "date": date,
        "content": content_text,
        "excerpt": custom_excerpt,
        "image": image_url,
        "slug": slug,
        "categories": categories,
    }


def add_dropcaps(content_text):
    """
    Adds HTML dropcaps to the first letter of content.
    Returns the modified content with dropcaps applied.
    """
    if content_text.strip():
        content_text = re.sub(
            r"^(\w)", 
            r'<span class="dropcaps">\1</span>', 
            content_text.strip(), 
            count=1
        )
    return content_text


def generate_frontmatter(post_data):
    """
    Takes post metadata and returns Jekyll YAML frontmatter string.
    Includes layout, title, date, categories, image, permalink, excerpt, and comments.
    """
    title = post_data["title"]
    pub_date = post_data["pub_date"]
    image = post_data["image"]
    excerpt = post_data["excerpt"]
    slug = post_data["slug"]
    categories = post_data["categories"]
    
    # Determine comments status based on post age
    comments_status = "false" if (datetime.now() - datetime.strptime(pub_date, "%Y-%m-%d")).days > 90 else "true"
    
    frontmatter = f"""---
layout: post
title: "{title}"
date: {pub_date}
categories: {categories}
image: {image}
permalink: /{slug}/
custom_excerpt: "{excerpt}"
comments: {comments_status}
---
"""
    return frontmatter


def format_markdown_file(frontmatter, content):
    """
    Combines frontmatter and content into complete Markdown format.
    Returns the complete markdown file content as a string.
    """
    md_content = frontmatter + "\n" + content + "\n"
    return md_content


def write_markdown_file(output_folder, filename, content):
    """
    Takes filename and content, writes to disk.
    Creates the file in the specified output folder.
    """
    filepath = os.path.join(output_folder, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as md_file:
            md_file.write(content)
        return True
    except IOError as e:
        print(f"Error writing file '{filepath}': {e}")
        return False


def prepare_output_folder(output_folder):
    """
    Prepares the output folder by removing and recreating it.
    Ensures a clean starting state.
    """
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)


def main():
    """
    Main function that orchestrates the WordPress to Jekyll migration.
    Reads posts from CSV, processes them, and writes Markdown files.
    """
    # Configuration
    csv_file = "sample-data.csv"
    output_folder = "sample-posts"
    
    # Prepare output folder
    prepare_output_folder(output_folder)
    
    # Read CSV file
    posts = read_csv_file(csv_file)
    
    if not posts:
        print("No posts found.")
        return
    
    # Process each post
    processed_count = 0
    for row in posts:
        # Process post row
        post_data = process_post_row(row)
        
        # Add dropcaps to content
        content_with_dropcaps = add_dropcaps(post_data["content"])
        
        # Generate frontmatter
        frontmatter = generate_frontmatter(post_data)
        
        # Format complete markdown file
        md_content = format_markdown_file(frontmatter, content_with_dropcaps)
        
        # Generate filename
        filename = f"{post_data['date']}-{post_data['slug']}.md"
        
        # Write markdown file
        if write_markdown_file(output_folder, filename, md_content):
            processed_count += 1
    
    # Report results
    print(f"Successfully processed {processed_count} posts.")
    print(f"Markdown files have been created in the '{output_folder}' folder.")


if __name__ == "__main__":
    main()
