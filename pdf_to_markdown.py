import tabula
import camelot
import pandas as pd
from pathlib import Path
import re
import csv
import pdfplumber
import sys

def analyze_text_style(text, font_size, font_name):
    """Analyze text style to determine if it's a heading, link, or regular text."""
    return {
        'text': text,
        'font_size': font_size,
        'font_name': font_name,
        'is_bold': 'bold' in str(font_name).lower() if font_name else False,
        'is_italic': 'italic' in str(font_name).lower() if font_name else False
    }

def is_heading(text_info, prev_text_info):
    """Enhanced heading detection based on text style and content."""
    text = text_info['text'].strip()
    
    # Check text length and ending
    if len(text) < 50 and not text.endswith('.'):
        # Check if it's not a bullet point
        if not text.startswith('•'):
            # Check if it's not a continuation
            if not prev_text_info or not prev_text_info['text'].strip().endswith(('.', ':', ';')):
                # Check font characteristics
                if text_info.get('is_bold', False) or text_info.get('font_size', 0) > 12:
                    return True
    return False

def is_link(text_info):
    """Enhanced link detection based on text style and patterns."""
    text = text_info['text'].strip()
    
    # Common link patterns
    link_patterns = [
        r'https?://\S+',  # URLs
        r'www\.\S+',      # www links
        r'\S+\.(com|org|net|edu|gov|io)\S*',  # Common TLDs
        r'\S+\.(pdf|doc|docx|xls|xlsx|txt)\S*',  # Common file extensions
        r'click here',  # Common link text
        r'read more',
        r'learn more',
        r'view',
        r'download',
        r'link',
        r'url',
        r'website',
        r'page',
        r'site',
        r'resource'
    ]
    
    # Check if text matches link patterns
    for pattern in link_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
            
    # Check if text is styled like a link (bold or larger font)
    if text_info.get('is_bold', False) or text_info.get('font_size', 0) > 12:
        return True
        
    return False

def format_links(text, text_info):
    """Format text containing links into Markdown link syntax."""
    # URL pattern
    url_pattern = r'(https?://\S+|www\.\S+|\S+\.(com|org|net|edu|gov|io|pdf|doc|docx|xls|xlsx|txt)\S*)'
    
    def replace_link(match):
        url = match.group(1)
        # If it's a www link without http(s), add https://
        if url.startswith('www.'):
            url = 'https://' + url
        return f'[{url}]({url})'
    
    # If the text is a link but doesn't contain a URL, use the text as the link text
    if is_link(text_info) and not re.search(url_pattern, text):
        # Try to find a URL in the surrounding context
        context = text_info.get('context', '')
        url_match = re.search(url_pattern, context)
        if url_match:
            url = url_match.group(1)
            if url.startswith('www.'):
                url = 'https://' + url
            return f'[{text}]({url})'
        return f'[{text}](#)'  # Use # as placeholder URL
        
    return re.sub(url_pattern, replace_link, text)

def markdownify_links(text):
    """Aggressively convert all URLs in text to markdown links."""
    url_pattern = r'(https?://\S+|www\.\S+|\S+\.(com|org|net|edu|gov|io|pdf|doc|docx|xls|xlsx|txt)\S*)'
    def repl(match):
        url = match.group(1)
        if url.startswith('www.'):
            url = 'https://' + url
        return f'[{url}]({url})'
    return re.sub(url_pattern, repl, text)

def format_markdown(text_blocks):
    """Format text blocks into proper Markdown structure."""
    formatted_lines = []
    prev_text_info = None
    current_paragraph = []
    
    for block in text_blocks:
        text = block['text'].strip()
        if not text:
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            formatted_lines.append('')
            continue
        
        # Aggressively format links in the text
        text = markdownify_links(text)
        
        # Check if text is a heading
        if is_heading(block, prev_text_info):
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            formatted_lines.append(f"## {text}")
        # Check if text is a bullet point
        elif text.startswith('•'):
            if current_paragraph:
                formatted_lines.append(' '.join(current_paragraph))
                current_paragraph = []
            formatted_lines.append(text)
        # Regular paragraph
        else:
            current_paragraph.append(text)
        
        prev_text_info = block
    
    # Add any remaining paragraph
    if current_paragraph:
        formatted_lines.append(' '.join(current_paragraph))
    
    return '\n\n'.join(formatted_lines)

def clean_table(df):
    """Clean and format the table data."""
    # Remove empty rows and columns
    df = df.dropna(how='all').dropna(axis=1, how='all')
    
    # Clean cell values
    for col in df.columns:
        df[col] = df[col].astype(str).str.strip()
    
    # Remove rows where all cells are empty or just whitespace
    df = df[~df.apply(lambda x: x.str.strip().eq('').all(), axis=1)]
    
    return df

def detect_header_row(df):
    """Heuristically detect the best header row in a DataFrame."""
    if df.empty:
        return None
        
    # Check first 3 rows
    for i in range(min(3, len(df))):
        row = df.iloc[i]
        # Count non-empty cells
        non_empty = sum(bool(str(cell).strip()) for cell in row)
        # Count string cells
        string_cells = sum(isinstance(cell, str) for cell in row)
        # Check if row has unique values
        unique_values = len(set(str(cell).strip() for cell in row))
        
        # Good header criteria:
        # 1. At least half the cells are non-empty
        # 2. At least half the cells are strings
        # 3. Most values are unique
        if (non_empty >= len(row) // 2 and 
            string_cells >= len(row) // 2 and 
            unique_values >= len(row) // 2):
            return i
    return None

def table_to_markdown(df):
    """Convert a pandas DataFrame to Markdown table format."""
    if df.empty:
        return ''
    
    # Clean the table
    df = clean_table(df)
    
    # Detect header row
    header_idx = detect_header_row(df)
    if header_idx is not None:
        # Use detected header
        df2 = df.copy()
        df2.columns = df2.iloc[header_idx]
        df2 = df2[(header_idx+1):]
    else:
        # Use generic headers
        df2 = df.copy()
        df2.columns = [f'Column {i+1}' for i in range(len(df2.columns))]
    
    # Aggressively convert links in every cell
    for col in df2.columns:
        df2[col] = df2[col].astype(str).apply(markdownify_links)
    
    # Convert to markdown
    markdown = df2.to_markdown(index=False)
    return markdown

def extract_tables_tabula(pdf_path):
    """Extract tables using tabula-py with multiple methods."""
    tables = []
    
    # Try lattice mode (for tables with borders)
    try:
        lattice_tables = tabula.read_pdf(
            pdf_path,
            pages='all',
            multiple_tables=True,
            lattice=True,
            guess=True,
            pandas_options={'header': None}
        )
        tables.extend(lattice_tables)
    except Exception as e:
        print(f"Lattice mode error: {str(e)}")
    
    # Try stream mode (for tables without borders)
    try:
        stream_tables = tabula.read_pdf(
            pdf_path,
            pages='all',
            multiple_tables=True,
            stream=True,
            guess=True,
            pandas_options={'header': None}
        )
        tables.extend(stream_tables)
    except Exception as e:
        print(f"Stream mode error: {str(e)}")
    
    return tables

def extract_tables_camelot(pdf_path):
    """Extract tables using camelot with multiple methods."""
    tables = []
    
    # Try lattice mode
    try:
        lattice_tables = camelot.read_pdf(
            pdf_path,
            pages='all',
            flavor='lattice',
            suppress_stdout=True
        )
        tables.extend([table.df for table in lattice_tables])
    except Exception as e:
        print(f"Camelot lattice mode error: {str(e)}")
    
    # Try stream mode
    try:
        stream_tables = camelot.read_pdf(
            pdf_path,
            pages='all',
            flavor='stream',
            suppress_stdout=True
        )
        tables.extend([table.df for table in stream_tables])
    except Exception as e:
        print(f"Camelot stream mode error: {str(e)}")
    
    return tables

def extract_and_format_pdf(pdf_path, md_path):
    """Extract text and tables from PDF and format as Markdown in original order."""
    markdown_blocks = []
    
    print("Extracting tables using multiple methods...")
    
    # Extract tables using both libraries
    tabula_tables = extract_tables_tabula(pdf_path)
    camelot_tables = extract_tables_camelot(pdf_path)
    
    # Combine and deduplicate tables
    all_tables = tabula_tables + camelot_tables
    print(f"Found {len(all_tables)} potential tables")
    
    # Process each table
    for i, table in enumerate(all_tables, 1):
        print(f"Processing table {i}...")
        if not table.empty:
            # Insert heading before each table
            markdown_blocks.append(f"## Table {i}")
            # Convert table to markdown
            md_table = table_to_markdown(table)
            if md_table.strip():
                markdown_blocks.append(md_table)
                print(f"Table {i} converted to markdown")
                # Save the first table as CSV for debugging
                if i == 1:
                    table.to_csv('first_table_debug.csv', index=False)
                    print("First table saved as first_table_debug.csv")
    
    # Join all content with proper spacing
    markdown_content = "\n\n".join(markdown_blocks)
    
    # Write to file
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"Markdown content extracted and saved to {md_path}")

def pdf_to_markdown(pdf_path, output_path):
    md_lines = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            # Extract tables
            tables = page.extract_tables()
            if tables:
                for table in tables:
                    md_lines.append(table_to_markdown(table))
                    md_lines.append("")
            # Extract text
            text = page.extract_text()
            if text:
                for line in text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    if is_heading(line):
                        md_lines.append(f"# {line}")
                    elif re.match(r"^[-*•] ", line):
                        md_lines.append(f"- {line[2:].strip()}")
                    else:
                        md_lines.append(line)
            md_lines.append("\n\\pagebreak\n")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
    print(f"Converted '{pdf_path}' to Markdown with structure in '{output_path}'")

def main():
    pdf_path = str(Path.home() / "Downloads" / "q-extract-tables-from-pdf.pdf")
    md_path = str(Path.cwd() / "q-pdf-to-markdown.md")
    
    extract_and_format_pdf(pdf_path, md_path)

if __name__ == "__main__":
    main() 