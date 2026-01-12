# notion-to-mdx

A tutorial for building your first Claude Code skill that converts Notion pages to MDX blog posts. This repository demonstrates how to create a skill with Python scripts, MCP integration, and automated workflows.

## What You'll Learn

This tutorial teaches you how to build a Claude Code skill that:
1. Integrates with Notion via MCP (Model Context Protocol)
2. Converts Notion content to MDX format
3. Extracts metadata and suggests tags
4. Processes images and URLs
5. Generates properly formatted blog posts

## Setting Up Notion MCP with Claude Code

### Prerequisites
- Claude Code installed
- A Notion account
- Python 3.7+

### Step 1: Create a Notion Integration

1. Go to [https://www.notion.so/profile/integrations](https://www.notion.so/profile/integrations)
2. Click "New integration"
3. Give your integration a name (e.g., "Claude Code MCP")
4. Select the workspace you want to connect
5. Set the capabilities you need (Read content, Update content, etc.)
6. Click "Submit" to create the integration
7. Copy the "Internal Integration Token" - you'll need this for authentication

### Step 2: Share Pages with Your Integration

For the integration to access your Notion pages:
1. Open the Notion page you want to access
2. Click the "..." menu in the top right
3. Scroll down and click "Add connections"
4. Select your integration from the list

### Step 3: Configure Claude Code MCP

Add the Notion MCP server to your Claude Code configuration:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/notion-mcp-server"],
      "env": {
        "NOTION_API_KEY": "your-integration-token-here"
      }
    }
  }
}
```

Replace `your-integration-token-here` with the token you copied in Step 1.

### Step 4: Verify the Connection

Restart Claude Code and verify the Notion MCP is connected by asking:
```
Can you list my Notion pages?
```

## Quick Start

Once Notion MCP is set up, ask Claude to convert your Notion content:
```
Convert my Notion page about [topic] to a blog post
```

The skill will:
1. Access your Notion content via MCP
2. Convert to MDX with proper markdown formatting
3. Extract metadata (title, date)
4. Suggest relevant tags using content analysis
5. Download and process images with alt text
6. Convert URLs to markdown links
7. Generate YAML frontmatter
8. Save to your blog directory

## Output Format

```mdx
---
title: Your Post Title
date: 2025-01-12
tags:
  - technology
  - startups
---

# Your Post Title

Your content with properly formatted markdown, images, and links...
```

## Structure

```
notion-to-mdx/
├── scripts/
│   ├── content_analyzer.py   # Analyzes content and suggests tags
│   ├── mdx_builder.py        # Builds MDX files with frontmatter
│   ├── image_processor.py    # Downloads and processes images
│   └── url_converter.py      # Converts URLs to markdown links
├── references/
│   ├── notion_elements_mapping.md  # Notion → Markdown conversion guide
│   └── tag_extraction_guide.md     # Tag suggestion methodology
├── assets/
│   └── mdx_template.txt      # MDX template reference
└── SKILL.md                  # Complete documentation
```

## Requirements

- Python 3.7+
- Optional: Notion MCP server for direct integration

## Example

**Input (Notion):**
```
Building Startups in SF

I moved to San Francisco. Check out https://www.ycombinator.com

[Image: YC office]

The tech scene is amazing!
```

**Output (MDX):**
```mdx
---
title: Building Startups in SF
date: 2025-01-12
tags:
  - entrepreneurship
  - SanFrancisco
  - startups
---

# Building Startups in SF

I moved to San Francisco. Check out [Y Combinator](https://www.ycombinator.com)

<div style={{ textAlign: 'center', margin: '2rem 0' }}>
  <div style={{ display: 'inline-block', width: '75%', maxWidth: '700px' }}>
![Y Combinator office](./photos/yc-office.jpg)
  </div>
</div>

## The tech scene is amazing!
```

## Documentation

See [SKILL.md](notion-to-mdx/SKILL.md) for complete workflow documentation, script usage, and troubleshooting.

## License

MIT
