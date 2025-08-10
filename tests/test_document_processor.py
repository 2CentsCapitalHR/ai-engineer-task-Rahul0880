#!/usr/bin/env python3
"""
Basic tests for the DocumentProcessor class.
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_processor import DocumentProcessor

class TestDocumentProcessor(unittest.TestCase):
    """Test cases for DocumentProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = DocumentProcessor()
    
    def test_init(self):
        """Test DocumentProcessor initialization."""
        self.assertIsInstance(self.processor, DocumentProcessor)
    
    def test_is_docx_file(self):
        """Test .docx file detection."""
        # Test valid .docx file
        self.assertTrue(self.processor.is_docx_file("document.docx"))
        self.assertTrue(self.processor.is_docx_file("contract.DOCX"))
        
        # Test invalid files
        self.assertFalse(self.processor.is_docx_file("document.pdf"))
        self.assertFalse(self.processor.is_docx_file("document.txt"))
        self.assertFalse(self.processor.is_docx_file("document"))
    
    def test_extract_text(self):
        """Test text extraction functionality."""
        # Mock document object
        mock_doc = Mock()
        mock_paragraph = Mock()
        mock_paragraph.text = "This is a test paragraph."
        mock_doc.paragraphs = [mock_paragraph]
        mock_doc.tables = []
        
        with patch('document_processor.Document') as mock_document_class:
            mock_document_class.return_value = mock_doc
            
            # Test text extraction
            result = self.processor.extract_text("test.docx")
            self.assertIn("This is a test paragraph.", result)
    
    def test_extract_structure(self):
        """Test structure extraction functionality."""
        # Mock document object with structure
        mock_doc = Mock()
        mock_heading = Mock()
        mock_heading.text = "Test Heading"
        mock_heading.style.name = "Heading 1"
        
        mock_paragraph = Mock()
        mock_paragraph.text = "Test paragraph"
        mock_paragraph.style.name = "Normal"
        
        mock_doc.paragraphs = [mock_heading, mock_paragraph]
        mock_doc.tables = []
        
        with patch('document_processor.Document') as mock_document_class:
            mock_document_class.return_value = mock_doc
            
            # Test structure extraction
            result = self.processor.extract_structure("test.docx")
            self.assertIn("Test Heading", result["headings"])
            self.assertIn("Test paragraph", result["paragraphs"])
    
    def test_identify_document_type(self):
        """Test document type identification."""
        # Test contract identification
        contract_text = "This is a service agreement between parties"
        doc_type = self.processor.identify_document_type(contract_text)
        self.assertEqual(doc_type, "Contract")
        
        # Test employment agreement identification
        employment_text = "Employment agreement terms and conditions"
        doc_type = self.processor.identify_document_type(employment_text)
        self.assertEqual(doc_type, "Employment Agreement")
        
        # Test unknown document type
        unknown_text = "Random text without legal context"
        doc_type = self.processor.identify_document_type(unknown_text)
        self.assertEqual(doc_type, "Unknown")

if __name__ == '__main__':
    unittest.main()
