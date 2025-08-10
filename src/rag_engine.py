"""
RAG Engine Module
Retrieval-Augmented Generation for ADGM legal knowledge and compliance
"""

import os
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class LegalReference:
    """Represents a legal reference or regulation"""
    title: str
    content: str
    source: str
    article: str
    category: str


class RAGEngine:
    """RAG engine for ADGM legal knowledge retrieval"""
    
    def __init__(self):
        self.legal_knowledge_base = self._initialize_knowledge_base()
        self.adgm_links = self._get_adgm_official_links()
    
    def _initialize_knowledge_base(self) -> Dict[str, List[LegalReference]]:
        """Initialize the ADGM legal knowledge base"""
        knowledge_base = {
            'company_formation': [
                LegalReference(
                    title="Company Formation Requirements",
                    content="Companies must have a registered office in ADGM, minimum share capital as specified, and comply with corporate governance standards.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 6",
                    category="Formation"
                ),
                LegalReference(
                    title="Articles of Association",
                    content="Must include company name, registered office, objects clause, share capital structure, director qualifications, and amendment procedures.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 6",
                    category="Formation"
                ),
                LegalReference(
                    title="Director Qualifications",
                    content="Directors must be at least 18 years old, not disqualified, and meet fit and proper person criteria.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 22",
                    category="Governance"
                )
            ],
            'compliance': [
                LegalReference(
                    title="Compliance Requirements",
                    content="Companies must maintain proper books and records, file annual returns, and comply with ongoing reporting obligations.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 45",
                    category="Compliance"
                ),
                LegalReference(
                    title="Reporting Obligations",
                    content="Annual financial statements, director reports, and changes in company structure must be reported to ADGM.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 45",
                    category="Compliance"
                )
            ],
            'commercial_regulations': [
                LegalReference(
                    title="Business Licensing",
                    content="Business activities require appropriate licenses and compliance with sector-specific regulations.",
                    source="ADGM Commercial Regulations",
                    article="Art. 3",
                    category="Licensing"
                ),
                LegalReference(
                    title="Risk Management",
                    content="Companies must implement appropriate risk management and compliance policies.",
                    source="ADGM Commercial Regulations",
                    article="Art. 12",
                    category="Compliance"
                )
            ],
            'jurisdiction': [
                LegalReference(
                    title="ADGM Jurisdiction",
                    content="All legal matters, disputes, and compliance issues fall under ADGM Courts jurisdiction, not UAE Federal Courts.",
                    source="ADGM Companies Regulations 2020",
                    article="Art. 6",
                    category="Jurisdiction"
                ),
                LegalReference(
                    title="Court System",
                    content="ADGM operates its own court system with specialized commercial and civil courts.",
                    source="ADGM Court Regulations",
                    article="Art. 1",
                    category="Jurisdiction"
                )
            ]
        }
        return knowledge_base
    
    def _get_adgm_official_links(self) -> Dict[str, str]:
        """Get official ADGM links and resources"""
        return {
            'main_website': 'https://www.adgm.com',
            'companies_regulations': 'https://www.adgm.com/operating-in-adgm/legal-framework/companies-regulations-2020',
            'commercial_regulations': 'https://www.adgm.com/operating-in-adgm/legal-framework/commercial-regulations',
            'court_system': 'https://www.adgm.com/operating-in-adgm/legal-framework/court-system',
            'licensing': 'https://www.adgm.com/operating-in-adgm/doing-business-licensing',
            'compliance': 'https://www.adgm.com/operating-in-adgm/operating-compliance'
        }
    
    def search_legal_knowledge(self, query: str, category: Optional[str] = None) -> List[LegalReference]:
        """Search legal knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        # Search across all categories or specific category
        categories_to_search = [category] if category else self.legal_knowledge_base.keys()
        
        for cat in categories_to_search:
            if cat in self.legal_knowledge_base:
                for reference in self.legal_knowledge_base[cat]:
                    # Simple keyword matching (in production, use vector similarity)
                    if (query_lower in reference.title.lower() or 
                        query_lower in reference.content.lower() or
                        query_lower in reference.article.lower()):
                        results.append(reference)
        
        # Sort by relevance (simple scoring)
        results.sort(key=lambda x: self._calculate_relevance_score(query_lower, x), reverse=True)
        
        return results[:5]  # Return top 5 results
    
    def _calculate_relevance_score(self, query: str, reference: LegalReference) -> float:
        """Calculate relevance score for search results"""
        score = 0.0
        
        # Title match gets highest score
        if query in reference.title.lower():
            score += 10.0
        
        # Content match gets medium score
        if query in reference.content.lower():
            score += 5.0
        
        # Article match gets lower score
        if query in reference.article.lower():
            score += 2.0
        
        return score
    
    def get_compliance_guidance(self, document_type: str, issue_type: str) -> List[LegalReference]:
        """Get specific compliance guidance for document types and issues"""
        query = f"{document_type} {issue_type}"
        
        if 'jurisdiction' in issue_type.lower():
            return self.search_legal_knowledge(query, 'jurisdiction')
        elif 'formation' in issue_type.lower():
            return self.search_legal_knowledge(query, 'company_formation')
        elif 'compliance' in issue_type.lower():
            return self.search_legal_knowledge(query, 'compliance')
        else:
            return self.search_legal_knowledge(query)
    
    def get_adgm_reference(self, article: str, regulation: str) -> Optional[LegalReference]:
        """Get specific ADGM regulation reference"""
        for category in self.legal_knowledge_base.values():
            for reference in category:
                if (reference.article.lower() == article.lower() and 
                    regulation.lower() in reference.source.lower()):
                    return reference
        return None
    
    def generate_legal_citation(self, reference: LegalReference) -> str:
        """Generate proper legal citation format"""
        return f"{reference.source}, {reference.article}"
    
    def get_related_regulations(self, category: str) -> List[LegalReference]:
        """Get all regulations in a specific category"""
        return self.legal_knowledge_base.get(category, [])
    
    def get_adgm_links_for_category(self, category: str) -> List[str]:
        """Get relevant ADGM official links for a category"""
        category_links = {
            'company_formation': ['main_website', 'companies_regulations', 'licensing'],
            'compliance': ['compliance', 'companies_regulations'],
            'commercial': ['commercial_regulations', 'licensing'],
            'jurisdiction': ['court_system', 'companies_regulations']
        }
        
        relevant_links = category_links.get(category, [])
        return [self.adgm_links[link] for link in relevant_links if link in self.adgm_links]
    
    def enhance_compliance_analysis(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enhance compliance issues with RAG-generated legal references"""
        enhanced_issues = []
        
        for issue in issues:
            enhanced_issue = issue.copy()
            
            # Get relevant legal guidance
            guidance = self.get_compliance_guidance(
                issue.get('document_type', ''),
                issue.get('type', '')
            )
            
            if guidance:
                # Add legal references
                enhanced_issue['legal_references'] = [
                    {
                        'title': ref.title,
                        'content': ref.content,
                        'source': ref.source,
                        'article': ref.article,
                        'citation': self.generate_legal_citation(ref)
                    }
                    for ref in guidance
                ]
                
                # Add ADGM links
                category = self._determine_issue_category(issue)
                enhanced_issue['adgm_links'] = self.get_adgm_links_for_category(category)
            
            enhanced_issues.append(enhanced_issue)
        
        return enhanced_issues
    
    def _determine_issue_category(self, issue: Dict[str, Any]) -> str:
        """Determine the category of an issue for link generation"""
        issue_type = issue.get('type', '').lower()
        
        if 'jurisdiction' in issue_type:
            return 'jurisdiction'
        elif 'formation' in issue_type or 'clause' in issue_type:
            return 'company_formation'
        elif 'compliance' in issue_type:
            return 'compliance'
        else:
            return 'commercial'
    
    def get_knowledge_base_summary(self) -> Dict[str, Any]:
        """Get summary of available legal knowledge"""
        summary = {}
        
        for category, references in self.legal_knowledge_base.items():
            summary[category] = {
                'total_references': len(references),
                'regulations_covered': list(set(ref.source for ref in references)),
                'articles_covered': list(set(ref.article for ref in references))
            }
        
        return summary
