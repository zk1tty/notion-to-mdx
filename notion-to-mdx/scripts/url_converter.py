#!/usr/bin/env python3
"""
URL converter for Notion to MDX
Extracts URLs and converts them to markdown links with descriptive text
"""

import argparse
import re
from urllib.parse import urlparse


def extract_urls(text: str) -> list:
    """
    Extract all URLs from text

    Args:
        text: Input text

    Returns:
        List of URLs found in text
    """
    # Match http(s) URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)
    return urls


def get_domain_from_url(url: str) -> str:
    """
    Extract domain name from URL

    Args:
        url: Full URL

    Returns:
        Domain name (e.g., "ycombinator.com")
    """
    parsed = urlparse(url)
    domain = parsed.netloc

    # Remove www. prefix if present
    if domain.startswith('www.'):
        domain = domain[4:]

    return domain


def generate_link_text(url: str, context: str = None) -> str:
    """
    Generate descriptive link text for URL

    Args:
        url: The URL
        context: Optional surrounding context text

    Returns:
        Descriptive link text
    """
    # Use domain as fallback
    domain = get_domain_from_url(url)

    # If context provided, try to extract relevant text
    if context:
        # Simple heuristic: use text before or after URL
        # In practice, this could be more sophisticated
        words = context.split()
        if words:
            # Use first few words as link text
            link_text = ' '.join(words[:3])
            if len(link_text) > 3:
                return link_text

    # Map common domains to friendly names
    domain_names = {
        'ycombinator.com': 'Y Combinator',
        'techcrunch.com': 'TechCrunch',
        'wikipedia.org': 'Wikipedia',
        'github.com': 'GitHub',
        'twitter.com': 'Twitter',
        'x.com': 'X (Twitter)',
        'linkedin.com': 'LinkedIn',
        'medium.com': 'Medium',
        'substack.com': 'Substack',
    }

    return domain_names.get(domain, domain)


def convert_urls_to_markdown(text: str) -> str:
    """
    Convert plain URLs in text to markdown links

    Args:
        text: Input text with plain URLs

    Returns:
        Text with URLs converted to markdown links
    """
    urls = extract_urls(text)

    for url in urls:
        # Skip if already in markdown link format
        if f']({url})' in text or f'[{url}]' in text:
            continue

        # Generate link text
        link_text = generate_link_text(url)

        # Replace URL with markdown link
        markdown_link = f'[{link_text}]({url})'
        text = text.replace(url, markdown_link)

    return text


def main():
    parser = argparse.ArgumentParser(
        description='Convert URLs in text to markdown links'
    )
    parser.add_argument(
        '--text',
        help='Text containing URLs to convert'
    )
    parser.add_argument(
        '--url',
        help='Specific URL to convert (optional)'
    )
    parser.add_argument(
        '--link-text',
        help='Custom link text for the URL'
    )

    args = parser.parse_args()

    # Validate arguments
    if not args.url and not args.text:
        parser.error("Either --text or --url must be provided")

    try:
        if args.url and args.link_text:
            # Convert single URL with custom link text
            markdown_link = f'[{args.link_text}]({args.url})'
            print(markdown_link)
        elif args.url:
            # Convert single URL with auto-generated link text
            link_text = generate_link_text(args.url)
            markdown_link = f'[{link_text}]({args.url})'
            print(markdown_link)
        else:
            # Convert all URLs in text
            converted_text = convert_urls_to_markdown(args.text)
            print(converted_text)

    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
