import { Calculator } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const FinancialTools = () => {
  return (
    <AIModulePlaceholder
      title="Financial Analysis Tools"
      description="Advanced financial modeling with DCF analysis and sensitivity testing"
      icon={Calculator}
      features={[
        'Discounted Cash Flow (DCF) modeling',
        'Sensitivity analysis with variable parameters',
        'IRR and NPV calculations',
        'Scenario planning (best/base/worst case)',
        'Debt service coverage ratio analysis',
        'Export financial models and visualizations',
      ]}
    />
  );
};

export default FinancialTools;
