# Notion Elements to Markdown Mapping

Comprehensive guide for converting Notion block types to Markdown syntax for MDX blog posts.

## Table of Contents

1. [Text Formatting](#text-formatting)
2. [Headings](#headings)
3. [Lists](#lists)
4. [Blocks](#blocks)
5. [Links](#links)
6. [Code](#code)
7. [Edge Cases](#edge-cases)
8. [Not Supported](#not-supported)

## Text Formatting

### Bold
- **Notion**: Bold text button or `Cmd+B`
- **Markdown**: `**bold text**`
- **Example**: `**This is bold**` → **This is bold**

### Italic
- **Notion**: Italic text button or `Cmd+I`
- **Markdown**: `*italic text*`
- **Example**: `*This is italic*` → *This is italic*

### Inline Code
- **Notion**: Inline code button or `` `code` ``
- **Markdown**: `` `code` ``
- **Example**: `` `const x = 5` `` → `const x = 5`

### Strikethrough
- **Notion**: Strikethrough button or `Cmd+Shift+S`
- **Markdown**: `~~strikethrough~~`
- **Example**: `~~removed text~~` → ~~removed text~~

### Underline
- **Notion**: Underline button
- **Markdown**: Not supported in standard Markdown
- **Conversion**: Remove underline formatting or use bold/italic instead

### Mixed Formatting
Combine multiple formats:
- **Notion**: Bold + Italic
- **Markdown**: `***bold and italic***`
- **Example**: `***This is both***` → ***This is both***

## Headings

### Heading 1
- **Notion**: `/heading1` or `Cmd+Option+1`
- **Markdown**: `# Heading 1`
- **Note**: Use sparingly; typically only for main title

### Heading 2
- **Notion**: `/heading2` or `Cmd+Option+2`
- **Markdown**: `## Heading 2`
- **Use**: Main sections

### Heading 3
- **Notion**: `/heading3` or `Cmd+Option+3`
- **Markdown**: `### Heading 3`
- **Use**: Subsections

### Heading Hierarchy
Maintain proper hierarchy:
```markdown
# Main Title
## Section
### Subsection
#### Sub-subsection (use sparingly)
```

## Lists

### Bulleted List
- **Notion**: `/bullet` or `-` at line start
- **Markdown**: `- item` or `* item`
- **Example**:
  ```markdown
  - First item
  - Second item
  - Third item
  ```

### Numbered List
- **Notion**: `/numbered` or `1.` at line start
- **Markdown**: `1. item`
- **Example**:
  ```markdown
  1. First step
  2. Second step
  3. Third step
  ```

### Nested Lists
- **Notion**: Tab to indent, Shift+Tab to outdent
- **Markdown**: Use 2 spaces for each indentation level
- **Example**:
  ```markdown
  - Main item
    - Nested item
    - Another nested item
      - Deeply nested
  - Back to main level
  ```

### To-Do List / Checkboxes
- **Notion**: `/todo` checkbox list
- **Markdown**: `- [ ]` unchecked, `- [x]` checked
- **Example**:
  ```markdown
  - [ ] Incomplete task
  - [x] Completed task
  ```

## Blocks

### Blockquote
- **Notion**: `/quote` block
- **Markdown**: `> quote text`
- **Example**:
  ```markdown
  > This is a quote
  > It can span multiple lines
  ```

### Callout Box
- **Notion**: `/callout` colored box with icon
- **Markdown**: Convert to blockquote with emoji
- **Conversion**:
  - Notion: 💡 Callout with light bulb
  - Markdown: `> 💡 Important note here`
- **Example**:
  ```markdown
  > **Key insight:** This is important information
  ```

### Divider / Horizontal Rule
- **Notion**: `/divider`
- **Markdown**: `---` or `***`
- **Example**:
  ```markdown
  Content above

  ---

  Content below
  ```

### Toggle / Accordion
- **Notion**: `/toggle` collapsible section
- **Markdown**: Not supported; convert to regular heading + content
- **Conversion**:
  ```markdown
  ### Toggle Title

  Content that was inside toggle
  ```

## Links

### Inline Link
- **Notion**: `Cmd+K` or paste URL
- **Markdown**: `[text](url)`
- **Example**: `[Visit Claude](https://claude.ai)` → [Visit Claude](https://claude.ai)

### External URL
- **Notion**: Paste URL
- **Markdown**: `[descriptive text](https://example.com)`
- **Best Practice**: Always use descriptive text, not bare URLs

### Page Links (Internal Notion)
- **Notion**: `@page-name` reference
- **Markdown**: Cannot preserve Notion internal links
- **Conversion**: Convert to plain text or remove

## Code

### Inline Code
- **Notion**: `` `code` ``
- **Markdown**: `` `code` ``
- **Example**: `` `const x = 5` ``

### Code Block
- **Notion**: `/code` block with language selection
- **Markdown**: ` ```language ` (triple backticks with language)
- **Example**:
  ````markdown
  ```javascript
  function hello() {
    console.log("Hello world");
  }
  ```
  ````

### Supported Languages
Common languages for syntax highlighting:
- `javascript`, `typescript`, `jsx`, `tsx`
- `python`, `java`, `go`, `rust`
- `html`, `css`, `scss`
- `bash`, `shell`, `sh`
- `json`, `yaml`, `markdown`

## Edge Cases

### Empty Lines
- **Notion**: Single line breaks
- **Markdown**: Use blank line for paragraph separation
- **Conversion**: Preserve blank lines between paragraphs

### Multiple Paragraphs in Blockquote
```markdown
> First paragraph of quote
>
> Second paragraph of quote
```

### Nested Blockquotes
```markdown
> Level 1 quote
> > Level 2 quote (rarely needed)
```

### Mixed List Types
```markdown
1. Numbered item
2. Another numbered
   - Nested bullet
   - Another bullet
3. Back to numbered
```

### Long Lines
- No special handling needed
- Markdown supports long lines
- Let the blog renderer handle line wrapping

## Not Supported

These Notion features cannot be directly converted to Markdown and require special handling:

### Images
- **Notion**: `/image` block
- **Reason**: Per user requirements, images are not handled
- **Action**: Skip or note location for manual addition later

### Embeds (YouTube, Twitter, etc.)
- **Notion**: `/embed` block
- **Markdown**: Not supported
- **Conversion**: Convert to plain link with description

### File Attachments
- **Notion**: `/file` block
- **Markdown**: Not supported
- **Action**: Note the file name for manual handling

### Databases & Tables
- **Notion**: Inline databases and tables
- **Markdown**: Tables are supported but complex databases aren't
- **Simple Table Conversion**:
  ```markdown
  | Column 1 | Column 2 |
  |----------|----------|
  | Data 1   | Data 2   |
  ```
- **Complex Databases**: Extract as list or skip

### Synced Blocks
- **Notion**: Synced content across pages
- **Markdown**: Not supported
- **Action**: Copy content directly

### Columns / Multi-column Layout
- **Notion**: Side-by-side columns
- **Markdown**: Not supported
- **Conversion**: Stack content vertically

### Colors & Backgrounds
- **Notion**: Colored text or background
- **Markdown**: Not supported in basic Markdown
- **Action**: Remove color formatting

### Page Mentions & Backlinks
- **Notion**: `@page` references
- **Markdown**: Not supported
- **Conversion**: Convert to plain text

## Conversion Best Practices

1. **Preserve Intent**: Focus on preserving the meaning and structure, not exact formatting
2. **Simplify**: When in doubt, use simpler Markdown over complex workarounds
3. **Consistency**: Maintain consistent formatting throughout the document
4. **Hierarchy**: Preserve heading hierarchy for proper document structure
5. **Readability**: Prioritize readability in the final Markdown output

## Quick Reference

| Notion Element | Markdown Syntax | Example |
|----------------|-----------------|---------|
| Bold | `**text**` | **bold** |
| Italic | `*text*` | *italic* |
| Inline Code | `` `code` `` | `code` |
| H1 | `# Title` | # Title |
| H2 | `## Section` | ## Section |
| H3 | `### Subsection` | ### Subsection |
| Bullet | `- item` | • item |
| Numbered | `1. item` | 1. item |
| Quote | `> quote` | > quote |
| Link | `[text](url)` | [text](url) |
| Code Block | ` ```lang ` | (fenced code) |
| Divider | `---` | --- |
