from pydantic import BaseModel, Field
from typing import Literal

class InvestigationReport(BaseModel):

    problem: str = Field(
        description="Description of the application failure"
    )

    evidence: list[str] = Field(
        description="Evidence collected from logs, code, and Git"
    )

    root_cause: str = Field(
        description="Most likely root cause of the incident"
    )

    confidence: Literal["low", "medium", "high"] = Field(
        description="Confidence in the root cause based on evidence"
    )

    affected_files: list[str] = Field(
        description="Source files related to the incident"
    )

    suspected_commit: str | None = Field(
        default=None,
        description="Git commit responsible for the regression, if identified"
    )

    suggested_fix: str = Field(
        description="Recommended solution to the incident"
    )


if __name__ == "__main__":
    report = InvestigationReport(
        problem="Login failure",
        evidence=["Database connection error in logs"],
        root_cause="Incorrect database configuration",
        confidence="high",
        affected_files=["sample_app/database.py"],
        suspected_commit="aab34e2",
        suggested_fix="Restore the previous configuration"
    )

    print(report.model_dump_json(indent=2))

    