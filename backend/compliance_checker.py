"""
InfraFlow AI - Compliance Checker
Compliance verification against DFI and international standards
"""

from typing import Dict, Any, List, Optional
import logging
import os
import asyncio
import anthropic

logger = logging.getLogger(__name__)


class ComplianceChecker:
    """
    Compliance checking engine for infrastructure projects
    Checks against EBRD, IFC, EU Taxonomy, and other standards
    """

    def __init__(self):
        """Initialize compliance checker"""
        # Initialize Claude for compliance analysis
        self.claude_api_key = os.getenv("ANTHROPIC_API_KEY")
        if self.claude_api_key:
            self.claude = anthropic.Anthropic(api_key=self.claude_api_key)
        else:
            logger.warning("Anthropic API key not configured")
            self.claude = None

        # Compliance standards database
        self.standards = self._load_standards()

    def _load_standards(self) -> Dict[str, Dict[str, Any]]:
        """
        Load compliance standards definitions

        Returns:
            Dictionary of standards with their requirements
        """
        return {
            "ebrd_environmental": {
                "name": "EBRD Environmental and Social Policy",
                "categories": [
                    "Environmental and Social Assessment",
                    "Labour and Working Conditions",
                    "Resource Efficiency and Pollution Prevention",
                    "Health and Safety",
                    "Land Acquisition and Involuntary Resettlement",
                    "Biodiversity Conservation",
                    "Indigenous Peoples",
                    "Cultural Heritage",
                    "Financial Intermediaries",
                    "Information Disclosure and Stakeholder Engagement"
                ],
                "key_requirements": [
                    "Environmental and Social Impact Assessment (ESIA)",
                    "Stakeholder Engagement Plan",
                    "Environmental and Social Management System (ESMS)",
                    "Grievance Mechanism",
                    "Disclosure of project information"
                ]
            },
            "ifc_performance": {
                "name": "IFC Performance Standards",
                "categories": [
                    "PS1: Assessment and Management of Environmental and Social Risks",
                    "PS2: Labor and Working Conditions",
                    "PS3: Resource Efficiency and Pollution Prevention",
                    "PS4: Community Health, Safety, and Security",
                    "PS5: Land Acquisition and Involuntary Resettlement",
                    "PS6: Biodiversity Conservation and Sustainable Management",
                    "PS7: Indigenous Peoples",
                    "PS8: Cultural Heritage"
                ],
                "key_requirements": [
                    "Environmental and Social Management System",
                    "Stakeholder Engagement",
                    "Environmental and Social Assessment",
                    "Management Program",
                    "Monitoring and Review"
                ]
            },
            "eu_taxonomy": {
                "name": "EU Taxonomy for Sustainable Activities",
                "categories": [
                    "Climate Change Mitigation",
                    "Climate Change Adaptation",
                    "Sustainable Use of Water and Marine Resources",
                    "Transition to Circular Economy",
                    "Pollution Prevention and Control",
                    "Protection of Healthy Ecosystems"
                ],
                "key_requirements": [
                    "Substantial Contribution to Environmental Objective",
                    "Do No Significant Harm (DNSH) to other objectives",
                    "Minimum Social Safeguards",
                    "Technical Screening Criteria compliance"
                ]
            },
            "local_content": {
                "name": "Local Content Requirements",
                "categories": [
                    "Local Employment",
                    "Local Procurement",
                    "Skills Transfer",
                    "Community Development"
                ],
                "key_requirements": [
                    "Local employment targets",
                    "Local supplier engagement",
                    "Training and capacity building",
                    "Community benefit agreements"
                ]
            },
            "esg_scoring": {
                "name": "ESG Scoring Framework",
                "categories": [
                    "Environmental Performance",
                    "Social Impact",
                    "Governance Structure"
                ],
                "key_requirements": [
                    "Carbon footprint disclosure",
                    "Diversity and inclusion metrics",
                    "Board independence",
                    "Anti-corruption measures"
                ]
            },
            "equator_principles": {
                "name": "Equator Principles",
                "categories": [
                    "Review and Categorization",
                    "Environmental and Social Assessment",
                    "Applicable Standards",
                    "Action Plan and Management System",
                    "Stakeholder Engagement",
                    "Grievance Mechanism",
                    "Independent Review",
                    "Covenants",
                    "Independent Monitoring and Reporting",
                    "Reporting and Transparency"
                ],
                "key_requirements": [
                    "Project categorization (A, B, or C)",
                    "Environmental and Social Impact Assessment",
                    "Environmental and Social Management Plan",
                    "Stakeholder engagement process",
                    "Independent environmental and social consultant"
                ]
            }
        }

    async def check_project(
        self,
        project_id: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check project compliance across all relevant standards

        Args:
            project_id: Project ID
            documents: Project documents with extracted data

        Returns:
            Comprehensive compliance assessment
        """
        try:
            logger.info(f"Checking compliance for project: {project_id}")

            # Determine applicable standards based on project data
            applicable_standards = self._determine_applicable_standards(documents)

            # Run checks for each standard
            all_issues = []
            all_recommendations = []
            standard_results = {}

            for standard in applicable_standards:
                result = await self._check_standard(standard, documents)
                standard_results[standard] = result

                if result.get("issues"):
                    all_issues.extend(result["issues"])
                if result.get("recommendations"):
                    all_recommendations.extend(result["recommendations"])

            # Determine overall status
            critical_issues = [i for i in all_issues if i.get("severity") == "critical"]
            high_issues = [i for i in all_issues if i.get("severity") == "high"]

            if critical_issues:
                overall_status = "non_compliant"
            elif high_issues:
                overall_status = "partial"
            else:
                overall_status = "compliant"

            return {
                "project_id": project_id,
                "overall_status": overall_status,
                "standards_checked": applicable_standards,
                "standard_results": standard_results,
                "issues": all_issues,
                "recommendations": list(set(all_recommendations)),  # Deduplicate
                "total_issues": len(all_issues),
                "critical_issues": len(critical_issues),
                "high_issues": len(high_issues)
            }

        except Exception as e:
            logger.error(f"Error checking compliance: {str(e)}")
            raise

    async def check_standards(
        self,
        project_id: str,
        documents: List[Dict[str, Any]],
        standards: List[str]
    ) -> Dict[str, Any]:
        """
        Check project against specific standards

        Args:
            project_id: Project ID
            documents: Project documents
            standards: List of standard codes to check

        Returns:
            Compliance check results
        """
        try:
            logger.info(f"Checking standards {standards} for project {project_id}")

            all_issues = []
            all_recommendations = []
            standard_results = {}

            for standard in standards:
                if standard not in self.standards:
                    logger.warning(f"Unknown standard: {standard}")
                    continue

                result = await self._check_standard(standard, documents)
                standard_results[standard] = result

                if result.get("issues"):
                    all_issues.extend(result["issues"])
                if result.get("recommendations"):
                    all_recommendations.extend(result["recommendations"])

            # Determine overall status
            critical_issues = [i for i in all_issues if i.get("severity") == "critical"]
            high_issues = [i for i in all_issues if i.get("severity") == "high"]

            if critical_issues:
                overall_status = "non_compliant"
            elif high_issues:
                overall_status = "partial"
            else:
                overall_status = "compliant"

            return {
                "project_id": project_id,
                "overall_status": overall_status,
                "standards_checked": standards,
                "standard_results": standard_results,
                "issues": all_issues,
                "recommendations": list(set(all_recommendations))
            }

        except Exception as e:
            logger.error(f"Error checking standards: {str(e)}")
            raise

    def _determine_applicable_standards(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Determine which standards apply to this project

        Args:
            documents: Project documents

        Returns:
            List of applicable standard codes
        """
        applicable = []

        # Extract project information
        project_info = {}
        for doc in documents:
            if doc.get("extracted_data"):
                project_info.update(doc["extracted_data"])

        # Check for DFI involvement
        dfi_involvement = project_info.get("dfi_involvement", "").lower()

        if "ebrd" in dfi_involvement:
            applicable.append("ebrd_environmental")

        if any(dfi in dfi_involvement for dfi in ["ifc", "world bank", "adb", "afdb"]):
            applicable.append("ifc_performance")

        # Check if EU-related
        country = project_info.get("location", "").lower()
        if any(eu_term in country for eu_term in ["eu", "europe", "european"]):
            applicable.append("eu_taxonomy")

        # Always check local content and ESG
        applicable.extend(["local_content", "esg_scoring"])

        # Check for project finance
        if "project finance" in project_info.get("financial_structure", "").lower():
            applicable.append("equator_principles")

        return list(set(applicable))

    async def _check_standard(
        self,
        standard_code: str,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Check compliance against a specific standard

        Args:
            standard_code: Standard code
            documents: Project documents

        Returns:
            Standard-specific compliance results
        """
        try:
            standard = self.standards.get(standard_code, {})

            # Extract relevant information from documents
            project_data = self._extract_project_data(documents)

            # Use AI to check compliance if available
            if self.claude:
                result = await self._ai_compliance_check(
                    standard_code,
                    standard,
                    project_data
                )
            else:
                # Fallback to rule-based checking
                result = self._rule_based_check(standard_code, standard, project_data)

            return result

        except Exception as e:
            logger.error(f"Error checking standard {standard_code}: {str(e)}")
            return {
                "status": "error",
                "issues": [],
                "recommendations": []
            }

    async def _ai_compliance_check(
        self,
        standard_code: str,
        standard: Dict[str, Any],
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use AI to perform comprehensive compliance check

        Args:
            standard_code: Standard code
            standard: Standard definition
            project_data: Extracted project data

        Returns:
            Compliance check results
        """
        try:
            import json

            prompt = f"""
You are an expert in infrastructure project compliance. Check this project against the {standard['name']}.

Standard Requirements:
{json.dumps(standard, indent=2)}

Project Data:
{json.dumps(project_data, indent=2)}

Analyze the project and identify:
1. Missing requirements or documentation
2. Potential compliance issues
3. Areas needing improvement
4. Specific recommendations

Return your analysis as a JSON object with this structure:
{{
  "status": "compliant" | "partial" | "non_compliant",
  "issues": [
    {{
      "standard": "{standard_code}",
      "severity": "critical" | "high" | "medium" | "low",
      "description": "Description of the issue",
      "reference": "Specific requirement reference",
      "recommendation": "How to address this issue"
    }}
  ],
  "recommendations": ["List of general recommendations"],
  "compliant_areas": ["Areas where project is compliant"],
  "missing_documents": ["Documents that should be provided"]
}}
"""

            message = self.claude.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            response_text = message.content[0].text

            # Extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                # Fallback
                return self._rule_based_check(standard_code, standard, project_data)

        except Exception as e:
            logger.error(f"Error in AI compliance check: {str(e)}")
            return self._rule_based_check(standard_code, standard, project_data)

    def _rule_based_check(
        self,
        standard_code: str,
        standard: Dict[str, Any],
        project_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform rule-based compliance check

        Args:
            standard_code: Standard code
            standard: Standard definition
            project_data: Project data

        Returns:
            Compliance check results
        """
        issues = []
        recommendations = []
        compliant_areas = []

        # Check for key requirements
        key_requirements = standard.get("key_requirements", [])

        for requirement in key_requirements:
            # Simple keyword-based checking
            requirement_lower = requirement.lower()

            # Check if requirement is mentioned in project data
            found = False
            for key, value in project_data.items():
                if isinstance(value, str) and requirement_lower in value.lower():
                    found = True
                    compliant_areas.append(requirement)
                    break

            if not found:
                issues.append({
                    "standard": standard_code,
                    "severity": "medium",
                    "description": f"Missing or incomplete: {requirement}",
                    "reference": standard["name"],
                    "recommendation": f"Provide documentation for {requirement}"
                })
                recommendations.append(f"Develop and submit {requirement}")

        # Determine status
        if len(issues) == 0:
            status = "compliant"
        elif len(issues) > len(key_requirements) / 2:
            status = "non_compliant"
        else:
            status = "partial"

        return {
            "status": status,
            "issues": issues,
            "recommendations": recommendations,
            "compliant_areas": compliant_areas,
            "missing_documents": [i["description"] for i in issues]
        }

    def _extract_project_data(
        self,
        documents: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Extract all relevant project data from documents

        Args:
            documents: Project documents

        Returns:
            Consolidated project data
        """
        project_data = {
            "documents_available": [],
            "stakeholders": [],
            "environmental_data": {},
            "social_data": {},
            "governance_data": {}
        }

        for doc in documents:
            # Document metadata
            project_data["documents_available"].append({
                "name": doc.get("name"),
                "type": doc.get("type")
            })

            # Extracted data
            if doc.get("extracted_data"):
                extracted = doc["extracted_data"]

                # Stakeholders
                if extracted.get("stakeholders"):
                    project_data["stakeholders"].extend(extracted["stakeholders"])

                # Environmental impact
                if extracted.get("environmental_impact"):
                    project_data["environmental_data"].update({
                        "impact_assessment": extracted["environmental_impact"]
                    })

                # Risk factors
                if extracted.get("risk_factors"):
                    project_data["risk_factors"] = extracted["risk_factors"]

                # Financial structure
                if extracted.get("financial_structure"):
                    project_data["financial_structure"] = extracted["financial_structure"]

                # Location and basic info
                for key in ["project_name", "location", "technology", "capacity"]:
                    if extracted.get(key):
                        project_data[key] = extracted[key]

        # Deduplicate stakeholders
        project_data["stakeholders"] = list(set(project_data["stakeholders"]))

        return project_data

    async def generate_compliance_report(
        self,
        project_id: str,
        compliance_results: Dict[str, Any]
    ) -> str:
        """
        Generate formatted compliance report

        Args:
            project_id: Project ID
            compliance_results: Compliance check results

        Returns:
            Formatted report as markdown
        """
        report_lines = [
            f"# Compliance Report - Project {project_id}",
            f"\n**Overall Status:** {compliance_results['overall_status'].upper()}",
            f"\n**Date:** {datetime.utcnow().strftime('%Y-%m-%d')}",
            f"\n## Summary",
            f"- Standards Checked: {len(compliance_results['standards_checked'])}",
            f"- Total Issues: {compliance_results.get('total_issues', 0)}",
            f"- Critical Issues: {compliance_results.get('critical_issues', 0)}",
            f"- High Priority Issues: {compliance_results.get('high_issues', 0)}",
            "\n## Standards Checked"
        ]

        for standard in compliance_results['standards_checked']:
            standard_name = self.standards.get(standard, {}).get("name", standard)
            report_lines.append(f"- {standard_name}")

        if compliance_results.get('issues'):
            report_lines.append("\n## Issues Identified")
            for i, issue in enumerate(compliance_results['issues'], 1):
                report_lines.append(
                    f"\n### {i}. {issue.get('description', 'Unknown Issue')}"
                )
                report_lines.append(f"- **Severity:** {issue.get('severity', 'unknown')}")
                report_lines.append(f"- **Standard:** {issue.get('standard', 'unknown')}")
                if issue.get('reference'):
                    report_lines.append(f"- **Reference:** {issue['reference']}")
                if issue.get('recommendation'):
                    report_lines.append(f"- **Recommendation:** {issue['recommendation']}")

        if compliance_results.get('recommendations'):
            report_lines.append("\n## Recommendations")
            for rec in compliance_results['recommendations']:
                report_lines.append(f"- {rec}")

        return "\n".join(report_lines)


# Import at module level for datetime usage
from datetime import datetime
