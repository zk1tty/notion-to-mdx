#!/usr/bin/env python3
"""
Content analyzer for Notion to MDX conversion
Extracts key themes and suggests tags based on content analysis
"""

import argparse
import re
from collections import Counter
from typing import List, Set

# Common words to exclude from tag analysis
STOP_WORDS = {
    'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
    'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
    'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
    'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
    'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
    'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
    'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
    'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over',
    'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work',
    'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these',
    'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has', 'had',
    'were', 'said', 'did', 'having', 'may', 'should', 'am', 'being', 'more',
    'very', 'through', 'really', 'much', 'need', 'thing', 'things', 'lot'
}

# Domain keyword mapping for theme identification
DOMAIN_KEYWORDS = {
    'technology': [
        'software', 'code', 'api', 'algorithm', 'programming', 'developer',
        'engineering', 'tech', 'system', 'data', 'ai', 'machine', 'learning',
        'blockchain', 'crypto', 'bitcoin', 'ethereum', 'web', 'frontend',
        'backend', 'database', 'cloud', 'deployment', 'architecture'
    ],
    'entrepreneurship': [
        'startup', 'founder', 'business', 'company', 'venture', 'entrepreneur',
        'investor', 'funding', 'revenue', 'growth', 'market', 'customer',
        'product', 'launch', 'pivot', 'unicorn', 'accelerator', 'incubator'
    ],
    'personal': [
        'journey', 'experience', 'life', 'story', 'learned', 'growth',
        'challenge', 'failure', 'success', 'lesson', 'reflection', 'mindset',
        'belief', 'perspective', 'change', 'transformation', 'discovery'
    ],
    'finance': [
        'money', 'financial', 'investment', 'trading', 'market', 'portfolio',
        'asset', 'derivative', 'option', 'future', 'capital', 'valuation',
        'risk', 'return', 'fund', 'banking', 'payment', 'currency'
    ],
    'education': [
        'learning', 'university', 'school', 'student', 'education', 'research',
        'study', 'academic', 'professor', 'course', 'teaching', 'knowledge',
        'training', 'skill', 'degree', 'phd', 'thesis'
    ],
    'culture': [
        'culture', 'society', 'community', 'people', 'social', 'network',
        'relationship', 'communication', 'collaboration', 'diversity', 'inclusion',
        'tradition', 'value', 'belief', 'philosophy', 'ethics'
    ]
}


def extract_keywords(content: str, title_weight: int = 3, heading_weight: int = 2) -> Counter:
    """
    Extract and count significant keywords from content

    Args:
        content: The markdown content to analyze
        title_weight: Weight multiplier for title keywords
        heading_weight: Weight multiplier for heading keywords

    Returns:
        Counter of keywords with weighted frequencies
    """
    keywords = Counter()

    # Extract title (first H1 or first line)
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).lower()
        title_words = re.findall(r'\b[a-z]{3,}\b', title)
        for word in title_words:
            if word not in STOP_WORDS:
                keywords[word] += title_weight

    # Extract from headings (H2, H3, etc.)
    headings = re.findall(r'^#{2,}\s+(.+)$', content, re.MULTILINE)
    for heading in headings:
        heading_words = re.findall(r'\b[a-z]{3,}\b', heading.lower())
        for word in heading_words:
            if word not in STOP_WORDS:
                keywords[word] += heading_weight

    # Extract from body text (remove markdown formatting)
    body = re.sub(r'^#+\s+.+$', '', content, flags=re.MULTILINE)  # Remove headings
    body = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', body)  # Remove links, keep text
    body = re.sub(r'[*_`~]', '', body)  # Remove formatting
    body_words = re.findall(r'\b[a-z]{3,}\b', body.lower())

    for word in body_words:
        if word not in STOP_WORDS:
            keywords[word] += 1

    return keywords


def identify_themes(keywords: Counter) -> List[str]:
    """
    Identify themes based on keyword clusters

    Args:
        keywords: Counter of extracted keywords

    Returns:
        List of identified theme names
    """
    theme_scores = Counter()

    for word, count in keywords.items():
        for theme, theme_keywords in DOMAIN_KEYWORDS.items():
            if word in theme_keywords:
                theme_scores[theme] += count

    # Return themes with score > 0, sorted by score
    identified = [theme for theme, score in theme_scores.most_common() if score > 0]
    return identified[:3]  # Limit to top 3 themes


def suggest_tags(content: str, max_tags: int = 5) -> List[str]:
    """
    Main function: analyze content and suggest tags

    Args:
        content: The markdown content to analyze
        max_tags: Maximum number of tags to suggest

    Returns:
        List of suggested tags
    """
    # Extract keywords
    keywords = extract_keywords(content)

    # Identify themes
    themes = identify_themes(keywords)

    # Combine themes and high-frequency keywords
    suggested = []

    # Add top themes as tags
    for theme in themes[:2]:  # Top 2 themes
        suggested.append(theme)

    # Add high-frequency specific keywords (not in themes)
    theme_words = set()
    for theme_keywords in DOMAIN_KEYWORDS.values():
        theme_words.update(theme_keywords)

    # Find proper nouns and important keywords
    # Proper nouns: words that appear capitalized in original content
    proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)*\b', content)
    proper_noun_counts = Counter(proper_nouns)

    # Add significant proper nouns (appearing 2+ times)
    for noun, count in proper_noun_counts.most_common():
        if count >= 2 and noun.lower() not in STOP_WORDS and len(suggested) < max_tags:
            suggested.append(noun)

    # Add other high-frequency keywords
    for word, count in keywords.most_common(20):
        if len(suggested) >= max_tags:
            break
        if word not in theme_words and word not in [s.lower() for s in suggested]:
            # Prefer specific technical terms
            if count >= 3:
                suggested.append(word)

    return suggested[:max_tags]


def main():
    parser = argparse.ArgumentParser(
        description='Analyze content and suggest tags for blog posts'
    )
    parser.add_argument(
        '--content',
        required=True,
        help='Content to analyze (markdown text)'
    )
    parser.add_argument(
        '--max-tags',
        type=int,
        default=5,
        help='Maximum number of tags to suggest (default: 5)'
    )
    args = parser.parse_args()

    tags = suggest_tags(args.content, args.max_tags)

    # Output tags one per line for easy parsing
    for tag in tags:
        print(tag)


if __name__ == '__main__':
    main()
