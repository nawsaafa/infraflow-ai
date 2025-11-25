import { Search } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const SemanticSearch = () => {
  return (
    <AIModulePlaceholder
      title="Semantic Search"
      description="Intelligent search across all infrastructure project documents using Pinecone vector embeddings"
      icon={Search}
      features={[
        'Natural language queries across all project documentation',
        'Context-aware search results with relevance scoring',
        'Filter by project, sector, country, or time period',
        'Highlight matching passages in source documents',
        'Save and share search queries',
        'Export search results to reports',
      ]}
    />
  );
};

export default SemanticSearch;
