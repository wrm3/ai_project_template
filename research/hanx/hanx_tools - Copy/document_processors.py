"""
Document processors for different file types.
Supports PDF, HTML, Markdown, and plain text files.
"""
import os
from typing import Dict, Any, List
from pathlib import Path
import json
from bs4 import BeautifulSoup
import markdown
import PyPDF2
import docx
import csv
import yaml
from datetime import datetime

class DocumentProcessor:
    """Base class for document processors."""
    def __init__(self, base_metadata: Dict[str, Any] = None):
        self.base_metadata = base_metadata or {}

    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        """Process a document and return its content and metadata."""
        raise NotImplementedError

    def _get_base_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get base metadata for a file."""
        path = Path(file_path)
        metadata = self.base_metadata.copy()
        metadata.update({
            "source": str(path),
            "file_name": path.name,
            "file_type": path.suffix.lower()[1:],
            "created_at": datetime.fromtimestamp(path.stat().st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(path.stat().st_mtime).isoformat(),
        })
        return metadata

class PDFProcessor(DocumentProcessor):
    """Process PDF documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        
        with open(file_path, 'rb') as file:
            pdf = PyPDF2.PdfReader(file)
            
            # Extract text
            content = ""
            for page in pdf.pages:
                content += page.extract_text() + "\n"
            
            # Get PDF metadata
            if pdf.metadata:
                metadata.update({
                    "title": pdf.metadata.get("/Title", ""),
                    "author": pdf.metadata.get("/Author", ""),
                    "subject": pdf.metadata.get("/Subject", ""),
                    "keywords": pdf.metadata.get("/Keywords", ""),
                })
            
        return content.strip(), metadata

class HTMLProcessor(DocumentProcessor):
    """Process HTML documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            # Extract metadata from meta tags
            meta_tags = soup.find_all('meta')
            for tag in meta_tags:
                name = tag.get('name', '').lower()
                content = tag.get('content', '')
                if name and content:
                    metadata[name] = content
            
            # Extract title
            if soup.title:
                metadata['title'] = soup.title.string
            
            # Extract main content (remove script, style, etc.)
            for tag in soup(['script', 'style', 'meta', 'link']):
                tag.decompose()
            
            content = soup.get_text(separator='\n')
            
        return content.strip(), metadata

class MarkdownProcessor(DocumentProcessor):
    """Process Markdown documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # Check for YAML frontmatter
            if content.startswith('---'):
                end_idx = content.find('---', 3)
                if end_idx != -1:
                    frontmatter = content[3:end_idx]
                    try:
                        yaml_metadata = yaml.safe_load(frontmatter)
                        if yaml_metadata:
                            metadata.update(yaml_metadata)
                        content = content[end_idx + 3:]
                    except yaml.YAMLError:
                        pass
            
            # Convert markdown to plain text
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.get_text(separator='\n')
            
        return content.strip(), metadata

class DocxProcessor(DocumentProcessor):
    """Process Word documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        
        doc = docx.Document(file_path)
        
        # Extract core properties
        core_props = doc.core_properties
        if core_props:
            metadata.update({
                "title": core_props.title or "",
                "author": core_props.author or "",
                "subject": core_props.subject or "",
                "keywords": core_props.keywords or "",
                "created": core_props.created.isoformat() if core_props.created else "",
                "modified": core_props.modified.isoformat() if core_props.modified else "",
            })
        
        # Extract text
        content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        return content.strip(), metadata

class TextProcessor(DocumentProcessor):
    """Process plain text documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        return content.strip(), metadata

class CSVProcessor(DocumentProcessor):
    """Process CSV documents."""
    def process(self, file_path: str) -> tuple[str, Dict[str, Any]]:
        metadata = self._get_base_metadata(file_path)
        content_lines = []
        
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            metadata['headers'] = headers
            
            for row in reader:
                # Convert each row to a descriptive text format
                row_text = " | ".join([f"{k}: {v}" for k, v in row.items()])
                content_lines.append(row_text)
        
        return "\n".join(content_lines), metadata

def get_processor(file_path: str, base_metadata: Dict[str, Any] = None) -> DocumentProcessor:
    """Get the appropriate processor for a file based on its extension."""
    ext = Path(file_path).suffix.lower()
    processors = {
        '.pdf': PDFProcessor,
        '.html': HTMLProcessor,
        '.htm': HTMLProcessor,
        '.md': MarkdownProcessor,
        '.markdown': MarkdownProcessor,
        '.docx': DocxProcessor,
        '.txt': TextProcessor,
        '.csv': CSVProcessor,
    }
    
    processor_class = processors.get(ext, TextProcessor)
    return processor_class(base_metadata)

def process_document(file_path: str, base_metadata: Dict[str, Any] = None) -> tuple[str, Dict[str, Any]]:
    """Process a document and return its content and metadata."""
    processor = get_processor(file_path, base_metadata)
    return processor.process(file_path) 