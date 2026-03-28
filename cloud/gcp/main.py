from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class GICDRequest(BaseModel):
    authority_ambiguity: bool
    incentive_misalignment: bool
    cost_externalization: bool
    governance_capture: bool

class GICDResponse(BaseModel):
    status: str
    reason: str

@app.post("/gicd-scan")
async def scan(req: GICDRequest):
    if any([req.authority_ambiguity, req.incentive_misalignment,
            req.cost_externalization, req.governance_capture]):
        return GICDResponse(status="FAIL", reason="One or more GICD markers detected. Agent nucleation blocked.")
    return GICDResponse(status="PASS", reason="All markers clear. Nucleation permitted.")
