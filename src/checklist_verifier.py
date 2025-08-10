"""
Document Checklist Verifier Module
Verifies that all required documents are present for specific legal processes
"""

import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from .document_processor import DocumentProcessor


@dataclass
class DocumentRequirement:
    """Represents a required document for a legal process"""
    document_name: str
    is_mandatory: bool
    description: str
    adgm_reference: str
    content_keywords: List[str]  # Keywords to identify document type from content


@dataclass
class ChecklistResult:
    """Result of checklist verification"""
    process_type: str
    documents_uploaded: int
    required_documents: int
    missing_documents: List[str]
    completeness_percentage: float
    is_complete: bool


class DocumentChecklistVerifier:
    """Verifies document completeness against ADGM checklists"""
    
    def __init__(self):
        # Initialize document processor for text extraction
        self.document_processor = DocumentProcessor()
        
        # Define required documents for different legal processes with content keywords
        self.process_checklists = {
            'Company Incorporation': [
                DocumentRequirement(
                    'Articles of Association',
                    True,
                    'Constitutional document defining company structure',
                    'ADGM Companies Regulations 2020, Art. 6',
                    ['articles of association', 'company articles', 'aoa', 'articles', 'constitutional document', 'company structure']
                ),
                DocumentRequirement(
                    'Memorandum of Association',
                    True,
                    'Document establishing company and its objects',
                    'ADGM Companies Regulations 2020, Art. 6',
                    ['memorandum of association', 'company memorandum', 'memorandum', 'company objects', 'company establishment']
                ),
                DocumentRequirement(
                    'Board Resolution',
                    True,
                    'Resolution authorizing incorporation',
                    'ADGM Companies Regulations 2020, Art. 22',
                    ['board resolution', 'board meeting', 'directors resolution', 'board decision', 'directors decision']
                ),
                DocumentRequirement(
                    'Shareholder Resolution',
                    True,
                    'Resolution approving incorporation',
                    'ADGM Companies Regulations 2020, Art. 15',
                    ['shareholder resolution', 'shareholders resolution', 'member resolution', 'shareholder decision', 'member decision']
                ),
                DocumentRequirement(
                    'Incorporation Application Form',
                    True,
                    'Official application for company registration',
                    'ADGM Companies Regulations 2020, Art. 6',
                    ['incorporation application', 'company registration', 'incorporation form', 'registration application', 'company formation']
                ),
                DocumentRequirement(
                    'UBO Declaration Form',
                    True,
                    'Ultimate Beneficial Owner declaration',
                    'ADGM Companies Regulations 2020, Art. 45',
                    ['ubo declaration', 'ultimate beneficial owner', 'beneficial owner', 'ubo form', 'ownership declaration']
                ),
                DocumentRequirement(
                    'Register of Members and Directors',
                    True,
                    'Register of company members and directors',
                    'ADGM Companies Regulations 2020, Art. 22',
                    ['register of members', 'register of directors', 'members register', 'directors register', 'company register']
                ),
                DocumentRequirement(
                    'Change of Registered Address Notice',
                    False,
                    'Notice of registered office address',
                    'ADGM Companies Regulations 2020, Art. 8',
                    ['change of address', 'registered address', 'office address', 'address change', 'registered office']
                )
            ],
            'Business Licensing': [
                DocumentRequirement(
                    'License Application Form',
                    True,
                    'Application for business license',
                    'ADGM Commercial Regulations, Art. 3',
                    ['license application', 'business license', 'licensing application', 'permit application', 'business permit']
                ),
                DocumentRequirement(
                    'Business Plan',
                    True,
                    'Detailed business plan and projections',
                    'ADGM Commercial Regulations, Art. 3',
                    ['business plan', 'business strategy', 'business proposal', 'business model', 'business projections']
                ),
                DocumentRequirement(
                    'Financial Statements',
                    True,
                    'Audited financial statements',
                    'ADGM Commercial Regulations, Art. 8',
                    ['financial statements', 'financial report', 'audited accounts', 'financial accounts', 'balance sheet']
                ),
                DocumentRequirement(
                    'Compliance Policy',
                    True,
                    'Compliance and risk management policy',
                    'ADGM Commercial Regulations, Art. 12',
                    ['compliance policy', 'risk management', 'compliance procedures', 'risk policy', 'compliance framework']
                ),
                DocumentRequirement(
                    'Board Resolution',
                    True,
                    'Resolution approving license application',
                    'ADGM Commercial Regulations, Art. 3',
                    ['board resolution', 'board meeting', 'directors resolution', 'board decision', 'directors decision']
                )
            ],
            'Employment Contracts': [
                DocumentRequirement(
                    'Employment Contract',
                    True,
                    'Standard employment agreement',
                    'ADGM Employment Regulations',
                    ['employment contract', 'employment agreement', 'work contract', 'employment terms', 'work agreement']
                ),
                DocumentRequirement(
                    'Job Description',
                    True,
                    'Detailed job role and responsibilities',
                    'ADGM Employment Regulations',
                    ['job description', 'role description', 'position description', 'job responsibilities', 'role requirements']
                ),
                DocumentRequirement(
                    'Company Policies',
                    False,
                    'Relevant company policies and procedures',
                    'ADGM Employment Regulations',
                    ['company policies', 'company procedures', 'workplace policies', 'employment policies', 'company rules']
                ),
                DocumentRequirement(
                    'Board Resolution',
                    True,
                    'Resolution approving employment terms',
                    'ADGM Employment Regulations',
                    ['board resolution', 'board meeting', 'directors resolution', 'board decision', 'directors decision']
                )
            ],
            'Commercial Agreements': [
                DocumentRequirement(
                    'Commercial Agreement',
                    True,
                    'Main commercial contract',
                    'ADGM Commercial Regulations',
                    ['commercial agreement', 'commercial contract', 'business agreement', 'commercial terms', 'business contract']
                ),
                DocumentRequirement(
                    'Due Diligence Report',
                    True,
                    'Due diligence findings',
                    'ADGM Commercial Regulations',
                    ['due diligence', 'due diligence report', 'diligence findings', 'investigation report', 'background check']
                ),
                DocumentRequirement(
                    'Board Resolution',
                    True,
                    'Resolution approving agreement',
                    'ADGM Commercial Regulations',
                    ['board resolution', 'board meeting', 'directors resolution', 'board decision', 'directors decision']
                ),
                DocumentRequirement(
                    'Legal Opinion',
                    False,
                    'Legal opinion on agreement terms',
                    'ADGM Commercial Regulations',
                    ['legal opinion', 'legal advice', 'legal assessment', 'legal review', 'legal counsel']
                )
            ]
        }
    
    def extract_docx_text(self, file_path: str) -> str:
        """Extract plain text from .docx file using document processor"""
        try:
            return self.document_processor.extract_text(file_path)
        except Exception as e:
            print(f"Warning: Could not extract text from {file_path}: {str(e)}")
            return ""
    
    def match_document_type(self, text: str, filename: str, required_doc: DocumentRequirement) -> bool:
        """
        Match document type based on content keywords and filename fallback
        
        Args:
            text: Extracted text content from the document
            filename: Original filename of the uploaded document
            required_doc: DocumentRequirement object with keywords and name
            
        Returns:
            True if document matches, False otherwise
        """
        # Convert text to lowercase for case-insensitive matching
        text_lower = text.lower()
        
        # Check content-based matching using keywords
        for keyword in required_doc.content_keywords:
            if keyword.lower() in text_lower:
                return True
        
        # Fallback: Check filename matching
        normalized_filename = self._normalize_filename(filename)
        normalized_required = self._normalize_filename(required_doc.document_name)
        
        if normalized_filename == normalized_required:
            return True
        
        # Additional fallback: Check if any keyword appears in filename
        for keyword in required_doc.content_keywords:
            if keyword.lower() in filename.lower():
                return True
        
        return False
    
    def identify_process_type(self, uploaded_documents: List[Dict[str, Any]]) -> str:
        """Identify the legal process based on uploaded documents"""
        document_types = [doc.get('document_type', '') for doc in uploaded_documents]
        
        # Scoring system to identify process type
        process_scores = {
            'Company Incorporation': 0,
            'Business Licensing': 0,
            'Employment Contracts': 0,
            'Commercial Agreements': 0
        }
        
        # Score based on document types
        for doc_type in document_types:
            if doc_type in ['Articles of Association', 'Memorandum of Association']:
                process_scores['Company Incorporation'] += 3
            elif doc_type in ['License Application Form', 'Business Plan']:
                process_scores['Business Licensing'] += 3
            elif doc_type in ['Employment Contract', 'Job Description']:
                process_scores['Employment Contracts'] += 3
            elif doc_type in ['Commercial Agreement', 'Due Diligence Report']:
                process_scores['Commercial Agreements'] += 3
            
            # Additional scoring for common documents
            if doc_type == 'Board Resolution':
                for process in process_scores:
                    process_scores[process] += 1
        
        # Return process with highest score
        return max(process_scores, key=process_scores.get)
    
    def _normalize_filename(self, filename: str) -> str:
        """Normalize filename for comparison by removing extensions, replacing separators, and converting to lowercase"""
        # Strip leading/trailing spaces first
        filename = filename.strip()
        
        # Handle common file extensions (case-insensitive)
        common_extensions = ['.docx', '.doc', '.pdf', '.txt', '.rtf', '.odt']
        name_without_ext = filename
        
        # Remove file extension if it's a common one (case-insensitive)
        filename_lower = filename.lower()
        for ext in common_extensions:
            if filename_lower.endswith(ext):
                name_without_ext = filename[:-len(ext)]
                break
        
        # Replace underscores, hyphens, and dots with spaces
        normalized = name_without_ext.replace('_', ' ').replace('-', ' ').replace('.', ' ')
        
        # Convert to lowercase and strip extra spaces
        normalized = ' '.join(normalized.lower().split())
        
        return normalized
    
    def _find_matching_document(self, uploaded_filename: str, required_document_names: List[str]) -> Optional[str]:
        """Find a matching required document name for an uploaded filename (fallback method)"""
        normalized_uploaded = self._normalize_filename(uploaded_filename)
        
        for required_name in required_document_names:
            normalized_required = self._normalize_filename(required_name)
            if normalized_uploaded == normalized_required:
                return required_name
        
        return None
    
    def verify_checklist(self, uploaded_documents: List[Dict[str, Any]]) -> ChecklistResult:
        """Verify document completeness against required checklist using content-based matching with filename fallback"""
        if not uploaded_documents:
            return ChecklistResult(
                process_type="Unknown",
                documents_uploaded=0,
                required_documents=0,
                missing_documents=[],
                completeness_percentage=0.0,
                is_complete=False
            )
        
        # Identify process type
        process_type = self.identify_process_type(uploaded_documents)
        
        if process_type not in self.process_checklists:
            return ChecklistResult(
                process_type="Unknown Process",
                documents_uploaded=len(uploaded_documents),
                required_documents=0,
                missing_documents=[],
                completeness_percentage=0.0,
                is_complete=False
            )
        
        # Get required documents for this process
        required_docs = self.process_checklists[process_type]
        mandatory_docs = [doc.document_name for doc in required_docs if doc.is_mandatory]
        
        # Track which required documents are found
        found_documents = set()
        
        # Check each uploaded document against required documents using content-based matching
        for uploaded_doc in uploaded_documents:
            uploaded_filename = uploaded_doc.get('file_name', '')
            file_path = uploaded_doc.get('file_path', '')
            
            if not uploaded_filename or not file_path:
                continue
            
            # Extract text content for content-based matching
            text_content = self.extract_docx_text(file_path)
            
            # Try content-based matching first
            for required_doc in required_docs:
                if required_doc.is_mandatory and required_doc.document_name not in found_documents:
                    if self.match_document_type(text_content, uploaded_filename, required_doc):
                        found_documents.add(required_doc.document_name)
                        break
            
            # If no content match found, try filename fallback
            if not any(self.match_document_type(text_content, uploaded_filename, doc) for doc in required_docs if doc.is_mandatory):
                matching_doc = self._find_matching_document(uploaded_filename, mandatory_docs)
                if matching_doc and matching_doc not in found_documents:
                    found_documents.add(matching_doc)
        
        # Find missing mandatory documents
        missing_docs = [doc for doc in mandatory_docs if doc not in found_documents]
        
        # Calculate completeness
        total_mandatory = len(mandatory_docs)
        uploaded_mandatory = len(found_documents)
        completeness_percentage = (uploaded_mandatory / total_mandatory) * 100 if total_mandatory > 0 else 0
        
        return ChecklistResult(
            process_type=process_type,
            documents_uploaded=len(uploaded_documents),
            required_documents=total_mandatory,
            missing_documents=missing_docs,
            completeness_percentage=round(completeness_percentage, 2),
            is_complete=len(missing_docs) == 0
        )
    
    def get_process_description(self, process_type: str) -> str:
        """Get human-readable description of the legal process"""
        descriptions = {
            'Company Incorporation': 'You are attempting to incorporate a company in ADGM',
            'Business Licensing': 'You are applying for a business license in ADGM',
            'Employment Contracts': 'You are setting up employment contracts for ADGM operations',
            'Commercial Agreements': 'You are establishing commercial agreements for ADGM business'
        }
        return descriptions.get(process_type, 'Unknown legal process')
    
    def generate_user_message(self, result: ChecklistResult) -> str:
        """Generate user-friendly message about document completeness"""
        process_desc = self.get_process_description(result.process_type)
        
        if result.is_complete:
            return f"Excellent! {process_desc}. You have uploaded all {result.required_documents} required documents. Your submission is complete and ready for review."
        else:
            missing_list = ', '.join([f"'{doc}'" for doc in result.missing_documents])
            return f"{process_desc}. Based on our reference list, you have uploaded {result.documents_uploaded} out of {result.required_documents} required documents. The missing document(s) appear to be: {missing_list}."
    
    def get_adgm_references(self, process_type: str) -> List[str]:
        """Get ADGM regulatory references for the process"""
        if process_type not in self.process_checklists:
            return []
        
        references = set()
        for doc_req in self.process_checklists[process_type]:
            if doc_req.adgm_reference:
                references.add(doc_req.adgm_reference)
        
        return list(references)
