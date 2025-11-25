export type ProjectStatus = 'draft' | 'active' | 'analyzed' | 'completed';
export type ProjectSector = 'energy' | 'transport' | 'water' | 'telecom' | 'social';
export type RiskLevel = 'low' | 'medium' | 'high' | 'critical';

export interface Project {
  id: string;
  name: string;
  country: string;
  sector: ProjectSector;
  status: ProjectStatus;
  investment_amount: number;
  currency: string;
  description?: string;
  dfi_partners?: string[];
  created_at: string;
  updated_at: string;
  risk_score?: number;
  compliance_status?: string;
  financial_irr?: number;
  expected_completion?: string;
}

export interface ProjectFinancials {
  investment_amount: number;
  currency: string;
  irr?: number;
  npv?: number;
  payback_period?: number;
  debt_equity_ratio?: number;
  leverage?: number;
}

export interface RiskAssessment {
  overall_score: number;
  political_risk: RiskLevel;
  financial_risk: RiskLevel;
  operational_risk: RiskLevel;
  esg_risk: RiskLevel;
  mitigation_strategies?: string[];
}

export interface DashboardKPIs {
  total_projects: number;
  total_investment: number;
  active_projects: number;
  countries_count: number;
  dfi_partners_count: number;
  avg_irr?: number;
}

export interface PipelineData {
  status: ProjectStatus;
  count: number;
  value: number;
}
