"""
ADGM Compliance Checker Module
Validates documents against ADGM rules, regulations, and compliance requirements
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class ComplianceIssue:
    """Represents a compliance issue found in a document"""
    issue_type: str
    severity: str  # 'High', 'Medium', 'Low'
    description: str
    section: str
    clause: str
    adgm_reference: str
    suggestion: str


class ADGMComplianceChecker:
    """Checks documents for ADGM compliance"""
    
    def __init__(self):
        # ADGM-specific compliance rules and patterns
        self.adgm_jurisdiction_patterns = [
            r'ADGM\s+Courts?',
            r'Abu\s+Dhabi\s+Global\s+Market',
            r'ADGM\s+Companies?\s+Regulations?',
            r'ADGM\s+Commercial\s+Regulations?'
        ]
        
        self.federal_court_patterns = [
            r'UAE\s+Federal\s+Courts?',
            r'Federal\s+Courts?\s+of\s+UAE',
            r'Dubai\s+Courts?',
            r'Abu\s+Dhabi\s+Courts?'
        ]
        
        self.required_clauses = {
            'Articles of Association': [
                'company name',
                'registered office',
                'objects clause',
                'share capital',
                'directors',
                'shareholders',
                'amendment procedures'
            ],
            'Memorandum of Association': [
                'company name',
                'registered office',
                'objects',
                'liability',
                'share capital',
                'subscribers'
            ],
            'Board Resolution': [
                'date',
                'directors present',
                'resolution text',
                'voting results',
                'signatures'
            ]
        }
        
        self.adgm_regulations = {
            'Companies Regulations 2020': [
                'Art. 6 - Company Formation',
                'Art. 15 - Share Capital Requirements',
                'Art. 22 - Director Qualifications',
                'Art. 45 - Corporate Governance'
            ],
            'Commercial Regulations': [
                'Art. 3 - Business Licensing',
                'Art. 8 - Compliance Requirements',
                'Art. 12 - Reporting Obligations'
            ]
        }
    
    def check_jurisdiction_compliance(self, content: str) -> List[ComplianceIssue]:
        """Check if document properly references ADGM jurisdiction"""
        issues = []
        content_lower = content.lower()
        
        # Check for incorrect jurisdiction references
        for pattern in self.federal_court_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                issues.append(ComplianceIssue(
                    issue_type="Jurisdiction Error",
                    severity="High",
                    description=f"Document references {match.group()} instead of ADGM Courts",
                    section="Jurisdiction Clause",
                    clause=match.group(),
                    adgm_reference="ADGM Companies Regulations 2020, Art. 6",
                    suggestion="Update jurisdiction clause to reference ADGM Courts exclusively"
                ))
        
        # Check for ADGM jurisdiction references
        adgm_references = 0
        for pattern in self.adgm_jurisdiction_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            adgm_references += len(list(matches))
        
        if adgm_references == 0:
            issues.append(ComplianceIssue(
                issue_type="Missing ADGM Reference",
                severity="High",
                description="Document does not reference ADGM jurisdiction",
                section="Jurisdiction",
                clause="No ADGM reference found",
                adgm_reference="ADGM Companies Regulations 2020, Art. 6",
                suggestion="Add explicit reference to ADGM jurisdiction and courts"
            ))
        
        return issues
    
    def check_required_clauses(self, document_type: str, content: str) -> List[ComplianceIssue]:
        """Check if document contains all required clauses for its type"""
        issues = []
        
        if document_type not in self.required_clauses:
            return issues
        
        required = self.required_clauses[document_type]
        content_lower = content.lower()
        
        for clause in required:
            if clause not in content_lower:
                issues.append(ComplianceIssue(
                    issue_type="Missing Required Clause",
                    severity="High",
                    description=f"Required clause '{clause}' is missing",
                    section="Document Structure",
                    clause=clause,
                    adgm_reference="ADGM Companies Regulations 2020",
                    suggestion=f"Add {clause} clause to comply with ADGM requirements"
                ))
        
        return issues
    
    def check_legal_language(self, content: str) -> List[ComplianceIssue]:
        """Check for ambiguous or non-binding legal language"""
        issues = []
        
        # Patterns for ambiguous language
        ambiguous_patterns = [
            (r'may\s+or\s+may\s+not', 'Ambiguous language - "may or may not"'),
            (r'at\s+our\s+discretion', 'Vague discretionary language'),
            (r'reasonable\s+efforts?', 'Subjective standard - "reasonable efforts"'),
            (r'best\s+endeavours?', 'Subjective standard - "best endeavours"'),
            (r'subject\s+to\s+availability', 'Conditional language without clear terms')
        ]
        
        for pattern, description in ambiguous_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                issues.append(ComplianceIssue(
                    issue_type="Ambiguous Language",
                    severity="Medium",
                    description=description,
                    section="Legal Language",
                    clause=match.group(),
                    adgm_reference="ADGM Commercial Regulations",
                    suggestion="Replace with specific, binding language"
                ))
        
        return issues
    
    def check_formatting_compliance(self, structure: Dict[str, Any]) -> List[ComplianceIssue]:
        """Check document formatting and structure compliance"""
        issues = []
        
        # Check for proper document structure
        if not structure.get('title'):
            issues.append(ComplianceIssue(
                issue_type="Missing Title",
                severity="Medium",
                description="Document lacks a clear title",
                section="Document Structure",
                clause="No title found",
                adgm_reference="ADGM Document Standards",
                suggestion="Add a clear, descriptive document title"
            ))
        
        # Check for proper sectioning
        if len(structure.get('sections', [])) < 2:
            issues.append(ComplianceIssue(
                issue_type="Poor Structure",
                severity="Low",
                description="Document lacks proper sectioning",
                section="Document Structure",
                clause="Insufficient sections",
                adgm_reference="ADGM Document Standards",
                suggestion="Organize content into clear, numbered sections"
            ))
        
        return issues
    
    def check_compliance(self, document_type: str, content: str, structure: Dict[str, Any]) -> Dict[str, Any]:
        """Main method to check document compliance"""
        all_issues = []
        
        # Run all compliance checks
        all_issues.extend(self.check_jurisdiction_compliance(content))
        all_issues.extend(self.check_required_clauses(document_type, content))
        all_issues.extend(self.check_legal_language(content))
        all_issues.extend(self.check_formatting_compliance(structure))
        
        # Calculate compliance score
        total_checks = len(all_issues)
        high_severity = len([i for i in all_issues if i.severity == 'High'])
        medium_severity = len([i for i in all_issues if i.severity == 'Medium'])
        low_severity = len([i for i in all_issues if i.severity == 'Low'])
        
        if total_checks == 0:
            compliance_score = 100
        else:
            # Weighted scoring: High=3, Medium=2, Low=1
            weighted_score = (high_severity * 3 + medium_severity * 2 + low_severity * 1)
            max_possible_score = total_checks * 3
            compliance_score = max(0, 100 - (weighted_score / max_possible_score) * 100)
        
        return {
            'compliance_score': round(compliance_score, 2),
            'total_issues': total_checks,
            'high_severity_issues': high_severity,
            'medium_severity_issues': medium_severity,
            'low_severity_issues': low_severity,
            'issues': [
                {
                    'type': issue.issue_type,
                    'severity': issue.severity,
                    'description': issue.description,
                    'section': issue.section,
                    'clause': issue.clause,
                    'adgm_reference': issue.adgm_reference,
                    'suggestion': issue.suggestion
                }
                for issue in all_issues
            ],
            'is_compliant': compliance_score >= 80
        }
