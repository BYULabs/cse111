"""
Test functions for WordPress to Jekyll Migrator.

This module contains unit tests for all major functions in wp_jekyll_migrator.py
using pytest framework. Each test function validates specific functionality and
edge cases.
"""

import pytest
from wp_jekyll_migrator import (
    sanitize_slug,
    add_dropcaps,
    generate_frontmatter,
    format_markdown_file,
    process_post_row
)


# ============================================================================
# Tests for sanitize_slug() function
# ============================================================================

def test_sanitize_slug_basic():
    """Test basic slug generation from simple titles."""
    # Arrange
    title = "Hello World"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "hello-world"


def test_sanitize_slug_with_numbers():
    """Test slug generation with numbers in the title."""
    # Arrange
    title = "Python 3 Tutorial"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "python-3-tutorial"


def test_sanitize_slug_special_chars():
    """Test handling of special characters that should be removed."""
    # Arrange
    title = "What? Really! (No way)"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "what-really-no-way"
    assert "?" not in result
    assert "!" not in result
    assert "(" not in result
    assert ")" not in result


def test_sanitize_slug_colons_slashes():
    """Test that colons and slashes are replaced with hyphens."""
    # Arrange
    title = "Part 1: Getting Started/Basics"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "part-1--getting-started-basics"
    assert "/" not in result
    assert ":" not in result


def test_sanitize_slug_unicode():
    """Test Unicode and accented character handling."""
    # Arrange
    title = "Café Menu"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "cafe-menu"
    assert "é" not in result


def test_sanitize_slug_multiple_accents():
    """Test handling of multiple accented characters."""
    # Arrange
    title = "Naïveté Résumé"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "naivete-resume"
    assert "ï" not in result
    assert "é" not in result


def test_sanitize_slug_spaces():
    """Test space-to-hyphen conversion."""
    # Arrange
    title = "This Is A Test"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "this-is-a-test"
    assert " " not in result


def test_sanitize_slug_multiple_spaces():
    """Test that multiple spaces are converted correctly."""
    # Arrange
    title = "Multiple   Spaces"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "multiple---spaces"


def test_sanitize_slug_lowercase():
    """Test that uppercase is converted to lowercase."""
    # Arrange
    title = "UPPERCASE TITLE"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "uppercase-title"
    assert result == result.lower()


def test_sanitize_slug_mixed_case_special():
    """Test combined uppercase, special chars, and spaces."""
    # Arrange
    title = "The BEST: Tips & Tricks!"
    
    # Act
    result = sanitize_slug(title)
    
    # Assert
    assert result == "the-best--tips--tricks"
    assert result == result.lower()


# ============================================================================
# Tests for add_dropcaps() function
# ============================================================================

def test_add_dropcaps_basic():
    """Test dropcaps added to first letter."""
    # Arrange
    content = "Web development is important."
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    assert result.startswith('<span class="dropcaps">W</span>')
    assert "eb development is important." in result


def test_add_dropcaps_number_start():
    """Test dropcaps with content starting with a number."""
    # Arrange
    content = "3 reasons to learn Python"
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    assert result.startswith('<span class="dropcaps">3</span>')
    assert " reasons to learn Python" in result


def test_add_dropcaps_only_first_letter():
    """Test that only the first letter gets dropcaps."""
    # Arrange
    content = "Amazing Article About Python"
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    # Count occurrences of dropcaps span
    dropcap_count = result.count('<span class="dropcaps">')
    assert dropcap_count == 1


def test_add_dropcaps_empty_string():
    """Test dropcaps with empty content."""
    # Arrange
    content = ""
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    assert result == ""
    assert '<span class="dropcaps">' not in result


def test_add_dropcaps_whitespace_only():
    """Test dropcaps with whitespace-only content."""
    # Arrange
    content = "   "
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    # Whitespace-only content returns unchanged (strip() is only used for if check)
    assert result == "   "
    assert '<span class="dropcaps">' not in result


def test_add_dropcaps_single_letter():
    """Test dropcaps with single letter content."""
    # Arrange
    content = "A"
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    assert result == '<span class="dropcaps">A</span>'


def test_add_dropcaps_preserves_rest():
    """Test that dropcaps preserves the rest of the content."""
    # Arrange
    content = "Python is a great programming language"
    
    # Act
    result = add_dropcaps(content)
    
    # Assert
    expected = '<span class="dropcaps">P</span>ython is a great programming language'
    assert result == expected


# ============================================================================
# Tests for generate_frontmatter() function
# ============================================================================

def test_generate_frontmatter_format():
    """Test correct YAML frontmatter format."""
    # Arrange
    post_data = {
        "title": "Test Post",
        "pub_date": "2025-02-18",
        "image": "/assets/images/test.jpg",
        "excerpt": "A test excerpt",
        "slug": "test-post",
        "categories": "Tutorial"
    }
    
    # Act
    result = generate_frontmatter(post_data)
    
    # Assert
    assert result.startswith("---")
    assert result.endswith("---\n")
    assert "layout: post" in result
    assert 'title: "Test Post"' in result
    assert "date: 2025-02-18" in result
    assert "categories: Tutorial" in result
    assert "image: /assets/images/test.jpg" in result
    assert "permalink: /test-post/" in result
    assert 'custom_excerpt: "A test excerpt"' in result
    assert "comments:" in result


def test_generate_frontmatter_has_yaml_markers():
    """Test that frontmatter has proper YAML markers."""
    # Arrange
    post_data = {
        "title": "Test",
        "pub_date": "2025-02-18",
        "image": "/img.jpg",
        "excerpt": "Test",
        "slug": "test",
        "categories": "Test"
    }
    
    # Act
    result = generate_frontmatter(post_data)
    
    # Assert
    lines = result.split("\n")
    assert lines[0] == "---"
    assert lines[-2] == "---"


def test_generate_frontmatter_escapes_quotes():
    """Test that titles with quotes are properly handled."""
    # Arrange
    post_data = {
        "title": 'Hello "World"',
        "pub_date": "2025-02-18",
        "image": "/img.jpg",
        "excerpt": "Test",
        "slug": "test",
        "categories": "Test"
    }
    
    # Act
    result = generate_frontmatter(post_data)
    
    # Assert
    assert 'title: "Hello "World""' in result


# ============================================================================
# Tests for format_markdown_file() function
# ============================================================================

def test_format_markdown_file_structure():
    """Test complete Markdown file structure with frontmatter and content."""
    # Arrange
    frontmatter = "---\nlayout: post\ntitle: \"Test\"\n---\n"
    content = "This is test content."
    
    # Act
    result = format_markdown_file(frontmatter, content)
    
    # Assert
    assert result.startswith(frontmatter)
    assert content in result
    assert result.endswith("\n")


def test_format_markdown_file_has_blank_line():
    """Test that there's a blank line between frontmatter and content."""
    # Arrange
    frontmatter = "---\nlayout: post\n---\n"
    content = "Content here"
    
    # Act
    result = format_markdown_file(frontmatter, content)
    
    # Assert
    expected = frontmatter + "\n" + content + "\n"
    assert result == expected


def test_format_markdown_file_multiline_content():
    """Test with multiline content."""
    # Arrange
    frontmatter = "---\nlayout: post\n---\n"
    content = "Line 1\nLine 2\nLine 3"
    
    # Act
    result = format_markdown_file(frontmatter, content)
    
    # Assert
    assert "Line 1" in result
    assert "Line 2" in result
    assert "Line 3" in result


# ============================================================================
# Tests for process_post_row() function
# ============================================================================

def test_process_post_row_complete_data():
    """Test processing a complete post row with all fields."""
    # Arrange
    row = {
        "Title": "Hello World",
        "Date": "2025-02-18",
        "Content": "This is content",
        "Excerpt": "This is excerpt",
        "Image Path": "https://example.com/images/test.jpg",
        "Slug": "hello-world",
        "Categories": "Tutorial"
    }
    
    # Act
    result = process_post_row(row)
    
    # Assert
    assert result["title"] == "Hello World"
    assert result["content"] == "This is content"
    assert result["excerpt"] == "This is excerpt"
    assert result["slug"] == "hello-world"
    assert result["categories"] == "Tutorial"
    assert "/assets/images/test.jpg" in result["image"]


def test_process_post_row_missing_title():
    """Test processing post row with missing title."""
    # Arrange
    row = {
        "Date": "2025-02-18",
        "Content": "Content here"
    }
    
    # Act
    result = process_post_row(row)
    
    # Assert
    assert result["title"] == "Untitled"


def test_process_post_row_missing_slug_generates_from_title():
    """Test that missing slug is generated from title."""
    # Arrange
    row = {
        "Title": "Test Post",
        "Date": "2025-02-18",
        "Content": "Content"
    }
    
    # Act
    result = process_post_row(row)
    
    # Assert
    assert result["slug"] == "test-post"


def test_process_post_row_missing_category():
    """Test that missing category defaults to Uncategorized."""
    # Arrange
    row = {
        "Title": "Test",
        "Date": "2025-02-18",
        "Content": "Content"
    }
    
    # Act
    result = process_post_row(row)
    
    # Assert
    assert result["categories"] == "Uncategorized"


def test_process_post_row_image_path_transformation():
    """Test that image paths are properly transformed."""
    # Arrange
    row = {
        "Title": "Test",
        "Date": "2025-02-18",
        "Content": "Content",
        "Image Path": "https://example.com/images/photo.jpg"
    }
    
    # Act
    result = process_post_row(row)
    
    # Assert
    assert result["image"] == "/assets/images/photo.jpg"
    assert "https://example.com" not in result["image"]


# ============================================================================
# Integration Tests
# ============================================================================

def test_integration_slug_to_frontmatter():
    """Test integration from title to complete frontmatter."""
    # Arrange
    title = "Hello World!"
    
    # Act
    slug = sanitize_slug(title)
    post_data = {
        "title": title,
        "pub_date": "2025-02-18",
        "image": "/assets/images/test.jpg",
        "excerpt": "Test excerpt",
        "slug": slug,
        "categories": "Blog"
    }
    frontmatter = generate_frontmatter(post_data)
    
    # Assert
    assert "hello-world" in frontmatter
    assert "permalink: /hello-world/" in frontmatter


def test_integration_complete_markdown_generation():
    """Test complete markdown file generation from post data."""
    # Arrange
    title = "Getting Started"
    content = "Web development is fun"
    
    # Act
    slug = sanitize_slug(title)
    content_styled = add_dropcaps(content)
    post_data = {
        "title": title,
        "pub_date": "2025-02-18",
        "image": "/assets/images/start.jpg",
        "excerpt": "A guide",
        "slug": slug,
        "categories": "Tutorial"
    }
    frontmatter = generate_frontmatter(post_data)
    markdown = format_markdown_file(frontmatter, content_styled)
    
    # Assert
    assert "---" in markdown
    assert "getting-started" in markdown
    assert '<span class="dropcaps">W</span>' in markdown
    # Content has dropcaps applied, so check for the styled version
    assert '<span class="dropcaps">W</span>eb development is fun' in markdown


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
