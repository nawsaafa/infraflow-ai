import { FileCheck } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const Compliance = () => {
  return (
    <AIModulePlaceholder
      title="AI Compliance Checker"
      description="Automated compliance verification using Claude AI to analyze projects against DFI standards"
      icon={FileCheck}
      features={[
        'Automated compliance checks against DFI policies and frameworks',
        'ESG (Environmental, Social, Governance) assessment',
        'Risk flag identification and categorization',
        'Regulatory requirement mapping',
        'Compliance score calculation with detailed breakdown',
        'Generate compliance reports and recommendations',
      ]}
    />
  );
};

export default Compliance;
