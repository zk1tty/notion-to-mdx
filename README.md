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
- Claude Code CLI installed
- A Notion account
- Python 3.7+

### Important: Claude Code vs Claude Desktop Authentication

**Note:** Authentication for Claude Code CLI is different from Claude Desktop or Claude.ai web interface. Each uses separate authentication systems and credentials. This guide is specifically for **Claude Code CLI**.

### Step 1: Add Notion MCP Server

Add the Notion MCP server to your Claude Code configuration:

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

This adds the Notion MCP server but doesn't authenticate yet.

### Step 2: Authenticate with Notion

![Connecting Claude Code to Notion MCP](assets/conenct%20Claude%20Code%20to%20Notion%20MCP.gif)

To connect Claude Code to your Notion workspace, run the authentication command:

```bash
/mcp
```

This will:
1. Display a list of MCP servers that need authentication
2. Select "notion" from the list and press Enter
3. Automatically open a browser window
4. Prompt you to log in to your Notion account
5. Ask you to select which workspace to connect
6. Complete the OAuth authentication flow

After successful authentication, you'll see:
```
Authentication successful. Reconnected to notion.
```

### Step 3: Verify the Connection

Verify the Notion MCP is connected:

```bash
claude mcp list
```

You should see:
```
notion: https://mcp.notion.com/mcp (HTTP) - ✓ Connected
```

You can also verify by asking Claude Code:
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
