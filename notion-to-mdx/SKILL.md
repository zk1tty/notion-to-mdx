---
name: notion-to-mdx
description: "Convert Notion pages to MDX blog posts with smart metadata extraction. Use when users want to: (1) Convert Notion content to MDX format, (2) Export Notion pages as blog posts, (3) Transform Notion documentation to markdown, (4) Create blog posts from Notion with automatic tag suggestions and frontmatter. Supports both Notion MCP server integration and pasted content as fallback."
---

# Notion to MDX Converter

Convert unstructured Notion pages into properly formatted MDX blog posts with YAML frontmatter, smart tag suggestions, and preserved markdown formatting.

## Overview

This skill transforms Notion content into MDX blog posts ready for static site generators. It handles:
- Basic Notion formatting (headings, bold, italic, lists, code, links, blockquotes)
- Smart metadata extraction (title, date, tags)
- YAML frontmatter generation
- Consistent MDX output format

The conversion process supports both Notion MCP server access and manual content input as fallback.

## Workflow

Follow this 6-step sequential process to convert Notion pages to MDX:

### Step 1: Access Notion Content

**Option A: Notion MCP Server (Preferred)**

Check if Notion MCP tools are available:
```bash
# Check for MCP tools
# Look for Notion-related tools in available MCP servers
```

If Notion MCP is available:
1. Use MCP tools to fetch the page content
2. Parse the returned Notion blocks
3. Proceed to Step 2

**Option B: Pasted Content (Fallback)**

If Notion MCP is not available:
1. Ask user to export or copy-paste the Notion page content
2. Accept the content as text/markdown
3. Proceed to Step 2

### Step 2: Convert Notion Blocks to Markdown

Apply basic conversion rules:

**Text Formatting**:
- Bold → `**text**`
- Italic → `*text*`
- Inline code → `` `code` ``
- Strikethrough → `~~text~~`

**Structure**:
- Heading 1 → `# Title`
- Heading 2 → `## Section`
- Heading 3 → `### Subsection`
- Bullet list → `- item`
- Numbered list → `1. item`
- Blockquote → `> quote`

**Code Blocks**:
````
```language
code here
```
````

**Links**:
- Extract all URLs from Notion content
- Convert to markdown format: `[descriptive text](url)`
- If URL has no description, use the domain name or page title as link text

**Images**:
1. **Extract images** from Notion content
2. **Download images** and save to `./photos/` folder within the post directory
3. **OCR images** to capture meaning and generate descriptive alt text
4. **Wrap with centered styling and caption**:

```mdx
<div style={{ textAlign: 'center', margin: '2rem 0' }}>
  <div style={{ display: 'inline-block', width: '75%', maxWidth: '700px' }}>
![Alt text describing image](./photos/image-name.jpg)
    <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem', fontStyle: 'italic' }}>
      Image caption/description here
    </div>
  </div>
</div>
```

**Caption format**: Use the same descriptive text from alt text or OCR analysis

**Image handling workflow**:
- Create `photos` folder: `mkdir -p ./photos`
- Download image from Notion URL
- Generate filename: lowercase, hyphenated (e.g., `elon-musk-book.jpg`)
- Use OCR or image analysis to generate meaningful alt text
- Place image in appropriate location within content flow

For complex Notion elements or edge cases, read [references/notion_elements_mapping.md](references/notion_elements_mapping.md).

### Step 3: Extract Metadata

#### Title Extraction

Extract title using priority order:
1. First `# Heading 1` in content
2. Notion page title (if available via MCP)
3. Prompt user to provide title

Clean the title:
- Remove markdown formatting (`#`, `**`, etc.)
- Strip leading/trailing whitespace
- **Remove colons (`:`)** or replace with ` -` to prevent YAML parsing errors
- Remove problematic characters like double quotes
- Validate: 5-100 characters

#### Date

Use current date in YYYY-MM-DD format:
```python
from datetime import date
today = date.today().isoformat()  # e.g., "2025-01-12"
```

#### Tag Suggestions

Run the content analyzer to suggest tags:

```bash
python scripts/content_analyzer.py --content "$MARKDOWN_CONTENT" --max-tags 5
```

**How it works**:
- Extracts keywords weighted by position (title ×3, headings ×2, body ×1)
- Identifies themes (technology, entrepreneurship, personal, etc.)
- Detects proper nouns (places, organizations, people)
- Suggests 2-5 relevant tags

**Example output**:
```
technology
entrepreneurship
SanFrancisco
startups
```

**User confirmation**:
1. Present suggested tags to user
2. Allow modifications (add/remove/change tags)
3. Accept final tag list

For customizing tag extraction logic, see [references/tag_extraction_guide.md](references/tag_extraction_guide.md).

### Step 4: Build MDX File

Use the MDX builder script to create the final file:

```bash
python scripts/mdx_builder.py \
  --title "Post Title Here" \
  --date "2025-01-12" \
  --tags "tag1,tag2,tag3" \
  --content "$MARKDOWN_CONTENT" \
  --output "output_path.mdx"
```

**Script validates**:
- Title: 5-100 characters
- Date: YYYY-MM-DD format
- Tags: At least 1, max 10
- Output: Creates parent directories if needed

**Automatic additions**:
- Footer advertisement: Adds credit line at the end of each post
  ```
  ---

  *This blog post was created using the notion-to-mdx skill - converting Notion pages to beautiful MDX blog posts.*
  ```

**Output format**:
```mdx
---
title: Post Title Here
date: 2025-01-12
tags:
  - tag1
  - tag2
  - tag3
---

[markdown content here]
```

### Step 5: Save and Move

1. **Save file**: Write to temporary location first (e.g., current directory)
2. **Display preview**: Show frontmatter and first paragraph
3. **Verify format**: Confirm YAML frontmatter is valid
4. **Move to blog directory**: Create folder and move file to final location

### Step 6: Verify Build

After moving the file, run the development server to verify no critical errors:

```bash
cd /Users/norikakizawa/Projects/n0ri.com
npm run develop
```

**Check for**:
- No YAML parsing errors
- No build failures
- Site builds successfully
- New post appears in development server

**If errors occur**:
1. Check title for special characters (colons, quotes)
2. Verify YAML frontmatter syntax
3. Ensure all tags are properly formatted
4. Fix issues and rebuild

**Allow iteration**: User can modify tags or title and rebuild if needed

**Moving to blog directory**:

Convert the title to lowercase folder name, create folders, and move files:

```bash
# Convert title to lowercase with hyphens
# Example: "Building DoubleClick for AI Agents" -> "building-doubleclick-for-ai-agents"
FOLDER_NAME=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g')

# Create folder structure in blog posts directory
mkdir -p "/Users/norikakizawa/Projects/n0ri.com/content/posts/$FOLDER_NAME/photos"

# Move and rename file to index.mdx
mv "temp-file.mdx" "/Users/norikakizawa/Projects/n0ri.com/content/posts/$FOLDER_NAME/index.mdx"

# Move images to photos folder (if any)
if [ -d "temp-images" ]; then
  mv temp-images/* "/Users/norikakizawa/Projects/n0ri.com/content/posts/$FOLDER_NAME/photos/"
fi

# Verify
ls -la "/Users/norikakizawa/Projects/n0ri.com/content/posts/$FOLDER_NAME/"
```

**Final path format**:
```
/Users/norikakizawa/Projects/n0ri.com/content/posts/[title-in-lowercase]/
├── index.mdx
└── photos/
    ├── image-1.jpg
    └── image-2.jpg
```

**Verification checklist**:
- [ ] Valid YAML frontmatter (no syntax errors)
- [ ] Title clean and appropriate length (no colons)
- [ ] Date in YYYY-MM-DD format
- [ ] 2-5 relevant tags
- [ ] Markdown properly formatted
- [ ] Blockquotes use `>` prefix
- [ ] Headings hierarchical (H1 → H2 → H3)
- [ ] Lists properly indented
- [ ] Links use `[text](url)` syntax
- [ ] Images downloaded to `./photos/` folder
- [ ] Images have descriptive alt text (from OCR)
- [ ] Images wrapped in centered div styling
- [ ] All URLs converted to markdown links
- [ ] File moved to `/Users/norikakizawa/Projects/n0ri.com/content/posts/[title]/index.mdx`

## Example Usage

**User request**: "Convert my Notion page about San Francisco startups to a blog post"

**Execution**:

1. **Access content** (via MCP or paste):
```
Building Startups in San Francisco

I moved to SF to join the startup ecosystem. Check out Y Combinator's website: https://www.ycombinator.com

[Image: YC Logo in the office]

The Tech Scene
People are building innovative companies. Read more at TechCrunch: https://techcrunch.com
```

2. **Convert to markdown with images and URLs**:
```markdown
# Building Startups in San Francisco

I moved to SF to join the startup ecosystem. Check out [Y Combinator](https://www.ycombinator.com)

<div style={{ textAlign: 'center', margin: '2rem 0' }}>
  <div style={{ display: 'inline-block', width: '75%', maxWidth: '700px' }}>
![Y Combinator office logo](./photos/yc-office-logo.jpg)
  </div>
</div>

## The Tech Scene

People are building innovative companies. Read more at [TechCrunch](https://techcrunch.com)
```

**Image processing**:
- Download image from Notion
- OCR/analyze: "Y Combinator logo on office wall"
- Save as `./photos/yc-office-logo.jpg`
- Generate alt text: "Y Combinator office logo"

3. **Extract metadata**:
- Title: "Building Startups in San Francisco"
- Date: "2025-01-12"
- Suggested tags: `technology, entrepreneurship, SanFrancisco, startups, community`

4. **Confirm tags with user**:
"I suggest these tags: technology, entrepreneurship, SanFrancisco, startups, community. Would you like to modify?"

5. **Build MDX**:
```bash
python scripts/mdx_builder.py \
  --title "Building Startups in San Francisco" \
  --date "2025-01-12" \
  --tags "entrepreneurship,startups,SanFrancisco" \
  --content "$CONTENT" \
  --output "blog-post.mdx"
```

6. **Move to blog directory with images**:
```bash
# Create folder structure
mkdir -p "/Users/norikakizawa/Projects/n0ri.com/content/posts/building-startups-in-san-francisco/photos"

# Move MDX file
mv "blog-post.mdx" "/Users/norikakizawa/Projects/n0ri.com/content/posts/building-startups-in-san-francisco/index.mdx"

# Move images
mv "yc-office-logo.jpg" "/Users/norikakizawa/Projects/n0ri.com/content/posts/building-startups-in-san-francisco/photos/"
```

7. **Final output**:
```mdx
---
title: Building Startups in San Francisco
date: 2025-01-12
tags:
  - entrepreneurship
  - startups
  - SanFrancisco
---

# Building Startups in San Francisco

I moved to SF to join the startup ecosystem...
```

**Final path**: `/Users/norikakizawa/Projects/n0ri.com/content/posts/building-startups-in-san-francisco/index.mdx`

8. **Verify build**:
```bash
cd /Users/norikakizawa/Projects/n0ri.com
npm run develop
```

Check for any YAML or build errors. If successful, the new post is ready!

## Quick Reference

### When to Use This Skill

Trigger this skill when user asks to:
- "Convert my Notion page to MDX"
- "Export Notion as blog post"
- "Transform this Notion content to markdown"
- "Create a blog post from my Notion page"
- "Convert Notion to MDX with frontmatter"

### Script Usage

**Content Analyzer**:
```bash
python scripts/content_analyzer.py \
  --content "Your markdown content here" \
  --max-tags 5
```

**MDX Builder**:
```bash
python scripts/mdx_builder.py \
  --title "Post Title" \
  --date "2025-01-12" \
  --tags "tag1,tag2,tag3" \
  --content "Your markdown content" \
  --output "path/to/output.mdx"
```

**Image Processor**:
```bash
python scripts/image_processor.py \
  --url "https://notion.so/image.jpg" \
  --output-dir "./photos" \
  --alt-text "Descriptive alt text" \
  --filename "custom-name.jpg"
```

**URL Converter**:
```bash
# Convert single URL
python scripts/url_converter.py \
  --url "https://ycombinator.com" \
  --link-text "Y Combinator"

# Convert all URLs in text
python scripts/url_converter.py \
  --text "Check out https://ycombinator.com for more info"
```

### Tag Format Guidelines

Based on user's blog style:

**Generic themes** (lowercase):
- `technology`, `personal`, `entrepreneurship`, `finance`

**Proper nouns** (PascalCase or as-written):
- `SanFrancisco`, `NetworkSchool`, `EntrepreneurFirst`, `Singapore`

**Specific topics** (lowercase, hyphenated):
- `web-development`, `machine-learning`, `crypto-trading`

## Resources

### scripts/content_analyzer.py
Analyzes markdown content and suggests relevant tags based on:
- Keyword frequency analysis (weighted by position)
- Theme detection using domain keyword dictionaries
- Proper noun recognition
- Returns 2-5 suggested tags

### scripts/mdx_builder.py
Constructs MDX files with proper YAML frontmatter:
- Validates title, date, and tags
- Sanitizes title (removes colons to prevent YAML errors)
- Ensures correct YAML indentation
- Creates output directory if needed
- Returns formatted MDX file

### scripts/image_processor.py
Downloads and processes images from Notion:
- Downloads images from URLs
- Generates safe filenames (lowercase, hyphenated)
- Creates alt text from context or OCR
- Wraps images with centered div styling
- Outputs formatted MDX with proper styling

### scripts/url_converter.py
Converts URLs to markdown links:
- Extracts all URLs from text
- Generates descriptive link text from domain or context
- Maps common domains to friendly names
- Converts plain URLs to markdown format `[text](url)`
- Handles both single URLs and bulk conversion

### references/notion_elements_mapping.md
Comprehensive guide for converting Notion block types to Markdown:
- Text formatting (bold, italic, code)
- Headings (H1, H2, H3)
- Lists (bulleted, numbered, nested)
- Blocks (quotes, code blocks, callouts)
- Links and special elements
- Edge cases and unsupported features

Load this when handling complex Notion formatting or encountering conversion issues.

### references/tag_extraction_guide.md
Deep dive into tag extraction methodology:
- Algorithm explanation (keyword extraction, theme detection)
- Customization options (weights, thresholds, domains)
- Tag best practices (naming conventions, quantity)
- Examples and troubleshooting
- Manual override workflows

Load this when customizing tag suggestions or improving tag quality.

### assets/mdx_template.txt
Template file showing the expected MDX blog post format with frontmatter, headings, lists, code blocks, and standard markdown elements.

## Tips for Best Results

1. **Preserve structure**: Maintain heading hierarchy from Notion
2. **Clean content**: Remove unnecessary empty lines or formatting
3. **Review tags**: Always confirm suggested tags with user
4. **Handle images**: Download, OCR for alt text, place in `./photos/` folder
5. **Convert URLs**: Extract all URLs and convert to markdown links with descriptive text
6. **Iterate if needed**: Allow user to modify metadata and rebuild
7. **Validate output**: Check YAML frontmatter before saving

## Common Issues

**Issue**: Notion MCP not available
**Solution**: Use fallback method (paste content)

**Issue**: Tags too generic
**Solution**: Review content_analyzer.py domain keywords or manually refine

**Issue**: Invalid YAML frontmatter
**Solution**: Use mdx_builder.py script (ensures correct formatting)

**Issue**: Missing title
**Solution**: Check for H1 in content, or prompt user

**Issue**: Complex Notion elements
**Solution**: Read notion_elements_mapping.md for conversion guidance

**Issue**: Images not displaying in blog
**Solution**: Verify images are in `./photos/` folder relative to index.mdx, check file paths

**Issue**: Image alt text not descriptive
**Solution**: Use OCR or vision model to analyze image content and generate meaningful description

**Issue**: URLs not converted to links
**Solution**: Extract all URLs (plain text or Notion links) and convert to `[text](url)` format

**Issue**: Link text generic or missing
**Solution**: Use domain name or fetch page title as link text (e.g., "ycombinator.com" or "Y Combinator")

**Issue**: Colon in title breaks YAML
**Solution**: mdx_builder.py automatically replaces colons with ` -`
