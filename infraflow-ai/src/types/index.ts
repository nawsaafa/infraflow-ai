// Type definitions for InfraFlow AI

export interface Project {
  id: string;
  name: string;
  sponsor: string;
  country: string;
  sector: string;
  total_value: number;
  dfi_partners: string[];
  status: 'active' | 'pending' | 'completed' | 'on-hold';
  risk_score: number;
  created_at: string;
  updated_at: string;
}

export interface Document {
  id: string;
  project_id: string;
  name: string;
  type: string;
  url: string;
  processed: boolean;
  extracted_data?: Record<string, any>;
  embeddings_id?: string;
  created_at: string;
}

export interface FinancialModel {
  id: string;
  project_id: string;
  model_type: string;
  assumptions: Record<string, any>;
  outputs: Record<string, any>;
  scenarios: Record<string, any>;
  created_at: string;
}

export interface ComplianceCheck {
  id: string;
  project_id: string;
  standard: string;
  status: 'compliant' | 'non-compliant' | 'pending';
  issues: string[];
  recommendations: string[];
  checked_at: string;
}

export interface RiskMetric {
  category: string;
  score: number;
  description: string;
  mitigation?: string;
}

export interface PortfolioAnalytics {
  total_projects: number;
  total_value: number;
  average_risk_score: number;
  sector_distribution: Record<string, number>;
  country_distribution: Record<string, number>;
}
