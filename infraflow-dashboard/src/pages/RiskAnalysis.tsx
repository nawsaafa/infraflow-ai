import { TrendingUp } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const RiskAnalysis = () => {
  return (
    <AIModulePlaceholder
      title="Risk Analysis & Visualization"
      description="Comprehensive risk assessment with interactive visualizations and scoring"
      icon={TrendingUp}
      features={[
        'Multi-dimensional risk scoring (political, financial, operational, ESG)',
        'Interactive risk matrix visualization',
        'Comparative risk analysis across projects',
        'Historical risk trend tracking',
        'Mitigation strategy recommendations',
        'Risk report generation',
      ]}
    />
  );
};

export default RiskAnalysis;
