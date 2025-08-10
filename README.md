# ADGM-Compliant Corporate Agent with Document Intelligence

An intelligent AI-powered legal assistant that helps review, validate, and prepare documentation for business incorporation and compliance within the Abu Dhabi Global Market (ADGM) jurisdiction.

## Features

- **Document Processing**: Accepts and parses `.docx` documents
- **ADGM Compliance Check**: Verifies documents against ADGM rules and regulations
- **Red Flag Detection**: Identifies legal inconsistencies and compliance issues
- **Intelligent Commenting**: Inserts contextual comments with legal citations
- **Document Checklist Verification**: Ensures all required documents are present
- **RAG Integration**: Uses Retrieval-Augmented Generation for legal accuracy
- **Structured Output**: Generates comprehensive JSON reports

## Project Structure

```
corporate-agent/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── src/
│   ├── __init__.py
│   ├── document_processor.py    # Document parsing and analysis
│   ├── adgm_checker.py         # ADGM compliance validation
│   ├── red_flag_detector.py    # Legal issue detection
│   ├── comment_generator.py    # Inline comment generation
│   ├── checklist_verifier.py   # Document completeness check
│   └── rag_engine.py           # RAG implementation
├── data/
│   ├── adgm_references/        # ADGM legal documents
│   └── templates/              # Document templates
# ADGM Corporate Agent

Automated document review and annotation for ADGM compliance.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/2CentsCapitalHR/ai-engineer-task-Rahul0880.git
   cd ai-engineer-task-Rahul0880
   ```

2. **(Optional) Create a virtual environment:**
   ```sh
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```sh
   python -m app
   ```

## Example Usage
- Upload a `.docx` document via the Gradio interface.
- The app will generate:
  - An annotated `.docx` file (with inline comments)
  - A structured output file (`analysis_report.json`)

## Example Files
- `examples/sample_documents/sample_contract_compliant.docx` (before)
- `examples/sample_outputs/sample_contract_compliant_reviewed.docx` (after)
- `examples/sample_outputs/analysis_report.json` (structured output)

## Notes
- All comments are added as visible text in the document, not as native Word comments.
- For more details, see the code in `src/comment_generator.py`.
```

## Usage

1. Open your browser and navigate to the Gradio interface
2. Upload one or more `.docx` documents
3. The system will automatically:
   - Parse and analyze the documents
   - Check for ADGM compliance
   - Detect red flags and legal issues
   - Insert contextual comments
   - Verify document completeness
4. Download the reviewed document and structured report

## API Configuration

The system supports multiple LLM providers:
- OpenAI GPT models
- Google Gemini
- Anthropic Claude
- Ollama (local models)

Configure your preferred provider in the `.env` file.

## Document Types Supported

- **Company Formation**: Articles of Association, Memorandum of Association, Board Resolutions
- **Regulatory Filings**: Licensing, compliance documents
- **Employment Contracts**: HR agreements and policies
- **Commercial Agreements**: Business contracts and partnerships

## Output Format

The system generates:
1. **Reviewed .docx file** with inline comments and highlights
2. **Structured JSON report** containing:
   - Process identification
   - Document completeness status
   - Issues found with severity levels
   - Legal citations and suggestions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is for educational and evaluation purposes.

## Support

For issues and questions, please refer to the project documentation or create an issue in the repository.
