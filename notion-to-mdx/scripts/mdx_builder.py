#!/usr/bin/env python3
"""
MDX file builder with YAML frontmatter
Ensures consistent formatting matching user's blog post format
"""

import argparse
from pathlib import Path
from typing import List


def sanitize_title(title: str) -> str:
    """
    Sanitize title for YAML frontmatter
    Removes colons and other problematic characters

    Args:
        title: Original title

    Returns:
        Sanitized title safe for YAML
    """
    # Remove colons as they break YAML parsing
    title = title.replace(':', ' -')
    # Remove other problematic characters
    title = title.replace('"', "'")
    return title.strip()


def build_frontmatter(title: str, date: str, tags: List[str]) -> str:
    """
    Build YAML frontmatter with proper formatting

    Args:
        title: Post title
        date: Post date in YYYY-MM-DD format
        tags: List of tags

    Returns:
        Formatted YAML frontmatter string
    """
    # Sanitize title to prevent YAML parsing errors
    safe_title = sanitize_title(title)

    frontmatter = "---\n"
    frontmatter += f"title: {safe_title}\n"
    frontmatter += f"date: {date}\n"
    frontmatter += "tags:\n"
    for tag in tags:
        frontmatter += f"  - {tag}\n"
    frontmatter += "---\n"
    return frontmatter


def build_mdx(title: str, date: str, tags: List[str], content: str) -> str:
    """
    Build complete MDX file with frontmatter, content, and footer

    Args:
        title: Post title
        date: Post date in YYYY-MM-DD format
        tags: List of tags
        content: Markdown content body

    Returns:
        Complete MDX file content with footer
    """
    frontmatter = build_frontmatter(title, date, tags)

    # Ensure content doesn't start with extra newlines
    content = content.strip()

    # Add footer advertisement
    footer = "\n\n---\n\n*This blog post was created using the [notion-to-mdx](https://github.com/zk1tty/notion-to-mdx) skill - converting Notion pages to beautiful MDX blog posts.*"

    # Combine with a single blank line between frontmatter and content
    return f"{frontmatter}\n{content}{footer}\n"


def validate_inputs(title: str, date: str, tags: List[str]) -> None:
    """
    Validate input parameters

    Args:
        title: Post title
        date: Post date
        tags: List of tags

    Raises:
        ValueError: If inputs are invalid
    """
    # Validate title
    if not title or len(title) < 5:
        raise ValueError("Title must be at least 5 characters long")
    if len(title) > 100:
        raise ValueError("Title must be at most 100 characters long")

    # Validate date format (YYYY-MM-DD)
    import re
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date):
        raise ValueError("Date must be in YYYY-MM-DD format")

    # Validate tags
    if not tags or len(tags) == 0:
        raise ValueError("At least one tag is required")
    if len(tags) > 10:
        raise ValueError("Maximum 10 tags allowed")


def main():
    parser = argparse.ArgumentParser(
        description='Build MDX blog post with YAML frontmatter'
    )
    parser.add_argument(
        '--title',
        required=True,
        help='Post title'
    )
    parser.add_argument(
        '--date',
        required=True,
        help='Post date in YYYY-MM-DD format'
    )
    parser.add_argument(
        '--tags',
        required=True,
        help='Comma-separated list of tags'
    )
    parser.add_argument(
        '--content',
        required=True,
        help='Markdown content body'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Output file path for the MDX file'
    )
    args = parser.parse_args()

    # Parse tags
    tags = [t.strip() for t in args.tags.split(',') if t.strip()]

    try:
        # Validate inputs
        validate_inputs(args.title, args.date, tags)

        # Build MDX content
        mdx_content = build_mdx(args.title, args.date, tags, args.content)

        # Ensure output directory exists
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write to file
        output_path.write_text(mdx_content, encoding='utf-8')

        print(f"✓ MDX file created: {args.output}")
        print(f"\nFrontmatter:")
        print(f"  Title: {args.title}")
        print(f"  Date: {args.date}")
        print(f"  Tags: {', '.join(tags)}")

    except ValueError as e:
        print(f"✗ Validation error: {e}")
        exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
