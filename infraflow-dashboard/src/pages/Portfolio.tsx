import { BarChart3 } from 'lucide-react';
import { AIModulePlaceholder } from './AIModulePlaceholder';

const Portfolio = () => {
  return (
    <AIModulePlaceholder
      title="Portfolio Analytics"
      description="Comprehensive portfolio analysis with charts, maps, and performance metrics"
      icon={BarChart3}
      features={[
        'Portfolio overview with aggregated metrics',
        'Geographic distribution map visualization',
        'Sector allocation charts',
        'Performance tracking over time',
        'Comparative analysis across projects',
        'Custom dashboard creation',
      ]}
    />
  );
};

export default Portfolio;
