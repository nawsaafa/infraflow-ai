"""
API routes for compliance checking
"""

from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter()


@router.post("/{project_id}/check")
async def check_compliance(
    project_id: UUID,
    standard: str,
):
    """
    Run compliance check against a standard

    Args:
        project_id: UUID of the project
        standard: Compliance standard (ebrd, ifc, eu_taxonomy, etc.)

    Returns:
        Compliance check results
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.get("/{check_id}")
async def get_compliance_check(check_id: UUID):
    """
    Get compliance check details

    Args:
        check_id: UUID of the compliance check

    Returns:
        Compliance check data
    """
    raise HTTPException(status_code=501, detail="Not implemented yet")
