# PDF-to-Markdown prompt

(authored by agents unless marked 🧑)

Convert the entire attached PDF to clean Markdown.

Return only the Markdown document. Do not add a preface, summary, commentary,
or enclosing code fence.

Preserve all substantive wording and the PDF's reading order. On multi-column
pages, read each column from top to bottom before moving right. Do not summarize,
omit, expand, translate, or invent content. Preserve the title, authors,
abstract, headings, paragraphs, lists, tables, equations, figure and table
captions, footnotes, endnotes, acknowledgments, and references.

Use Markdown headings, lists, tables, links, and LaTeX math where they preserve
the source accurately. Remove repeated page headers, repeated page footers,
and standalone page numbers. Join words split only by line-wrap hyphenation,
but preserve intentional hyphens. Preserve figure numbers and captions without
inventing visual details. Write `[unreadable]` for content that cannot be read;
never guess.
