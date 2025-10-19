# File Processors Tool

The `file_processors.py` provides utilities for working with various file formats, including Word documents, Excel spreadsheets, CSV files, HTML, and PDFs.

## Word Document Processing

```python
from tools.file_processors import WordProcessor

# Read a Word document
content = WordProcessor.read_docx('document.docx')
print(content)

# Create a new document
WordProcessor.create_docx(
    'new.docx',
    content=['Paragraph 1', 'Paragraph 2'],
    title='Document Title'
)

# Add content to existing document
WordProcessor.add_to_docx('existing.docx', 'New content')

# Extract tables from a document
tables = WordProcessor.extract_tables('document.docx')
for table in tables:
    print(table)  # Each table is a list of rows
```

## Excel Processing

```python
from tools.file_processors import ExcelProcessor
import pandas as pd

# Read an Excel file
df = ExcelProcessor.read_excel('data.xlsx', sheet_name='Sheet1')
print(df.head())

# Create a new Excel file
data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
ExcelProcessor.create_excel('new.xlsx', data)

# Append data to existing file
ExcelProcessor.append_excel('existing.xlsx', data, sheet_name='Sheet2')

# Read specific columns
df = ExcelProcessor.read_excel('data.xlsx', usecols=['Name', 'Age'])

# Read multiple sheets
sheets = ExcelProcessor.read_excel_sheets('data.xlsx', sheet_names=['Sheet1', 'Sheet2'])
for name, df in sheets.items():
    print(f"Sheet: {name}")
    print(df.head())
```

## CSV Processing

```python
from tools.file_processors import CSVProcessor

# Read a CSV file
data = CSVProcessor.read_csv('data.csv')
print(data[:5])  # First 5 rows

# Create a new CSV file
records = [
    {'name': 'John', 'age': 30},
    {'name': 'Jane', 'age': 25}
]
CSVProcessor.create_csv('new.csv', records)

# Append data to existing file
CSVProcessor.append_csv('existing.csv', records)

# Read with specific options
data = CSVProcessor.read_csv(
    'data.csv',
    delimiter=';',
    encoding='latin-1',
    columns=['name', 'age']
)
```

## HTML Processing

```python
from tools.file_processors import HTMLProcessor

# Read HTML file
html_content = HTMLProcessor.read_html('page.html')
print(html_content)

# Parse HTML content
soup = HTMLProcessor.parse_html(html_content)
title = soup.find('title').text
paragraphs = [p.text for p in soup.find_all('p')]

# Create HTML file
HTMLProcessor.create_html(
    'new.html',
    content='<h1>Hello World</h1><p>This is a paragraph.</p>',
    title='My Page'
)

# Extract text from HTML
text = HTMLProcessor.extract_text(html_content)
print(text)

# Extract links from HTML
links = HTMLProcessor.extract_links(html_content)
for link in links:
    print(f"URL: {link['href']}, Text: {link['text']}")
```

## PDF Processing

```python
from tools.file_processors import PDFProcessor

# Read PDF content
text = PDFProcessor.read_pdf('document.pdf')
print(text)

# Extract text from specific pages
text = PDFProcessor.read_pdf('document.pdf', pages=[1, 3, 5])
print(text)

# Extract tables
tables = PDFProcessor.extract_tables('document.pdf')
for i, table in enumerate(tables):
    print(f"Table {i+1}:")
    print(table)

# Extract images
images = PDFProcessor.extract_images('document.pdf', 'output_dir')
print(f"Extracted {len(images)} images")

# Get PDF metadata
metadata = PDFProcessor.get_metadata('document.pdf')
print(f"Author: {metadata.get('Author')}")
print(f"Creation Date: {metadata.get('CreationDate')}")
```

## Combined Example: Data Extraction Pipeline

```python
from tools.file_processors import WordProcessor, ExcelProcessor, PDFProcessor, CSVProcessor
import os
import pandas as pd

def extract_data_from_directory(directory, output_file):
    """Extract data from various file types in a directory and compile into a single Excel file.
    
    Args:
        directory: Directory containing files to process
        output_file: Path to output Excel file
    """
    all_data = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if filename.endswith('.pdf'):
            # Extract text from PDF
            text = PDFProcessor.read_pdf(filepath)
            all_data.append({'filename': filename, 'content': text, 'type': 'pdf'})
            
            # Extract tables from PDF
            tables = PDFProcessor.extract_tables(filepath)
            if tables:
                for i, table in enumerate(tables):
                    all_data.append({
                        'filename': filename,
                        'content': f"Table {i+1}: {table}",
                        'type': 'pdf_table'
                    })
                    
        elif filename.endswith('.docx'):
            # Extract text from Word document
            text = WordProcessor.read_docx(filepath)
            all_data.append({'filename': filename, 'content': text, 'type': 'docx'})
            
        elif filename.endswith('.xlsx'):
            # Extract data from Excel file
            df = ExcelProcessor.read_excel(filepath)
            all_data.append({
                'filename': filename,
                'content': df.to_string(index=False),
                'type': 'xlsx'
            })
            
        elif filename.endswith('.csv'):
            # Extract data from CSV file
            data = CSVProcessor.read_csv(filepath)
            all_data.append({
                'filename': filename,
                'content': str(data),
                'type': 'csv'
            })
    
    # Convert to DataFrame and save to Excel
    df = pd.DataFrame(all_data)
    ExcelProcessor.create_excel(output_file, df)
    print(f"Data extracted from {len(all_data)} files and saved to {output_file}")

# Example usage
if __name__ == "__main__":
    extract_data_from_directory("./documents", "extracted_data.xlsx")
``` 