"""
ADGM Corporate Agent - Main Application
Main Gradio interface for the ADGM-compliant corporate agent
"""

import os
import json
import logging
from typing import List, Dict, Any, Tuple
import gradio as gr

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Import our modules
from src.document_processor import DocumentProcessor
from src.adgm_checker import ADGMComplianceChecker
from src.checklist_verifier import DocumentChecklistVerifier
from src.comment_generator import CommentGenerator
from src.rag_engine import RAGEngine


class ADGMCorporateAgent:
    """
    Main corporate agent class that orchestrates all functionality.
    """
    
    def __init__(self) -> None:
        self.document_processor = DocumentProcessor()
        self.compliance_checker = ADGMComplianceChecker()
        self.checklist_verifier = DocumentChecklistVerifier()
        self.comment_generator = CommentGenerator()
        self.rag_engine = RAGEngine()
        
        # Create output directory
        self.output_dir = "examples/sample_outputs"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def process_documents(self, files: List[str]) -> Tuple[str, str, str]:
        """
        Main method to process uploaded documents.
        Returns a tuple of (user_message, structured_output, commented_files).
        """
        if not files:
            return "No files uploaded", "", ""
        processed_documents = []
        all_issues = []
        errors = []
        for file_path in files:
            try:
                doc_info = self.document_processor.process_document(file_path)
                processed_documents.append(doc_info)
                compliance_result = self.compliance_checker.check_compliance(
                    doc_info['document_type'],
                    doc_info['text_content'],
                    doc_info['structure']
                )
                enhanced_issues = self.rag_engine.enhance_compliance_analysis(
                    compliance_result['issues']
                )
                for issue in enhanced_issues:
                    issue['document'] = doc_info['file_name']
                    issue['document_type'] = doc_info['document_type']
                all_issues.extend(enhanced_issues)
                doc_info['compliance_score'] = compliance_result['compliance_score']
                doc_info['total_issues'] = compliance_result['total_issues']
            except Exception as e:
                logging.error(f"Error processing {file_path}: {str(e)}")
                errors.append(f"{os.path.basename(file_path)}: {str(e)}")
        checklist_result = self.checklist_verifier.verify_checklist(processed_documents)
        user_message = self.checklist_verifier.generate_user_message(checklist_result)
        structured_output = self._generate_structured_output(
            processed_documents,
            all_issues,
            checklist_result
        )
        commented_files = self._generate_commented_documents(files, all_issues)
        if errors:
            user_message += "\n\nErrors:\n" + "\n".join(errors)
        return user_message, structured_output, commented_files
    
    def _generate_structured_output(self, documents: List[Dict], issues: List[Dict], checklist: Any) -> str:
        """
        Generate structured JSON output.
        """
        output = {
            "process": checklist.process_type,
            "documents_uploaded": checklist.documents_uploaded,
            "required_documents": checklist.required_documents,
            "missing_documents": checklist.missing_documents,
            "completeness_percentage": checklist.completeness_percentage,
            "is_complete": checklist.is_complete,
            "documents": [
                {
                    "file_name": doc['file_name'],
                    "document_type": doc['document_type'],
                    "compliance_score": doc['compliance_score'],
                    "total_issues": doc['total_issues'],
                    "word_count": doc['word_count']
                }
                for doc in documents
            ],
            "issues_found": [
                {
                    "document": issue['document'],
                    "document_type": issue['document_type'],
                    "section": issue['section'],
                    "issue": issue['description'],
                    "severity": issue['severity'],
                    "suggestion": issue['suggestion'],
                    "adgm_reference": issue['adgm_reference']
                }
                for issue in issues
            ]
        }
        
        # Save to file
        output_file = os.path.join(self.output_dir, "analysis_report.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        return json.dumps(output, indent=2, ensure_ascii=False)
    
    def _generate_commented_documents(self, input_files: List[str], issues: List[Dict]) -> str:
        """
        Generate commented versions of documents. Returns a string summary of output files.
        """
        commented_files = []
        
        for file_path in input_files:
            # Group issues by document
            doc_issues = [issue for issue in issues if issue['document'] == os.path.basename(file_path)]
            
            if doc_issues:
                # Create output filename
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(self.output_dir, f"{base_name}_reviewed.docx")
                
                # Add comments to document
                success = self.comment_generator.add_comments_to_document(
                    file_path, doc_issues, output_path
                )
                
                if success:
                    commented_files.append(output_path)
        
        if commented_files:
            return "\n".join([f"✅ {os.path.basename(f)}" for f in commented_files])
        else:
            return "No commented documents generated"
    
    def get_adgm_links(self) -> str:
        """
        Get ADGM official links.
        """
        links = self.rag_engine.adgm_links
        links_text = "## Official ADGM Resources\n\n"
        
        for name, url in links.items():
            display_name = name.replace('_', ' ').title()
            links_text += f"- **[{display_name}]({url})**\n"
        
        return links_text


def create_interface():
    """Create the Gradio interface"""
    agent = ADGMCorporateAgent()
    
    with gr.Blocks(
        title="ADGM Corporate Agent",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .main-header {
            text-align: center;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        """
    ) as interface:
        
        # Header
        gr.HTML("""
        <div class="main-header">
            <h1>🏛️ ADGM Corporate Agent</h1>
            <p>Intelligent AI-powered legal assistant for ADGM compliance and document review</p>
        </div>
        """)
        
        with gr.Row():
            with gr.Column(scale=2):
                # File upload section
                gr.Markdown("## 📄 Upload Documents")
                gr.Markdown("Upload your `.docx` documents for ADGM compliance review")
                
                file_input = gr.File(
                    file_count="multiple",
                    file_types=[".docx"],
                    label="Upload Documents",
                    height=200
                )
                
                process_btn = gr.Button(
                    "🔍 Process Documents",
                    variant="primary",
                    size="lg"
                )
                
                # Results section
                gr.Markdown("## 📊 Analysis Results")
                user_message = gr.Textbox(
                    label="Document Status",
                    lines=3,
                    interactive=False
                )
                
                structured_output = gr.JSON(
                    label="Structured Analysis Report",
                    height=400
                )
                
                commented_files = gr.Textbox(
                    label="Generated Files",
                    lines=2,
                    interactive=False
                )
            
            with gr.Column(scale=1):
                # Information panels
                gr.Markdown("## ℹ️ About the Agent")
                gr.Markdown("""
                This AI-powered corporate agent helps you:
                
                ✅ **Verify ADGM Compliance**
                ✅ **Detect Legal Red Flags**
                ✅ **Check Document Completeness**
                ✅ **Generate Inline Comments**
                ✅ **Provide Legal References**
                
                **Supported Document Types:**
                - Articles of Association
                - Memorandum of Association
                - Board Resolutions
                - Employment Contracts
                - Commercial Agreements
                - Compliance Policies
                """)
                
                # ADGM Links
                adgm_links = gr.Markdown(agent.get_adgm_links())
                
                # Process button action
                process_btn.click(
                    fn=agent.process_documents,
                    inputs=[file_input],
                    outputs=[user_message, structured_output, commented_files]
                )
        
        # Footer
        gr.HTML("""
        <div style="text-align: center; padding: 20px; color: #666;">
            <p>Built with ❤️ for ADGM compliance and legal document review</p>
            <p>Powered by AI and RAG technology</p>
        </div>
        """)
    
    return interface


if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    interface.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        show_error=True
    )
