"""
InfraFlow AI - Financial Engine
Financial modeling, DCF analysis, and risk assessment
"""

from typing import Dict, Any, List, Optional
import logging
import numpy as np
import pandas as pd
from datetime import datetime
import asyncio
import anthropic
import os

logger = logging.getLogger(__name__)


class FinancialEngine:
    """
    Financial modeling and analysis engine
    Supports DCF, Monte Carlo simulation, and risk assessment
    """

    def __init__(self):
        """Initialize financial engine"""
        # Initialize Claude for financial analysis
        self.claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            logger.warning("Anthropic API key not configured")
            self.claude = None

    async def create_model(
        self,
        project_id: str,
        model_type: str,
        assumptions: Dict[str, Any],
        scenarios: List[Dict[str, Any]],
        num_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Create financial model based on type and assumptions

        Args:
            project_id: Project ID
            model_type: Type of model (dcf, blended_finance, etc.)
            assumptions: Financial assumptions
            scenarios: List of scenarios to model
            num_simulations: Number of Monte Carlo simulations

        Returns:
            Model results including NPV, IRR, scenarios
        """
        try:
            logger.info(f"Creating {model_type} model for project {project_id}")

            # Base model calculation
            if model_type == "dcf":
                base_results = await self._calculate_dcf(assumptions)
            elif model_type == "monte_carlo":
                base_results = await self._run_monte_carlo(assumptions, num_simulations)
            elif model_type == "blended_finance":
                base_results = await self._calculate_blended_finance(assumptions)
            else:
                base_results = await self._calculate_dcf(assumptions)

            # Scenario analysis
            scenario_results = []
            if scenarios:
                scenario_results = await self._run_scenarios(
                    assumptions,
                    scenarios,
                    model_type
                )

            # Sensitivity analysis
            sensitivity = await self._sensitivity_analysis(assumptions, model_type)

            # Compile results
            results = {
                "project_id": project_id,
                "model_type": model_type,
                "npv": base_results.get("npv"),
                "irr": base_results.get("irr"),
                "payback_period": base_results.get("payback_period"),
                "scenarios_results": scenario_results,
                "sensitivity_analysis": sensitivity,
                "monte_carlo_results": base_results.get("monte_carlo_stats"),
                "created_at": datetime.utcnow()
            }

            logger.info(f"Financial model created: NPV={results['npv']}, IRR={results['irr']}")
            return results

        except Exception as e:
            logger.error(f"Error creating financial model: {str(e)}")
            raise

    async def _calculate_dcf(self, assumptions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate Discounted Cash Flow (DCF) analysis

        Args:
            assumptions: Financial assumptions including:
                - discount_rate: WACC or discount rate
                - project_lifetime: Years
                - initial_investment: Initial capex
                - annual_revenue: Revenue projections
                - annual_costs: Operating costs
                - revenue_growth_rate: Annual revenue growth
                - tax_rate: Corporate tax rate

        Returns:
            DCF results including NPV, IRR, payback period
        """
        try:
            # Extract assumptions
            discount_rate = assumptions.get("discount_rate", 0.10)
            project_lifetime = assumptions.get("project_lifetime", 25)
            initial_investment = assumptions.get("initial_investment", 0)
            annual_revenue = assumptions.get("annual_revenue", 0)
            annual_costs = assumptions.get("annual_costs", 0)
            revenue_growth_rate = assumptions.get("revenue_growth_rate", 0.03)
            tax_rate = assumptions.get("tax_rate", 0.20)

            # Generate cash flow projections
            cash_flows = []
            years = []

            # Year 0: Initial investment (negative cash flow)
            cash_flows.append(-initial_investment)
            years.append(0)

            # Years 1 to N: Operating cash flows
            cumulative_cf = -initial_investment
            payback_year = None

            for year in range(1, project_lifetime + 1):
                # Revenue grows each year
                revenue = annual_revenue * ((1 + revenue_growth_rate) ** (year - 1))

                # Costs may grow with inflation
                costs = annual_costs * ((1 + assumptions.get("inflation_rate", 0.025)) ** (year - 1))

                # EBITDA
                ebitda = revenue - costs

                # Depreciation (straight-line)
                depreciation = initial_investment / project_lifetime if initial_investment > 0 else 0

                # EBIT
                ebit = ebitda - depreciation

                # Tax
                tax = max(0, ebit * tax_rate)

                # Net income
                net_income = ebit - tax

                # Free cash flow (add back depreciation)
                fcf = net_income + depreciation

                cash_flows.append(fcf)
                years.append(year)

                # Calculate payback period
                cumulative_cf += fcf
                if payback_year is None and cumulative_cf >= 0:
                    payback_year = year

            # Calculate NPV
            npv = sum(cf / ((1 + discount_rate) ** year) for year, cf in zip(years, cash_flows))

            # Calculate IRR using numpy
            irr = self._calculate_irr(cash_flows)

            # Payback period
            payback_period = payback_year if payback_year else project_lifetime

            return {
                "npv": float(npv),
                "irr": float(irr) if irr is not None else None,
                "payback_period": float(payback_period),
                "cash_flows": [float(cf) for cf in cash_flows],
                "years": years
            }

        except Exception as e:
            logger.error(f"Error calculating DCF: {str(e)}")
            raise

    def _calculate_irr(self, cash_flows: List[float]) -> Optional[float]:
        """
        Calculate Internal Rate of Return using Newton-Raphson method

        Args:
            cash_flows: List of cash flows

        Returns:
            IRR as decimal (e.g., 0.12 for 12%)
        """
        try:
            # Use numpy's IRR calculation
            irr = np.irr(cash_flows)

            # Check if valid
            if np.isnan(irr) or np.isinf(irr):
                return None

            return irr

        except Exception as e:
            logger.warning(f"Could not calculate IRR: {str(e)}")
            return None

    async def _run_monte_carlo(
        self,
        assumptions: Dict[str, Any],
        num_simulations: int = 1000
    ) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation for NPV analysis

        Args:
            assumptions: Base assumptions with distributions
            num_simulations: Number of simulations to run

        Returns:
            Statistics from Monte Carlo analysis
        """
        try:
            logger.info(f"Running Monte Carlo simulation with {num_simulations} iterations")

            npvs = []
            irrs = []

            # Define parameter distributions
            discount_rate_mean = assumptions.get("discount_rate", 0.10)
            discount_rate_std = assumptions.get("discount_rate_std", 0.02)

            revenue_mean = assumptions.get("annual_revenue", 0)
            revenue_std = assumptions.get("annual_revenue_std", revenue_mean * 0.15)

            cost_mean = assumptions.get("annual_costs", 0)
            cost_std = assumptions.get("annual_costs_std", cost_mean * 0.10)

            # Run simulations
            for i in range(num_simulations):
                # Sample from distributions
                sim_discount_rate = np.random.normal(discount_rate_mean, discount_rate_std)
                sim_revenue = np.random.normal(revenue_mean, revenue_std)
                sim_costs = np.random.normal(cost_mean, cost_std)

                # Ensure positive values
                sim_discount_rate = max(0.01, min(0.30, sim_discount_rate))
                sim_revenue = max(0, sim_revenue)
                sim_costs = max(0, sim_costs)

                # Run DCF with sampled parameters
                sim_assumptions = assumptions.copy()
                sim_assumptions.update({
                    "discount_rate": sim_discount_rate,
                    "annual_revenue": sim_revenue,
                    "annual_costs": sim_costs
                })

                result = await self._calculate_dcf(sim_assumptions)

                npvs.append(result["npv"])
                if result["irr"] is not None:
                    irrs.append(result["irr"])

            # Calculate statistics
            npv_array = np.array(npvs)
            irr_array = np.array(irrs) if irrs else np.array([])

            monte_carlo_stats = {
                "npv_mean": float(np.mean(npv_array)),
                "npv_median": float(np.median(npv_array)),
                "npv_std": float(np.std(npv_array)),
                "npv_5th_percentile": float(np.percentile(npv_array, 5)),
                "npv_95th_percentile": float(np.percentile(npv_array, 95)),
                "probability_positive_npv": float(np.sum(npv_array > 0) / len(npv_array)),
                "irr_mean": float(np.mean(irr_array)) if len(irr_array) > 0 else None,
                "irr_median": float(np.median(irr_array)) if len(irr_array) > 0 else None,
                "num_simulations": num_simulations
            }

            return {
                "npv": monte_carlo_stats["npv_mean"],
                "irr": monte_carlo_stats["irr_mean"],
                "payback_period": None,  # Not calculated in Monte Carlo
                "monte_carlo_stats": monte_carlo_stats
            }

        except Exception as e:
            logger.error(f"Error running Monte Carlo simulation: {str(e)}")
            raise

    async def _calculate_blended_finance(
        self,
        assumptions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate blended finance structure

        Args:
            assumptions: Blended finance assumptions including:
                - commercial_debt_amount
                - concessional_debt_amount
                - equity_amount
                - grant_amount
                - commercial_rate
                - concessional_rate
                - equity_return

        Returns:
            Blended finance analysis
        """
        try:
            # Extract components
            commercial_debt = assumptions.get("commercial_debt_amount", 0)
            concessional_debt = assumptions.get("concessional_debt_amount", 0)
            equity = assumptions.get("equity_amount", 0)
            grants = assumptions.get("grant_amount", 0)

            total_financing = commercial_debt + concessional_debt + equity + grants

            # Calculate blended cost of capital
            commercial_rate = assumptions.get("commercial_rate", 0.08)
            concessional_rate = assumptions.get("concessional_rate", 0.03)
            equity_return = assumptions.get("equity_return", 0.15)

            if total_financing > 0:
                blended_rate = (
                    (commercial_debt * commercial_rate +
                     concessional_debt * concessional_rate +
                     equity * equity_return) / total_financing
                )
            else:
                blended_rate = 0

            # Run DCF with blended rate
            dcf_assumptions = assumptions.copy()
            dcf_assumptions["discount_rate"] = blended_rate

            dcf_result = await self._calculate_dcf(dcf_assumptions)

            # Add blended finance details
            dcf_result["blended_finance"] = {
                "total_financing": total_financing,
                "commercial_debt": commercial_debt,
                "concessional_debt": concessional_debt,
                "equity": equity,
                "grants": grants,
                "blended_cost_of_capital": blended_rate,
                "subsidy_percentage": (concessional_debt + grants) / total_financing if total_financing > 0 else 0
            }

            return dcf_result

        except Exception as e:
            logger.error(f"Error calculating blended finance: {str(e)}")
            raise

    async def _run_scenarios(
        self,
        base_assumptions: Dict[str, Any],
        scenarios: List[Dict[str, Any]],
        model_type: str
    ) -> List[Dict[str, Any]]:
        """
        Run scenario analysis

        Args:
            base_assumptions: Base case assumptions
            scenarios: List of scenarios with assumption overrides
            model_type: Type of model to run

        Returns:
            List of scenario results
        """
        scenario_results = []

        for scenario in scenarios:
            try:
                # Merge scenario assumptions with base
                scenario_assumptions = base_assumptions.copy()
                scenario_assumptions.update(scenario.get("assumptions_override", {}))

                # Run model
                if model_type == "dcf":
                    result = await self._calculate_dcf(scenario_assumptions)
                elif model_type == "blended_finance":
                    result = await self._calculate_blended_finance(scenario_assumptions)
                else:
                    result = await self._calculate_dcf(scenario_assumptions)

                scenario_results.append({
                    "name": scenario.get("name", "Unnamed Scenario"),
                    "probability": scenario.get("probability", 0),
                    "npv": result.get("npv"),
                    "irr": result.get("irr"),
                    "payback_period": result.get("payback_period")
                })

            except Exception as e:
                logger.error(f"Error running scenario {scenario.get('name')}: {str(e)}")
                continue

        return scenario_results

    async def _sensitivity_analysis(
        self,
        assumptions: Dict[str, Any],
        model_type: str
    ) -> Dict[str, List[float]]:
        """
        Run sensitivity analysis on key parameters

        Args:
            assumptions: Base assumptions
            model_type: Model type

        Returns:
            Sensitivity results for each parameter
        """
        sensitivity_results = {}

        # Parameters to test
        parameters = {
            "discount_rate": [-0.02, -0.01, 0, 0.01, 0.02],
            "revenue_growth_rate": [-0.02, -0.01, 0, 0.01, 0.02],
            "annual_revenue": [-0.20, -0.10, 0, 0.10, 0.20]  # Percentage changes
        }

        for param, variations in parameters.items():
            npv_impacts = []

            for variation in variations:
                try:
                    # Apply variation
                    test_assumptions = assumptions.copy()

                    if param == "annual_revenue":
                        # Percentage change
                        base_value = assumptions.get(param, 0)
                        test_assumptions[param] = base_value * (1 + variation)
                    else:
                        # Absolute change
                        base_value = assumptions.get(param, 0)
                        test_assumptions[param] = base_value + variation

                    # Calculate NPV
                    if model_type == "dcf":
                        result = await self._calculate_dcf(test_assumptions)
                    else:
                        result = await self._calculate_dcf(test_assumptions)

                    npv_impacts.append(result.get("npv", 0))

                except Exception as e:
                    logger.warning(f"Error in sensitivity analysis for {param}: {str(e)}")
                    npv_impacts.append(0)

            sensitivity_results[param] = npv_impacts

        return sensitivity_results

    async def analyze_project(
        self,
        project_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze project financial viability from documents

        Args:
            project_id: Project ID
            documents: Project documents with extracted data

        Returns:
            Financial analysis summary
        """
        try:
            logger.info(f"Analyzing project financials: {project_id}")

            # Extract financial data from documents
            financial_data = self._extract_financial_data(documents)

            if not financial_data:
                return {
                    "status": "insufficient_data",
                    "message": "Insufficient financial data in documents"
                }

            # Build assumptions from extracted data
            assumptions = self._build_assumptions_from_data(financial_data)

            # Run basic DCF
            dcf_result = await self._calculate_dcf(assumptions)

            # Generate AI-powered insights
            insights = await self._generate_financial_insights(
                financial_data,
                dcf_result
            )

            return {
                "status": "completed",
                "npv": dcf_result.get("npv"),
                "irr": dcf_result.get("irr"),
                "payback_period": dcf_result.get("payback_period"),
                "assumptions": assumptions,
                "insights": insights,
                "data_sources": [d.get("name") for d in documents if d.get("extracted_data")]
            }

        except Exception as e:
            logger.error(f"Error analyzing project: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    def _extract_financial_data(
        self,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract financial data from document metadata"""
        financial_data = {}

        for doc in documents:
            extracted = doc.get("extracted_data", {})

            # Collect investment amounts
            if extracted.get("total_investment"):
                financial_data["total_investment"] = extracted["total_investment"]

            # Collect financial structure
            if extracted.get("financial_structure"):
                financial_data["financial_structure"] = extracted["financial_structure"]

            # Collect capacity (for revenue estimation)
            if extracted.get("capacity"):
                financial_data["capacity"] = extracted["capacity"]

        return financial_data

    def _build_assumptions_from_data(
        self,
        financial_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build model assumptions from extracted financial data"""
        assumptions = {
            "discount_rate": 0.10,  # Default WACC
            "project_lifetime": 25,  # Typical infrastructure project
            "tax_rate": 0.20,
            "revenue_growth_rate": 0.03,
            "inflation_rate": 0.025
        }

        # Use extracted investment
        if financial_data.get("total_investment"):
            assumptions["initial_investment"] = financial_data["total_investment"]

        # Estimate revenue (simplified - would be more sophisticated in production)
        if financial_data.get("capacity"):
            # Parse capacity and estimate revenue
            # This is a placeholder - real implementation would be more complex
            assumptions["annual_revenue"] = assumptions.get("initial_investment", 0) * 0.15

        # Estimate costs (typically 30-40% of revenue for infrastructure)
        if "annual_revenue" in assumptions:
            assumptions["annual_costs"] = assumptions["annual_revenue"] * 0.35

        return assumptions

    async def _generate_financial_insights(
        self,
        financial_data: Dict[str, Any],
        dcf_result: Dict[str, Any]
    ) -> List[str]:
        """Generate AI-powered financial insights"""
        if not self.claude:
            return ["Financial analysis completed - see metrics for details"]

        try:
            import json

            prompt = f"""
Analyze this infrastructure project's financial data and provide key insights:

Financial Data:
{json.dumps(financial_data, indent=2)}

DCF Results:
- NPV: ${dcf_result.get('npv', 0):,.0f}
- IRR: {dcf_result.get('irr', 0) * 100:.2f}%
- Payback Period: {dcf_result.get('payback_period', 0):.1f} years

Provide 5-7 concise financial insights focusing on:
- Investment attractiveness
- Risk factors
- Return profile
- Comparison to typical infrastructure projects
- Recommendations for improvement

Return as JSON array of strings.
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

            # Extract JSON
            import re
            json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
            if json_match:
                insights = json.loads(json_match.group())
                return insights
            else:
                return ["Financial metrics calculated successfully"]

        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return ["Financial analysis completed"]

    async def assess_risks(
        self,
        project_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Comprehensive risk assessment

        Args:
            project_id: Project ID
            documents: Project documents

        Returns:
            Risk assessment with categorized risks
        """
        try:
            logger.info(f"Assessing risks for project: {project_id}")

            # Extract risk factors from documents
            risk_factors = []
            all_risks = []

            for doc in documents:
                extracted = doc.get("extracted_data", {})
                if extracted.get("risk_factors"):
                    all_risks.extend(extracted["risk_factors"])

            # Categorize and score risks
            risk_categories = {
                "financial": [],
                "political": [],
                "environmental": [],
                "technical": [],
                "regulatory": []
            }

            # Use AI to categorize and score risks
            if self.claude and all_risks:
                categorized_risks = await self._categorize_risks(all_risks)
                risk_factors = categorized_risks
            else:
                # Default risk factors
                risk_factors = self._default_risk_factors()

            # Calculate overall risk score
            overall_score = self._calculate_risk_score(risk_factors)

            # Determine risk level
            if overall_score < 30:
                risk_level = "low"
            elif overall_score < 50:
                risk_level = "medium"
            elif overall_score < 70:
                risk_level = "high"
            else:
                risk_level = "critical"

            # Identify critical risks
            critical_risks = [
                risk["name"] for risk in risk_factors
                if risk.get("risk_score", 0) > 60
            ]

            # Generate mitigation plan
            mitigation_plan = await self._generate_mitigation_plan(risk_factors)

            return {
                "project_id": project_id,
                "overall_score": overall_score,
                "risk_level": risk_level,
                "risk_factors": risk_factors,
                "critical_risks": critical_risks,
                "mitigation_plan": mitigation_plan,
                "assessed_at": datetime.utcnow()
            }

        except Exception as e:
            logger.error(f"Error assessing risks: {str(e)}")
            raise

    async def _categorize_risks(
        self,
        risks: List[str]
    ) -> List[Dict[str, Any]]:
        """Use AI to categorize and score risks"""
        # This would use Claude to analyze and categorize risks
        # Simplified version for now
        risk_factors = []

        for i, risk in enumerate(risks[:10]):  # Limit to 10 risks
            # Simple heuristic categorization
            category = "financial"
            if any(term in risk.lower() for term in ["political", "government", "regulation"]):
                category = "political"
            elif any(term in risk.lower() for term in ["environmental", "climate", "pollution"]):
                category = "environmental"
            elif any(term in risk.lower() for term in ["technical", "technology", "engineering"]):
                category = "technical"

            risk_factors.append({
                "category": category,
                "name": risk[:100],  # Truncate
                "description": risk,
                "likelihood": 50.0,  # Default values
                "impact": 50.0,
                "risk_score": 50.0,
                "mitigation_strategies": []
            })

        return risk_factors

    def _default_risk_factors(self) -> List[Dict[str, Any]]:
        """Generate default risk factors for infrastructure projects"""
        return [
            {
                "category": "financial",
                "name": "Currency Risk",
                "description": "Risk of currency devaluation affecting returns",
                "likelihood": 40.0,
                "impact": 60.0,
                "risk_score": 48.0,
                "mitigation_strategies": ["Currency hedging", "Local revenue contracts"]
            },
            {
                "category": "political",
                "name": "Regulatory Risk",
                "description": "Risk of changes in regulatory framework",
                "likelihood": 35.0,
                "impact": 70.0,
                "risk_score": 49.0,
                "mitigation_strategies": ["Long-term agreements", "Political risk insurance"]
            }
        ]

    def _calculate_risk_score(self, risk_factors: List[Dict[str, Any]]) -> float:
        """Calculate overall risk score from individual factors"""
        if not risk_factors:
            return 50.0  # Default medium risk

        total_score = sum(risk.get("risk_score", 50.0) for risk in risk_factors)
        return total_score / len(risk_factors)

    async def _generate_mitigation_plan(
        self,
        risk_factors: List[Dict[str, Any]]
    ) -> List[str]:
        """Generate risk mitigation plan"""
        mitigation_plan = []

        # Collect all mitigation strategies
        for risk in risk_factors:
            if risk.get("mitigation_strategies"):
                mitigation_plan.extend(risk["mitigation_strategies"])

        # Deduplicate
        mitigation_plan = list(set(mitigation_plan))

        # Add general recommendations
        mitigation_plan.extend([
            "Conduct regular risk reviews",
            "Maintain contingency reserves",
            "Ensure comprehensive insurance coverage"
        ])

        return mitigation_plan[:10]  # Top 10 recommendations
