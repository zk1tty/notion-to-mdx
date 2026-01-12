# Tag Extraction and Suggestion Guide

Methodology for intelligent tag extraction from blog content using the content_analyzer.py script.

## Table of Contents

1. [Overview](#overview)
2. [Algorithm Explanation](#algorithm-explanation)
3. [Customizing Tag Suggestions](#customizing-tag-suggestions)
4. [Tag Best Practices](#tag-best-practices)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

## Overview

The tag extraction system analyzes blog content to suggest relevant tags automatically. It uses a combination of:

1. **Keyword Frequency Analysis**: Identifies important words based on frequency
2. **Weighted Extraction**: Prioritizes title and heading keywords
3. **Theme Detection**: Matches content against domain keyword dictionaries
4. **Proper Noun Recognition**: Identifies specific entities (people, places, projects)

## Algorithm Explanation

### Step 1: Keyword Extraction

The script extracts keywords from three areas with different weights:

- **Title (H1) keywords**: Weight ×3
- **Heading (H2, H3) keywords**: Weight ×2
- **Body text keywords**: Weight ×1

**Rationale**: Titles and headings are more representative of main topics.

**Example**:
```markdown
# Building Startups in San Francisco    ← "startup" and "francisco" weighted ×3
## The Tech Scene                        ← "tech" weighted ×2
I learned about software development... ← "software" and "development" weighted ×1
```

### Step 2: Stopword Filtering

Common words are filtered out to focus on meaningful keywords:

**Filtered**: the, be, to, of, and, a, in, that, have, it, for, this, what, how, etc.

**Kept**: startup, technology, building, software, san, francisco, blockchain, etc.

### Step 3: Theme Identification

Keywords are matched against predefined domain categories:

**Domain Categories**:
- **technology**: software, code, api, algorithm, ai, blockchain, web, etc.
- **entrepreneurship**: startup, founder, business, company, investor, etc.
- **personal**: journey, experience, life, learned, growth, reflection, etc.
- **finance**: money, trading, investment, market, portfolio, capital, etc.
- **education**: learning, university, research, academic, teaching, etc.
- **culture**: society, community, people, relationship, diversity, etc.

**Theme Scoring**:
- Each keyword match adds to the theme's score
- Top 2-3 themes become candidate tags

### Step 4: Proper Noun Detection

Proper nouns (capitalized words) appearing 2+ times are identified as potential tags:

**Examples**:
- San Francisco (location)
- Ethereum (technology/project)
- Entrepreneur First (program/organization)
- NetworkSchool (community)

### Step 5: Tag Selection

Final tags are selected using this priority:

1. **Top 2 themes** (e.g., "technology", "personal")
2. **Significant proper nouns** (appearing 2+ times)
3. **High-frequency specific keywords** (appearing 3+ times, not generic themes)

**Result**: 2-5 relevant tags

## Customizing Tag Suggestions

### Modifying Domain Keywords

Edit `DOMAIN_KEYWORDS` dictionary in `scripts/content_analyzer.py`:

```python
DOMAIN_KEYWORDS = {
    'technology': [
        'software', 'code', 'api',
        # Add your specific tech keywords
        'kubernetes', 'nextjs', 'tailwind'
    ],
    'custom-domain': [  # Add new domains
        'keyword1', 'keyword2', 'keyword3'
    ]
}
```

### Adjusting Weights

Modify extraction weights in `extract_keywords()`:

```python
# Current defaults
title_weight = 3      # Title keywords ×3
heading_weight = 2    # Heading keywords ×2
body_weight = 1       # Body keywords ×1

# Adjust to emphasize different sections
title_weight = 5      # More emphasis on title
heading_weight = 1    # Less emphasis on headings
```

### Changing Frequency Thresholds

Adjust minimum occurrence thresholds:

```python
# For proper nouns (line ~135)
if count >= 2:  # Change to 3 for stricter filtering

# For keywords (line ~145)
if count >= 3:  # Change to 4 or 5 for higher bar
```

### Limiting Tag Count

Change maximum tags in function call:

```bash
# Default: 5 tags
python scripts/content_analyzer.py --content "$CONTENT" --max-tags 5

# More tags: 7
python scripts/content_analyzer.py --content "$CONTENT" --max-tags 7

# Fewer tags: 3
python scripts/content_analyzer.py --content "$CONTENT" --max-tags 3
```

### Adding Stop Words

Expand the stopword list to filter out more generic terms:

```python
STOP_WORDS = {
    'the', 'be', 'to',
    # Add domain-specific stopwords
    'content', 'post', 'article', 'blog'
}
```

## Tag Best Practices

### General Guidelines

1. **Specificity**: Prefer specific over generic tags
   - ✓ Good: `blockchain`, `ethereum`, `san-francisco`
   - ✗ Avoid: `technology`, `place`, `topic`

2. **Consistency**: Use consistent naming conventions
   - Use lowercase for generic terms: `startups`, `technology`
   - Use PascalCase for proper nouns: `SanFrancisco`, `NetworkSchool`

3. **Relevance**: Each tag should add meaningful categorization
   - ✓ Good: Tags represent distinct themes or topics
   - ✗ Avoid: Tags that are too similar or redundant

4. **Quantity**: 2-5 tags per post
   - Minimum 2: Ensures basic categorization
   - Maximum 5: Prevents tag dilution

### Tag Naming Conventions

Based on user's existing blog posts:

**Proper Nouns** (places, organizations, people):
- Format: PascalCase or as-written
- Examples: `SanFrancisco`, `NetworkSchool`, `EntrepreneurFirst`

**Generic Topics** (themes, domains):
- Format: lowercase, hyphenated if multi-word
- Examples: `technology`, `personal`, `startups`, `machine-learning`

**Mixed Example**:
```yaml
tags:
  - technology       # Generic theme
  - startups         # Generic theme
  - SanFrancisco     # Proper noun (place)
  - YCombinator      # Proper noun (organization)
```

### Tag Categories

Organize tags into mental categories:

**Domain Tags** (what field/industry):
- `technology`, `finance`, `education`, `design`

**Topic Tags** (what specific area):
- `blockchain`, `ai`, `web-development`, `trading`

**Context Tags** (what aspect/perspective):
- `personal`, `tutorial`, `philosophy`, `culture`

**Entity Tags** (where/who/what organization):
- `Singapore`, `Stanford`, `Ethereum`, `NetworkSchool`

## Examples

### Example 1: Technical Startup Post

**Content**:
```markdown
# Building a Crypto Trading Platform

We built a decentralized trading engine on Ethereum. The architecture uses smart contracts for settlement and a Python backend for order matching.

## Technical Challenges

Implementing atomic swaps and handling blockchain confirmations...
```

**Extracted Tags**:
1. `technology` (theme)
2. `finance` (theme)
3. `Ethereum` (proper noun, 2+ occurrences)
4. `blockchain` (keyword, 3+ occurrences)
5. `trading` (keyword, 3+ occurrences)

**Final Tags**: `technology, finance, Ethereum, blockchain, trading`

### Example 2: Personal Journey Post

**Content**:
```markdown
# My Journey to Dark Talent

After failing the University of Tokyo exam, I discovered Elon Musk's biography. This changed my perspective on success and led me to study complexity science.

## Breaking Free from Expectations

Growing up in Osaka, Japan, I faced traditional expectations...
```

**Extracted Tags**:
1. `personal` (theme)
2. `education` (theme)
3. `Japan` (proper noun, 2+ occurrences)
4. `journey` (keyword, 3+ occurrences)

**Final Tags**: `personal, education, Japan, journey`

### Example 3: Location-Specific Post

**Content**:
```markdown
# Moving to San Francisco

San Francisco's startup ecosystem is incredible. I joined Entrepreneur First and met amazing founders building innovative companies.

## The Community

The NetworkSchool community in SF has been transformative...
```

**Extracted Tags**:
1. `personal` (theme)
2. `entrepreneurship` (theme)
3. `SanFrancisco` (proper noun, 3+ occurrences)
4. `EntrepreneurFirst` (proper noun, 2+ occurrences)
5. `NetworkSchool` (proper noun, 2+ occurrences)

**Final Tags**: `personal, entrepreneurship, SanFrancisco, EntrepreneurFirst, NetworkSchool`

## Troubleshooting

### Issue: Too Many Generic Tags

**Problem**: Getting tags like "technology", "work", "people"

**Solutions**:
1. Increase keyword frequency threshold
2. Add generic terms to stopwords
3. Prefer proper nouns over generic themes
4. Manually review and replace generic tags

### Issue: Missing Important Tags

**Problem**: Relevant keywords not appearing in suggestions

**Solutions**:
1. Check if keyword appears in domain dictionaries
2. Verify keyword isn't in stopwords list
3. Lower frequency thresholds
4. Increase max_tags parameter

### Issue: Proper Nouns Not Detected

**Problem**: Important names/places not being tagged

**Solutions**:
1. Verify proper capitalization in content
2. Lower proper noun frequency threshold (currently 2)
3. Manually add important proper nouns

### Issue: Too Many Tags

**Problem**: Getting 7-10 suggested tags

**Solutions**:
1. Reduce --max-tags parameter
2. Increase frequency thresholds
3. Prioritize themes over keywords
4. Manually select top 3-5 most relevant

### Issue: Irrelevant Tags

**Problem**: Tags that don't match content theme

**Solutions**:
1. Review extracted keywords (add debug logging)
2. Adjust domain keyword mappings
3. Add misleading terms to stopwords
4. Use manual override for critical posts

## Manual Override Workflow

While the script provides intelligent suggestions, always allow for manual refinement:

1. **Generate suggestions**: Run content_analyzer.py
2. **Review**: Check relevance and specificity
3. **Refine**: Add/remove/modify tags as needed
4. **Confirm**: Present final list to user
5. **Build**: Use refined tags in mdx_builder.py

**Example Workflow**:
```bash
# 1. Generate suggestions
SUGGESTED=$(python scripts/content_analyzer.py --content "$CONTENT")

# 2. Review (show to user)
echo "Suggested tags: $SUGGESTED"

# 3. Get user confirmation/modifications
read -p "Modify tags? " USER_TAGS

# 4. Use final tags
FINAL_TAGS="${USER_TAGS:-$SUGGESTED}"

# 5. Build MDX
python scripts/mdx_builder.py --tags "$FINAL_TAGS" ...
```

## Advanced: Custom Tag Strategies

### Strategy 1: Series Tags

For multi-part blog series, add consistent series tag:

```python
# If part of a series, prepend series tag
series_tag = "startup-journey"  # User-specified
tags = [series_tag] + suggested_tags
```

### Strategy 2: Time-Based Tags

Add temporal context for relevant posts:

```python
# For time-specific posts
year = datetime.now().year
if 'retrospective' in content or 'year-in-review' in content:
    tags.append(f"{year}")
```

### Strategy 3: Audience Tags

Tag by intended audience:

```python
# Detect audience indicators
if any(word in content for word in ['beginner', 'introduction', 'basics']):
    tags.append('tutorial')
elif any(word in content for word in ['advanced', 'deep-dive', 'expert']):
    tags.append('advanced')
```

## Summary

**Key Takeaways**:
1. Tag extraction combines frequency analysis, theme detection, and proper noun recognition
2. Customization is possible through adjusting weights, thresholds, and domain keywords
3. Always allow manual review and refinement of suggested tags
4. Aim for 2-5 specific, relevant tags per post
5. Maintain consistent naming conventions (lowercase themes, PascalCase proper nouns)

**Remember**: The goal is to suggest good tags quickly, not to be perfect. User review ensures quality while saving time compared to manual tag creation from scratch.
