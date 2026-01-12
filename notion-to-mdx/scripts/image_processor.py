#!/usr/bin/env python3
"""
Image processor for Notion to MDX conversion
Downloads images and generates alt text using OCR/vision
"""

import argparse
import re
import requests
from pathlib import Path
from urllib.parse import urlparse


def sanitize_filename(text: str) -> str:
    """
    Convert text to safe filename

    Args:
        text: Original text

    Returns:
        Safe filename with lowercase, hyphens, no special chars
    """
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)
    # Remove special characters except hyphens and dots
    text = re.sub(r'[^a-z0-9\-\.]', '', text)
    # Remove multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    # Strip leading/trailing hyphens
    text = text.strip('-')
    return text


def download_image(image_url: str, output_dir: Path, filename: str = None) -> Path:
    """
    Download image from URL

    Args:
        image_url: URL of the image
        output_dir: Directory to save image
        filename: Optional custom filename (auto-generated if not provided)

    Returns:
        Path to downloaded image
    """
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename if not provided
    if not filename:
        parsed_url = urlparse(image_url)
        original_name = Path(parsed_url.path).name
        filename = sanitize_filename(original_name)

    # Ensure filename has extension
    if '.' not in filename:
        filename += '.jpg'

    output_path = output_dir / filename

    # Download image
    response = requests.get(image_url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"✓ Downloaded: {output_path}")
    return output_path


def generate_alt_text_from_context(image_context: str) -> str:
    """
    Generate alt text from surrounding context

    Args:
        image_context: Text surrounding the image in Notion

    Returns:
        Generated alt text
    """
    # This is a simple heuristic - in practice, use vision API or OCR
    # For now, clean up the context text to make reasonable alt text
    if not image_context:
        return "Image"

    # Clean and truncate
    alt_text = image_context.strip()
    alt_text = re.sub(r'\s+', ' ', alt_text)

    # Truncate if too long
    if len(alt_text) > 100:
        alt_text = alt_text[:97] + "..."

    return alt_text


def wrap_image_with_styling(image_path: str, alt_text: str) -> str:
    """
    Wrap image markdown with centered div styling and caption

    Args:
        image_path: Relative path to image (e.g., ./photos/image.jpg)
        alt_text: Alt text for the image

    Returns:
        Formatted MDX with div styling and caption
    """
    return f"""<div style={{{{ textAlign: 'center', margin: '2rem 0' }}}}>
  <div style={{{{ display: 'inline-block', width: '75%', maxWidth: '700px' }}}}>
![{alt_text}]({image_path})
    <div style={{{{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem', fontStyle: 'italic' }}}}>
      {alt_text}
    </div>
  </div>
</div>"""


def main():
    parser = argparse.ArgumentParser(
        description='Process images for Notion to MDX conversion'
    )
    parser.add_argument(
        '--url',
        required=True,
        help='Image URL to download'
    )
    parser.add_argument(
        '--output-dir',
        required=True,
        help='Output directory for images'
    )
    parser.add_argument(
        '--filename',
        help='Custom filename (optional, auto-generated if not provided)'
    )
    parser.add_argument(
        '--alt-text',
        help='Alt text for the image (optional, can be generated from context)'
    )
    parser.add_argument(
        '--context',
        help='Surrounding text context to help generate alt text'
    )

    args = parser.parse_args()

    try:
        # Download image
        output_dir = Path(args.output_dir)
        image_path = download_image(args.url, output_dir, args.filename)

        # Generate alt text
        if args.alt_text:
            alt_text = args.alt_text
        elif args.context:
            alt_text = generate_alt_text_from_context(args.context)
        else:
            alt_text = "Image"

        # Generate relative path for MDX
        relative_path = f"./photos/{image_path.name}"

        # Output formatted MDX
        mdx_output = wrap_image_with_styling(relative_path, alt_text)
        print("\n--- MDX Output ---")
        print(mdx_output)
        print("\nAlt text:", alt_text)

    except Exception as e:
        print(f"✗ Error: {e}")
        exit(1)


if __name__ == '__main__':
    main()
