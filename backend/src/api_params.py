from fastapi import APIRouter
from src.schemas import AutoParams

router = APIRouter()

auto_params = {
    "QuestionID":"2198",
    "ButtonAlias":"1",
    "HubComputerName":"test",
    "POS":"667",
    "UserText":""
    }

@router.post("/save_auto_params/")
async def save_auto_params(params: AutoParams):
    global auto_params
    auto_params["QuestionID"] = params.QuestionID
    auto_params["ButtonAlias"] = params.ButtonAlias
    auto_params["HubComputerName"] = params.HubComputerName
    auto_params["POS"] = params.POS
    auto_params["UserText"] = params.UserText
    return {"status": "success"}

def get_auto_params():
    return auto_params