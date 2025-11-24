"""
InfraFlow AI - Document Processor
Document processing with LangChain and AI-powered extraction
"""

from typing import Dict, Any, List, Optional
import os
import logging
import tempfile
import asyncio
from datetime import datetime
import hashlib

from fastapi import UploadFile
from langchain_community.document_loaders import (
    UnstructuredFileLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Pinecone as PineconeLangChain
from pinecone import Pinecone, ServerlessSpec
import anthropic

from database import Database

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Document processing with AI-powered extraction and analysis
    Implements the DocumentProcessor class from SPARC lines 313-365
    """

    def __init__(self):
        """Initialize document processor with AI services"""
        self.db = Database()

        # LangChain components
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000,
            chunk_overlap=200,
            length_function=len,
            separators=["\n\n", "\n", " ", ""]
        )

        # Initialize embeddings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if self.openai_api_key:
            self.embeddings = OpenAIEmbeddings(
                openai_api_key=self.openai_api_key,
                model="text-embedding-3-small"
            )
        else:
            logger.warning("OpenAI API key not configured")
            self.embeddings = None

        # Initialize Pinecone for vector storage
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_env = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
        self.pinecone_index = os.getenv("PINECONE_INDEX", "infraflow-docs")

        if self.pinecone_api_key:
            self.pc = Pinecone(api_key=self.pinecone_api_key)
            self._ensure_pinecone_index()
        else:
            logger.warning("Pinecone API key not configured")
            self.pc = None

        # Initialize Claude for extraction
        self.claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            logger.warning("Anthropic API key not configured")
            self.claude = None

        # Storage bucket for documents
        self.storage_bucket = os.getenv("STORAGE_BUCKET", "documents")

    def _ensure_pinecone_index(self):
        """Ensure Pinecone index exists"""
        try:
            # Check if index exists
            existing_indexes = self.pc.list_indexes()
            index_names = [index.name for index in existing_indexes]

            if self.pinecone_index not in index_names:
                logger.info(f"Creating Pinecone index: {self.pinecone_index}")
                self.pc.create_index(
                    name=self.pinecone_index,
                    dimension=1536,  # OpenAI embedding dimension
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=self.pinecone_env
                    )
                )
                logger.info("Pinecone index created successfully")

        except Exception as e:
            logger.error(f"Error ensuring Pinecone index: {str(e)}")

    async def process_document(
        self,
        file: UploadFile,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Process uploaded document through full pipeline

        Args:
            file: Uploaded file
            project_id: Project ID to associate document with

        Returns:
            Document metadata with extraction results
        """
        try:
            logger.info(f"Processing document: {file.filename} for project {project_id}")

            # Stage 1: Save file to temporary location
            temp_path = await self._save_temp_file(file)

            try:
                # Stage 2: Load and parse document
                raw_docs = await self._load_document(temp_path, file.filename)

                # Stage 3: Smart chunking
                chunks = self.text_splitter.split_documents(raw_docs)
                logger.info(f"Document split into {len(chunks)} chunks")

                # Stage 4: Extract key information using Claude
                extracted_data = await self._extract_key_info(chunks, file.filename)

                # Stage 5: Generate embeddings and store in vector DB
                embeddings_id = None
                if self.embeddings and self.pc:
                    embeddings_id = await self._store_embeddings(
                        chunks,
                        project_id,
                        file.filename
                    )

                # Stage 6: Upload to permanent storage
                file_url = await self._upload_to_storage(temp_path, project_id, file.filename)

                # Stage 7: Save document metadata to database
                document_data = {
                    "project_id": project_id,
                    "name": file.filename,
                    "type": self._detect_document_type(file.filename, extracted_data),
                    "url": file_url,
                    "processed": True,
                    "extracted_data": extracted_data,
                    "embeddings_id": embeddings_id,
                    "created_at": datetime.utcnow()
                }

                document_id = await self.db.create_document(document_data)

                logger.info(f"Document processed successfully: {document_id}")

                return {
                    "id": document_id,
                    "name": file.filename,
                    "type": document_data["type"],
                    "url": file_url,
                    "extracted_data": extracted_data
                }

            finally:
                # Cleanup temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)

        except Exception as e:
            logger.error(f"Error processing document {file.filename}: {str(e)}")
            raise

    async def _save_temp_file(self, file: UploadFile) -> str:
        """Save uploaded file to temporary location"""
        suffix = os.path.splitext(file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            content = await file.read()
            tmp.write(content)
            return tmp.name

    async def _load_document(self, file_path: str, filename: str) -> List[Any]:
        """
        Load document using appropriate loader based on file type

        Args:
            file_path: Path to file
            filename: Original filename

        Returns:
            List of loaded documents
        """
        ext = os.path.splitext(filename)[1].lower()

        try:
            if ext == '.pdf':
                loader = PyPDFLoader(file_path)
            elif ext in ['.docx', '.doc']:
                loader = Docx2txtLoader(file_path)
            elif ext in ['.xlsx', '.xls']:
                loader = UnstructuredExcelLoader(file_path)
            else:
                # Use unstructured for other formats
                loader = UnstructuredFileLoader(file_path)

            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            docs = await loop.run_in_executor(None, loader.load)

            return docs

        except Exception as e:
            logger.error(f"Error loading document {filename}: {str(e)}")
            raise

    async def _extract_key_info(
        self,
        chunks: List[Any],
        filename: str
    ) -> Dict[str, Any]:
        """
        Extract key information from document using Claude

        Implements extraction logic from SPARC lines 349-365

        Args:
            chunks: Document chunks
            filename: Document filename

        Returns:
            Extracted structured data
        """
        if not self.claude:
            logger.warning("Claude not configured, skipping extraction")
            return {}

        try:
            # Combine first few chunks for analysis
            content = "\n\n".join([chunk.page_content for chunk in chunks[:5]])

            # Truncate if too long
            if len(content) > 100000:
                content = content[:100000]

            extraction_prompt = f"""
Extract key information from this infrastructure project document ({filename}).

Return a JSON object with the following fields (use null for missing information):
- project_name: Name of the project
- location: Project location (country, region, city)
- total_investment: Total investment value (extract number only)
- currency: Currency of investment
- stakeholders: List of key stakeholders mentioned
- technology: Technology type or specifications
- capacity: Project capacity (e.g., MW, MW/h)
- environmental_impact: Key environmental metrics or impacts
- financial_structure: Description of financial structure
- risk_factors: List of identified risk factors
- timeline: Key milestones and timeline
- sponsor: Project sponsor or developer
- dfi_involvement: Any DFI or development bank involvement mentioned

Document content:
{content}
"""

            # Call Claude API
            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": extraction_prompt
                }]
            )

            # Parse response
            response_text = message.content[0].text

            # Extract JSON from response
            import json
            import re

            # Try to find JSON in response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                extracted = json.loads(json_match.group())
            else:
                extracted = {}

            logger.info(f"Extracted data from {filename}: {list(extracted.keys())}")
            return extracted

        except Exception as e:
            logger.error(f"Error extracting information: {str(e)}")
            return {}

    async def _store_embeddings(
        self,
        chunks: List[Any],
        project_id: str,
        filename: str
    ) -> str:
        """
        Generate embeddings and store in Pinecone

        Args:
            chunks: Document chunks
            project_id: Project ID
            filename: Document filename

        Returns:
            Embeddings namespace ID
        """
        try:
            # Generate unique namespace for this project
            namespace = f"project_{project_id}"

            # Prepare texts for embedding
            texts = [chunk.page_content for chunk in chunks]
            metadatas = [
                {
                    "project_id": project_id,
                    "filename": filename,
                    "chunk_index": i,
                    "source": chunk.metadata.get("source", "")
                }
                for i, chunk in enumerate(chunks)
            ]

            # Generate embeddings
            loop = asyncio.get_event_loop()
            vectors = await loop.run_in_executor(
                None,
                self.embeddings.embed_documents,
                texts
            )

            # Store in Pinecone
            index = self.pc.Index(self.pinecone_index)

            # Prepare vectors for upsert
            vectors_to_upsert = []
            for i, (vector, metadata) in enumerate(zip(vectors, metadatas)):
                vector_id = hashlib.md5(
                    f"{project_id}_{filename}_{i}".encode()
                ).hexdigest()

                vectors_to_upsert.append({
                    "id": vector_id,
                    "values": vector,
                    "metadata": {**metadata, "text": texts[i][:1000]}  # Store snippet
                })

            # Upsert in batches
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                index.upsert(vectors=batch, namespace=namespace)

            logger.info(f"Stored {len(vectors)} embeddings in namespace {namespace}")
            return namespace

        except Exception as e:
            logger.error(f"Error storing embeddings: {str(e)}")
            return None

    async def _upload_to_storage(
        self,
        file_path: str,
        project_id: str,
        filename: str
    ) -> str:
        """
        Upload file to permanent storage

        Args:
            file_path: Local file path
            project_id: Project ID
            filename: Original filename

        Returns:
            Public URL of uploaded file
        """
        try:
            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()

            # Generate storage path
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            storage_path = f"{project_id}/{timestamp}_{filename}"

            # Upload to Supabase storage
            url = self.db.upload_file(
                bucket=self.storage_bucket,
                file_path=storage_path,
                file_data=file_data
            )

            return url

        except Exception as e:
            logger.error(f"Error uploading to storage: {str(e)}")
            # Return local path as fallback
            return f"file://{file_path}"

    def _detect_document_type(
        self,
        filename: str,
        extracted_data: Dict[str, Any]
    ) -> str:
        """
        Detect document type from filename and content

        Args:
            filename: Document filename
            extracted_data: Extracted content

        Returns:
            Document type
        """
        filename_lower = filename.lower()

        # Check filename patterns
        if any(term in filename_lower for term in ['feasibility', 'study', 'assessment']):
            return "feasibility_study"
        elif any(term in filename_lower for term in ['financial', 'model', 'fcf', 'dcf']):
            return "financial_model"
        elif any(term in filename_lower for term in ['environmental', 'eia', 'impact']):
            return "environmental_impact"
        elif any(term in filename_lower for term in ['technical', 'specs', 'specification']):
            return "technical_specs"
        elif any(term in filename_lower for term in ['legal', 'agreement', 'contract']):
            return "legal_agreement"
        elif any(term in filename_lower for term in ['compliance', 'regulatory']):
            return "compliance_report"
        else:
            return "other"

    async def generate_project_summary(
        self,
        project_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive project summary from all documents

        Args:
            project_id: Project ID
            documents: List of project documents

        Returns:
            Project summary with key findings
        """
        try:
            # Collect all extracted data
            all_extracted_data = []
            stakeholders = set()
            total_investment = None
            technologies = set()

            for doc in documents:
                if doc.get("extracted_data"):
                    data = doc["extracted_data"]
                    all_extracted_data.append(data)

                    # Aggregate stakeholders
                    if data.get("stakeholders"):
                        stakeholders.update(data["stakeholders"])

                    # Get investment amount
                    if data.get("total_investment") and not total_investment:
                        total_investment = data["total_investment"]

                    # Collect technologies
                    if data.get("technology"):
                        technologies.add(data["technology"])

            # Generate summary
            summary = {
                "total_documents": len(documents),
                "processed_documents": sum(1 for d in documents if d.get("processed")),
                "total_investment": total_investment,
                "stakeholders": list(stakeholders),
                "technologies": list(technologies),
                "key_findings": await self._generate_key_findings(all_extracted_data),
                "document_types": self._count_document_types(documents)
            }

            return summary

        except Exception as e:
            logger.error(f"Error generating project summary: {str(e)}")
            return {
                "total_documents": len(documents),
                "error": str(e)
            }

    async def _generate_key_findings(
        self,
        extracted_data_list: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Generate key findings from extracted data using Claude

        Args:
            extracted_data_list: List of extracted data from documents

        Returns:
            List of key findings
        """
        if not self.claude or not extracted_data_list:
            return []

        try:
            import json

            data_summary = json.dumps(extracted_data_list, indent=2)

            prompt = f"""
Analyze this infrastructure project data and provide 5-7 key findings:

{data_summary}

Provide concise, actionable findings focusing on:
- Project viability and strength
- Financial structure
- Key risks or concerns
- Stakeholder alignment
- Technical feasibility

Return findings as a JSON array of strings.
"""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text

            # Extract JSON array
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                findings = json.loads(json_match.group())
                return findings
            else:
                return ["Analysis completed - see extracted data for details"]

        except Exception as e:
            logger.error(f"Error generating key findings: {str(e)}")
            return []

    def _count_document_types(self, documents: List[Dict[str, Any]]) -> Dict[str, int]:
        """Count documents by type"""
        type_counts = {}
        for doc in documents:
            doc_type = doc.get("type", "unknown")
            type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
        return type_counts

    async def query_project_documents(
        self,
        project_id: str,
        query: str,
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Query project documents using vector similarity search

        Args:
            project_id: Project ID
            query: Search query
            top_k: Number of results to return

        Returns:
            List of relevant document chunks
        """
        if not self.embeddings or not self.pc:
            logger.warning("Embeddings or Pinecone not configured")
            return []

        try:
            # Generate query embedding
            loop = asyncio.get_event_loop()
            query_vector = await loop.run_in_executor(
                None,
                self.embeddings.embed_query,
                query
            )

            # Query Pinecone
            index = self.pc.Index(self.pinecone_index)
            namespace = f"project_{project_id}"

            results = index.query(
                vector=query_vector,
                top_k=top_k,
                namespace=namespace,
                include_metadata=True
            )

            # Format results
            formatted_results = []
            for match in results.matches:
                formatted_results.append({
                    "score": match.score,
                    "text": match.metadata.get("text", ""),
                    "filename": match.metadata.get("filename", ""),
                    "chunk_index": match.metadata.get("chunk_index", 0)
                })

            return formatted_results

        except Exception as e:
            logger.error(f"Error querying documents: {str(e)}")
            return []
