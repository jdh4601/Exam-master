#!/usr/bin/env python3
"""Convert password-protected PDF lecture materials to structured markdown."""
from __future__ import annotations

import argparse
import re
import statistics
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Auto-install dependencies
sys.path.insert(0, str(Path(__file__).parent))
from ensure_deps import ensure_dependencies

ensure_dependencies()

import pdfplumber
from pypdf import PdfReader, PdfWriter


@dataclass
class Section:
    """A structural unit of extracted PDF content."""

    level: int  # 0=body, 1=h1, 2=h2, 3=h3
    content: str
    section_type: str  # "heading", "paragraph", "list", "table"


def decrypt_pdf(pdf_path: Path, password: str) -> Path:
    """Decrypt a password-protected PDF and return path to decrypted temp file.

    Args:
        pdf_path: Path to the encrypted PDF.
        password: Password to decrypt.

    Returns:
        Path to a temporary decrypted PDF file.

    Raises:
        ValueError: If the password is incorrect or decryption fails.
    """
    reader = PdfReader(pdf_path)

    if not reader.is_encrypted:
        return pdf_path

    result = reader.decrypt(password)
    if result == 0:
        raise ValueError(f"Wrong password for {pdf_path.name}")

    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    writer.write(tmp)
    tmp.close()
    return Path(tmp.name)


def _compute_font_size_thresholds(
    pages: list[pdfplumber.page.Page],
) -> dict[str, float]:
    """Analyze font sizes across all pages to determine heading thresholds."""
    all_sizes: list[float] = []
    for page in pages:
        words = page.extract_words(extra_attrs=["size"])
        all_sizes.extend(float(w["size"]) for w in words if w.get("size"))

    if not all_sizes:
        return {"body": 12.0, "h1": 20.0, "h2": 16.0, "h3": 14.0}

    median_size = statistics.median(all_sizes)

    return {
        "body": median_size,
        "h1": median_size * 1.6,
        "h2": median_size * 1.3,
        "h3": median_size * 1.15,
    }


def _classify_line_level(
    line_sizes: list[float], thresholds: dict[str, float]
) -> int:
    """Determine heading level from font sizes in a line."""
    if not line_sizes:
        return 0

    avg_size = statistics.mean(line_sizes)

    if avg_size >= thresholds["h1"]:
        return 1
    if avg_size >= thresholds["h2"]:
        return 2
    if avg_size >= thresholds["h3"]:
        return 3
    return 0


_LIST_PATTERN = re.compile(
    r"^\s*(?:[-•●◦▪▸►]|\d+[.)]\s|[a-zA-Z][.)]\s|[ivxIVX]+[.)]\s)"
)
_MONOSPACE_FONTS = {"Courier", "Consolas", "Monaco", "Menlo", "LucidaConsole"}


def _is_list_item(text: str) -> bool:
    return bool(_LIST_PATTERN.match(text))


def _is_monospace(fontnames: list[str]) -> bool:
    for name in fontnames:
        if any(mono.lower() in name.lower() for mono in _MONOSPACE_FONTS):
            return True
    return False


def _extract_table_as_markdown(table: list[list[str | None]]) -> str:
    """Convert a pdfplumber table to a markdown pipe table."""
    if not table or len(table) < 1:
        return ""

    # Clean cells
    cleaned: list[list[str]] = []
    for row in table:
        cleaned.append([(cell or "").strip().replace("\n", " ") for cell in row])

    if not cleaned:
        return ""

    # Build markdown table
    col_count = max(len(row) for row in cleaned)
    lines: list[str] = []

    # Header row
    header = cleaned[0] + [""] * (col_count - len(cleaned[0]))
    lines.append("| " + " | ".join(header) + " |")
    lines.append("| " + " | ".join(["---"] * col_count) + " |")

    # Data rows
    for row in cleaned[1:]:
        padded = row + [""] * (col_count - len(row))
        lines.append("| " + " | ".join(padded) + " |")

    return "\n".join(lines)


def extract_structured_text(
    pdf_path: Path,
    page_range: tuple[int, int] | None = None,
) -> list[Section]:
    """Extract text from PDF with structure detection.

    Args:
        pdf_path: Path to the (decrypted) PDF file.
        page_range: Optional (start, end) 1-based page range.

    Returns:
        List of Section objects representing the document structure.
    """
    sections: list[Section] = []

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages
        if page_range:
            start, end = page_range[0] - 1, page_range[1]
            pages = pages[start:end]

        thresholds = _compute_font_size_thresholds(pages)

        for page in pages:
            # Extract tables first to identify table regions
            tables = page.find_tables()
            table_bboxes = [t.bbox for t in tables]

            for table_obj in tables:
                table_data = table_obj.extract()
                if table_data:
                    md_table = _extract_table_as_markdown(table_data)
                    if md_table:
                        sections.append(Section(0, md_table, "table"))

            # Extract text lines outside of table regions
            lines = page.extract_text_lines(
                return_chars=True,
                strip=True,
            )

            for line_info in lines:
                text = line_info["text"].strip()
                if not text:
                    continue

                # Skip lines inside table bounding boxes
                line_top = line_info["top"]
                line_bottom = line_info.get("bottom", line_top + 10)
                is_in_table = False
                for bbox in table_bboxes:
                    # bbox = (x0, top, x1, bottom)
                    if line_top >= bbox[1] - 2 and line_bottom <= bbox[3] + 2:
                        is_in_table = True
                        break
                if is_in_table:
                    continue

                # Get font metadata from chars
                chars = line_info.get("chars", [])
                sizes = [float(c["size"]) for c in chars if c.get("size")]
                fontnames = [c.get("fontname", "") for c in chars if c.get("fontname")]

                # Classify
                if _is_monospace(fontnames):
                    sections.append(Section(0, text, "code"))
                elif _is_list_item(text):
                    sections.append(Section(0, text, "list"))
                else:
                    level = _classify_line_level(sizes, thresholds)
                    if level > 0:
                        sections.append(Section(level, text, "heading"))
                    else:
                        sections.append(Section(0, text, "paragraph"))

    return sections


def clean_sections(sections: list[Section]) -> list[Section]:
    """Clean extracted sections: remove duplicates, fix encoding artifacts."""
    if not sections:
        return sections

    cleaned: list[Section] = []

    # Detect repeated headers/footers (text appearing on many pages)
    text_counts: dict[str, int] = {}
    for s in sections:
        if s.section_type == "paragraph" and len(s.content) < 80:
            text_counts[s.content] = text_counts.get(s.content, 0) + 1

    page_count = max(1, sum(1 for s in sections if s.section_type == "heading") // 3)
    repeated = {
        t for t, count in text_counts.items() if count > max(2, page_count * 0.5)
    }

    for section in sections:
        content = section.content

        # Skip repeated headers/footers
        if content in repeated and section.section_type == "paragraph":
            continue

        # Fix common encoding artifacts
        content = content.replace("\ufb01", "fi")
        content = content.replace("\ufb02", "fl")
        content = content.replace("\u2019", "'")
        content = content.replace("\u2018", "'")
        content = content.replace("\u201c", '"')
        content = content.replace("\u201d", '"')
        content = content.replace("\u2013", "-")
        content = content.replace("\u2014", "--")

        # Normalize whitespace (but keep intentional line breaks in tables)
        if section.section_type != "table":
            content = re.sub(r"[ \t]+", " ", content)

        cleaned.append(
            Section(section.level, content.strip(), section.section_type)
        )

    return cleaned


def sections_to_markdown(sections: list[Section]) -> str:
    """Render Section list to a markdown string."""
    lines: list[str] = []
    prev_type = ""

    for section in sections:
        match section.section_type:
            case "heading":
                if lines:
                    lines.append("")
                prefix = "#" * section.level
                lines.append(f"{prefix} {section.content}")
                lines.append("")

            case "table":
                if lines and lines[-1] != "":
                    lines.append("")
                lines.append(section.content)
                lines.append("")

            case "list":
                # Normalize list markers to markdown
                text = re.sub(r"^(\s*)[-•●◦▪▸►]\s*", r"\1- ", section.content)
                lines.append(text)

            case "code":
                if prev_type != "code":
                    if lines and lines[-1] != "":
                        lines.append("")
                    lines.append("```")
                lines.append(section.content)

            case "paragraph":
                if prev_type == "code":
                    lines.append("```")
                    lines.append("")
                lines.append(section.content)

        # Close code block if switching away from code
        if prev_type == "code" and section.section_type != "code":
            # Already handled above in paragraph case
            pass

        prev_type = section.section_type

    # Close any trailing code block
    if prev_type == "code":
        lines.append("```")

    result = "\n".join(lines)
    # Normalize multiple blank lines
    result = re.sub(r"\n{3,}", "\n\n", result)
    return result.strip() + "\n"


def convert_single(
    input_path: Path,
    password: str,
    output_path: Path | None = None,
    page_range: tuple[int, int] | None = None,
) -> Path:
    """Convert a single PDF to markdown.

    Args:
        input_path: Path to the PDF file.
        password: PDF password.
        output_path: Output markdown path. Defaults to same name with .md extension.
        page_range: Optional (start, end) 1-based page range.

    Returns:
        Path to the generated markdown file.
    """
    if output_path is None:
        output_path = input_path.with_suffix(".md")

    print(f"Processing: {input_path.name}")

    # Decrypt
    decrypted_path = decrypt_pdf(input_path, password)
    is_temp = decrypted_path != input_path

    try:
        # Extract
        sections = extract_structured_text(decrypted_path, page_range)

        # Clean
        sections = clean_sections(sections)

        # Convert to markdown
        markdown = sections_to_markdown(sections)

        # Write output
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
        print(f"  -> {output_path}")

        return output_path
    finally:
        if is_temp:
            decrypted_path.unlink(missing_ok=True)


def convert_batch(
    input_dir: Path,
    password: str,
    output_dir: Path | None = None,
    page_range: tuple[int, int] | None = None,
) -> list[Path]:
    """Convert all PDFs in a directory to markdown.

    Args:
        input_dir: Directory containing PDF files.
        password: Shared PDF password.
        output_dir: Output directory. Defaults to input_dir.
        page_range: Optional (start, end) 1-based page range.

    Returns:
        List of generated markdown file paths.
    """
    if output_dir is None:
        output_dir = input_dir

    pdf_files = sorted(input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {input_dir}")
        return []

    print(f"Found {len(pdf_files)} PDF files in {input_dir}")
    results: list[Path] = []

    for pdf_path in pdf_files:
        md_path = output_dir / pdf_path.with_suffix(".md").name
        try:
            result = convert_single(pdf_path, password, md_path, page_range)
            results.append(result)
        except Exception as e:
            print(f"  ERROR: {pdf_path.name} - {e}", file=sys.stderr)

    print(f"\nConverted {len(results)}/{len(pdf_files)} files successfully.")
    return results


def _parse_page_range(page_str: str) -> tuple[int, int]:
    """Parse a page range string like '1-10' into a tuple."""
    parts = page_str.split("-")
    if len(parts) == 1:
        n = int(parts[0])
        return (n, n)
    return (int(parts[0]), int(parts[1]))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert password-protected PDF to markdown"
    )
    parser.add_argument("--input", "-i", type=Path, help="Input PDF file path")
    parser.add_argument("--input-dir", type=Path, help="Input directory for batch mode")
    parser.add_argument("--password", "-p", type=str, default="", help="PDF password")
    parser.add_argument("--output", "-o", type=Path, help="Output markdown file path")
    parser.add_argument("--output-dir", type=Path, help="Output directory for batch")
    parser.add_argument("--pages", type=str, help="Page range (e.g., 1-10)")

    args = parser.parse_args()
    page_range = _parse_page_range(args.pages) if args.pages else None

    if args.input_dir:
        convert_batch(args.input_dir, args.password, args.output_dir, page_range)
    elif args.input:
        convert_single(args.input, args.password, args.output, page_range)
    else:
        parser.error("Either --input or --input-dir is required")


if __name__ == "__main__":
    main()
