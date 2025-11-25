import { FileText } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const MemoGenerator = () => {
  return (
    <AIModulePlaceholder
      title="Investment Memo Generator"
      description="AI-powered investment memorandum creation using Claude to synthesize project data"
      icon={FileText}
      features={[
        'Automatically generate investment memos from project data',
        'Customizable templates for different DFI requirements',
        'Executive summary generation',
        'Financial analysis integration',
        'Risk assessment inclusion',
        'Export to PDF, Word, or markdown formats',
      ]}
    />
  );
};

export default MemoGenerator;
